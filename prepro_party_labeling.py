
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
    keep_columns=['label', 'id', 'party_label', 'US_congress_bio_ID']):
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

    # If desired drop people who weren't ever part of congress
    # (have no US_congress_bio_ID).
    if drop_non_congress:
        df_sa.dropna(subset=['US_congress_bio_ID'], inplace=True)


    # Uses wikidata qid to assign a 1 letter party code to each party
    # (see function below). A similar function could be used for UK political
    # parties
    def label_party_usa(parties):
        REPUBLICAN_QID = 'Q29468'
        DEMOCRAT_QID = 'Q29552'


        # TODO Possible improvement have a more advanced rule for when a person
        # is affiliatied to both parties.
        if REPUBLICAN_QID in parties and DEMOCRAT_QID in parties:
            return None
            # return 'RD'
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

    def sa_label_parties(df_sa, labeler):
        # Filter out anyone who doesn't have any party assigned to them
        df_has_party = df_sa[df_sa['party'].notna()].copy()

        # Use function label_party to assign single letter party code to each row
        df_has_party['party_label'] = df_has_party['party'].map(label_party_usa)

        # Drop non politician quotes
        df_has_party = df_has_party[df_has_party.apply(lambda x: only_politician(x.occupation), axis=1)]

        # Drop any person that didn't get attributed a party_label
        df_has_party.dropna(subset=['party_label'], inplace=True)

        return df_has_party

    # Label people by party
    df_sa = sa_label_parties(df_sa, label_party_usa)

    # Drop unecessary columns from the data
    if keep_columns != None:
        df_sa = df_sa[keep_columns]

    return df_sa

#=============================================================================
# Quote labeling

def merge_quotes_to_speakers(df_quotes, df_sa_labeled):

    def quotes_qid_cleanup(df_quotes):
        """
        Internal function. Drops quotes which don't have a qid assigned
        to them and picks the best qid (if there are several, heuristically)
        to associate to that quote.
        """

        # Drop tables which don't have any qid (no speaker attributed)
        df_has_qids = df_quotes[df_quotes['qids'].map(lambda x: len(x)) > 0].copy()

        # Pick 1st qid in qid list
        df_has_qids['top_qid'] = df_has_qids['qids'].map(lambda x: x[0])

        # Drop qids since we only need top_qid from now.
        df_has_qids.drop('qids', axis=1, inplace=True)

        return df_has_qids

    def merge(df_quotes, df_sa_labeled):
        df_merged = df_quotes.merge(df_sa_labeled, left_on='top_qid', right_on='id')

        #Drop top_qid and label since qid and speaker contain the same info
        df_merged.drop(['top_qid', 'label'], axis=1, inplace=True)
        return df_merged

    return merge(quotes_qid_cleanup(df_quotes), df_sa_labeled)


#=============================================================================
