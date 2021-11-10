import bz2
import json

import pandas as pd

from helpers import *


#=============================================================================
# Speaker Attribute Processing

df_sa = pd.read_parquet(SPEAKER_ATTRIBUTES_PATH)

# Only keep congress memebers (OPTIONAL, can be commented)
# df_sa.dropna(subset=['US_congress_bio_ID'], inplace=True)



REPUBLICAN_QID = 'Q29468'
DEMOCRAT_QID = 'Q29552'

def sa_label_parties(df_sa):

    def label_party(parties):
        # TODO Figure out what to do if a person in a member of multiple parties at the same time
        if REPUBLICAN_QID in parties and DEMOCRAT_QID in parties:
            return None
        elif REPUBLICAN_QID in parties:
            return 'R'
        elif DEMOCRAT_QID in parties:
            return 'D'
        else:
            return None

    df_has_party = df_sa[df_sa['party'].notna()].copy()

    # Use function label_party to assign single letter party code to each row
    df_has_party['party_label'] = df_has_party['party'].map(label_party)

    # Drop any person that didn't get attributed a party_label
    df_has_party.dropna(subset=['party_label'], inplace=True)

    return df_has_party


def sa_keep_useful_stuff(df_sa):
    return df_sa[['label', 'id', 'party_label', 'US_congress_bio_ID']]


df_sa_party_labeled = sa_keep_useful_stuff(sa_label_parties(df_sa))
# This DataFrame contains name, qid, party_label for each person/congress member.
# name=label, qid=id, party_label=party_label


#=============================================================================
# File manipulation

def quotes_clean(df_quotes):
    df_quotes = df_quotes.drop('phase', axis=1).drop('urls', axis=1).drop('probas', axis=1)

    # Drop tables which don't have any qid
    df_has_qids = df_quotes[df_quotes['qids'].map(lambda x: len(x)) > 0].copy()

    # Pick 1st qid in qid list
    df_has_qids['top_qid'] = df_has_qids['qids'].map(lambda x: x[0])

    df_has_qids.drop('qids', axis=1, inplace=True)

    return df_has_qids

# df_quotes_clean = quotes_clean(df_quotes)

i=0

with pd.read_json(QUOTES_2020_PATH, lines=True, compression='bz2', chunksize=100000) as df_reader:
    # with open(QUOTES_2020_PARTY_LABELED_MINI_PATH, 'wb') as d_file:
    # with bz2.open(QUOTES_2020_PARTY_LABELED_SMALL_PATH, 'wb') as d_file:
    # with bz2.open(QUOTES_2020_PARTY_LABELED_CONGRESS_ONLY_PATH, 'wb') as d_file:
    with bz2.open(QUOTES_2020_PARTY_LABELED_PATH, 'wb') as d_file:
        for df_quotes_chunk in df_reader:
            print(i)

            df_quotes_clean_chunk = quotes_clean(df_quotes_chunk)

            df_merged_chunk = df_quotes_clean_chunk.merge(df_sa_party_labeled, left_on='top_qid', right_on='id').drop(['top_qid', 'label'], axis=1)
            df_merged_chunk.to_json(d_file, orient='records', lines=True)

            i += 1
            # if i >= 10:
            #     break


# print(chunk)
