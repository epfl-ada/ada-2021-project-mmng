
import bz2
import json

import pandas as pd

from helpers import *


#=============================================================================
# Wikidata speaker_attribute data processing

def load_wikidata():
    df_sa = pd.read_parquet(SPEAKER_ATTRIBUTES_PATH)
    return df_sa


def speaker_attribute_processing(df_sa, drop_non_congress=False,
    keep_columns=['label', 'id', 'party_label'],
    label_RD=True, extra_manual_labeling=True):
    """
    Performs processing on speaker attribute file to extract informations
    that are useful to us.

    Parameters:
     - df_sa: speaker_attribute DataFrame
     - drop_non_congress: Drops people who aren't part of congress if True.
     (Default: False)
     - keep_columns: [list or none] Keeps the selected columns in the returned
     speaker_attribute DataFrame.
     If None doesn't drop any columns.
     (Default: ['label', 'id', 'party_label', 'US_congress_bio_ID'])

    Returns:
        speaker_attribute Data frame labeled by party
    """

    # Uses wikidata qid to assign a 1 letter party code to each party
    # (see function below). A similar function could be used for UK political
    # parties
    def label_party_usa(parties):
        REPUBLICAN_QID = 'Q29468'
        DEMOCRAT_QID = 'Q29552'

        if REPUBLICAN_QID in parties and DEMOCRAT_QID in parties:
            # Customizable behaviour if part of 2 parties
            if label_RD:
                return 'RD'
            else:
                return None
        elif REPUBLICAN_QID in parties:
            return 'R'
        elif DEMOCRAT_QID in parties:
            return 'D'
        else:
            return None

    def only_politician(occupation):
        POLITICIAN = 'Q82955'
        result = False
        if occupation is not None:
            if POLITICIAN in occupation:
                result = True
        return result

    def sa_label_parties(df_sa):
        # Filter out anyone who doesn't have any party assigned to them
        df_has_party = df_sa[df_sa['party'].notna()].copy()

        # Use function label_party to assign single letter party code to each row
        df_has_party['party_label'] = df_has_party['party'].map(label_party_usa)

        # Drop non politician quotes
        df_has_party = df_has_party[df_has_party.apply(lambda x: only_politician(x.occupation), axis=1)]

        # Drop any person that didn't get attributed a party_label
        df_has_party.dropna(subset=['party_label'], inplace=True)

        return df_has_party

    #-------------------------------------------------------------------------

    df_sa = df_sa[['id', 'label', 'party', 'occupation']]

    # If desired drop people who weren't ever part of congress
    # (have no US_congress_bio_ID).
    if drop_non_congress:
        df_sa.dropna(subset=['US_congress_bio_ID'], inplace=True)

    # Label people by party
    df_sa = sa_label_parties(df_sa)

    if extra_manual_labeling:
        manually_label_party(df_sa, id_inf_D, 'D')
        manually_label_party(df_sa, id_inf_R, 'R')

    df_sa.dropna(subset=['label'], inplace=True)
    # df_sa['label'] = df_sa['label'].map(lambda x: x.lower())

    # Drop unecessary columns from the data
    if keep_columns != None:
        df_sa = df_sa[keep_columns]

    return df_sa

#=============================================================================
# Quote labeling

def merge_quotes_to_speakers(df_quotes, df_sa_labeled):

    def quotes_qid_cleanup(df_quotes, qid_strategy='manual'):
        """
        Internal function. Drops quotes which don't have a qid assigned
        to them and picks the best qid (if there are several, heuristically)
        to associate to that quote.

        qid_strategy: (default) 'pick_first', 'manual' or 'heuristic'
        """

        # Drop quotes which don't have any qid (no speaker attributed)
        df_res = df_quotes[df_quotes['qids'].map(lambda x: len(x)) > 0].copy()


        if qid_strategy == 'pick_first':
            # Pick 1st qid in qid list
            df_res['top_qid'] = df_res['qids'].map(lambda x: x[0])

        elif qid_strategy == 'manual':
            # Drop any quotes that have multiple qids attributed
            # Except for manually configured speakers
            df_res = select_best_qids_manual(df_res)

        elif qid_strategy == 'heuristic':
            select_best_qids_heuristical_inplace(df_res)

        else:
            raise ValueError(f'Passed bad qid_strategy: {qid_strategy}')

        # Drop qids since we only need top_qid from now.
        df_res.drop('qids', axis=1, inplace=True)

        return df_res

    def merge(df_quotes, df_sa_labeled):
        df_merged = df_quotes.merge(df_sa_labeled, left_on='top_qid', right_on='id')

        #Drop top_qid and label since qid and speaker contain the same info
        df_merged['speaker'] = df_merged['label']
        df_merged.drop(['top_qid', 'label'], axis=1, inplace=True)
        return df_merged

    return merge(quotes_qid_cleanup(df_quotes), df_sa_labeled)


#=============================================================================


def manually_label_party(df_sa, qids, party_label):
    df_sa.loc[df_sa.id.map(lambda x: x in qids), 'party_label'] = party_label


def select_best_qids_manual(df):
    def intersection(lst1, lst2):
        return list(set(lst1) & set(lst2))

    df_res = df

    # Drop any quotes that has multiple qid attributed to it
    df_qid_lengths = df_res['qids'].map(lambda x: len(x))
    df_res = df_res[df_qid_lengths == 1]

    df_res['top_qid'] = df_res['qids'].map(lambda x: x[0])

    # Now we manually select the qid of famous politicians
    df_multiqids = df.loc[~df.index.isin(df_res.index)]

    # Now we take the top_qid corresponding the the qid of someone in our manually
    # defined lists
    id_inf = id_inf_R + id_inf_D
    df_manually_selected = df_multiqids.loc[df_multiqids.qids.map(lambda qids: len(intersection(qids, id_inf)) == 1)].copy()
    df_manually_selected['top_qid'] = df_manually_selected.qids.map(lambda qids: intersection(qids, id_inf)[0])

    # Now we concatenate all speakers who only had 1 qid and those
    # where we manually selected the best qid.
    df_res = pd.concat([df_res, df_manually_selected])
    return df_res


def select_best_qids_heuristical_inplace(df):
    def select_best_qid(qids:list):

        # Directly return qid if only 1 qid
        if len(qids) == 1:
            return qids[0]

        # We noticed that shorter qids usually imply greater popularity of
        # an individual. Thus, we take the shortest qid.
        # However, if the shortest and 2nd shortest qid are same length discard.
        qids_n_lengths = list(map(lambda x: (x, len(x)), qids))
        qids_n_lengths = sorted(qids_n_lengths, key=lambda x: x[1])

        shortest_qid_n_length = qids_n_lengths[0]
        second_shortest_qid_n_length = qids_n_lengths[1]
        if shortest_qid_n_length[1] == second_shortest_qid_n_length[1]:
            return None

        return shortest_qid_n_length[0]

    df['top_qid'] = df['qids'].map(select_best_qid)
    df.dropna(subset=['top_qid'], inplace=True)
