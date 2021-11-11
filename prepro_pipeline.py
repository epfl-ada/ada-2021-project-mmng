
import bz2
import json

import pandas as pd

import texthero as hero

import texthero.preprocessing as hp

from helpers import *
from prepro_party_labeling import *

#=============================================================================
# RUN PARAMETERS
# Tweakable setting to control our pipeline

# Input files
raw_data_filepaths = [QUOTES_2020_PATH]

# raw_data_filepaths = [
#     QUOTES_2015_PATH,
#     QUOTES_2016_PATH,
#     QUOTES_2017_PATH,
#     QUOTES_2018_PATH,
#     QUOTES_2019_PATH,
#     QUOTES_2020_PATH
#     ]


# Output files
cleaned_labeled_filepath = QUOTES_2020_PARTY_LABELED_CLEANED_PATH
# cleaned_labeled_filepath = QUOTES_PARTY_LABELED_CLEANED_PATH

#-----------------------------------------------------------------------------
# Pipeline control

LABEL_PARTY = True      # labeling by merging with wikidata dump
CLEAN_QUOTES = True     # clean quotes using clean function below
CLEAN_SPEAKER = True    # clean speaker name (by applying str.lower())

#=============================================================================
# Preprocessing functions

def clean(series):
    series = hp.fillna(series)
    series = hp.lowercase(series)
    series = hp.remove_digits(series)
    series = hp.remove_punctuation(series)
    series = hp.remove_diacritics(series)
    series = hp.remove_stopwords(series)
    series = hp.remove_whitespace(series)
    return series


#=============================================================================
# Preprocessing Pipeline!

print('==================================================================')
print(' Starting data preprocessing')

print('------------------------------------------------------------------')
print(' Loading and preparing wikidata dump (10s-60s)')
df_sa = load_wikidata()
df_sa_labeled = speaker_attribute_processing(df_sa)
print('DONE')
print()

print('==================================================================')
print(' Starting file preprocessing')
print(' \tWriting outputs to: ' + cleaned_labeled_filepath)

# Open output file
with bz2.open(cleaned_labeled_filepath, 'wb') as d_file:
    for raw_data_filepath in raw_data_filepaths:
        print('------------------------------------------------------------------')
        print('Processing file: ' + raw_data_filepath)

        i=0
        print('Chunks done: ',end='')

        # Batched file processing
        with pd.read_json(raw_data_filepath, lines=True, compression='bz2', chunksize=100000) as df_reader:
            for df_quotes_chunk in df_reader:

                df = df_quotes_chunk.drop(['phase', 'urls', 'probas'], axis=1)

                # Merge quotes to speakers to get party labels
                if LABEL_PARTY:
                    df = merge_quotes_to_speakers(df, df_sa_labeled)

                # Cleaning quotations
                if CLEAN_QUOTES:
                    df['quotation'] = clean(df['quotation'])

                # Cleaning speaker name
                if CLEAN_SPEAKER:
                    df['speaker'] = df['speaker'].apply(lambda x: x.lower())

                # write to output
                df.to_json(d_file, orient='records', lines=True)

                # Print progress
                print(i, end='  ')
                i += 1
                # if i >= 10: # Uncomment to not run on full file
                #     break

        print('\n------------------------------------------------------------------')
