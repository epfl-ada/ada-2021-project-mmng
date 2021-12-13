
import sys

import bz2
import json

import pandas as pd

import texthero.preprocessing as hp

from helpers import *
from prepro_party_labeling import *


from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize

#=============================================================================
# RUN PARAMETERS
# Tweakable setting to control our pipeline

# Input files
# input_files = [QUOTES_2020_PATH]
input_files = [
    QUOTES_2015_PATH,
    QUOTES_2016_PATH,
    QUOTES_2017_PATH,
    QUOTES_2018_PATH,
    QUOTES_2019_PATH,
    QUOTES_2020_PATH
    ]


# Output files
# output_file = QUOTES_2020_LABELED
# output_file = QUOTES_LABELED

#-----------------------------------------------------------------------------
# Pipeline control

# LABEL_PARTY = True      # labeling by merging with wikidata dump
# CLEAN_QUOTES = False     # clean quotes using clean function below
# CLEAN_SPEAKER = True    # clean speaker name (by applying str.lower())

#=============================================================================
# Preprocessing functions

def cleanA(series):
    series = hp.fillna(series)
    # series = hp.lowercase(series)
    series = hp.remove_digits(series)
    # series = hp.remove_punctuation(series)
    series = hp.remove_diacritics(series)
    # series = hp.remove_stopwords(series)
    series = hp.remove_whitespace(series)
    return series

def cleanB(series):
    series = hp.fillna(series)
    series = hp.lowercase(series)
    series = hp.remove_digits(series)
    series = hp.remove_punctuation(series)
    series = hp.remove_diacritics(series)
    # series = hp.remove_stopwords(series)
    series = hp.remove_whitespace(series)
    return series

def cleanC(series):
    series = hp.fillna(series)
    series = hp.lowercase(series)
    series = hp.remove_digits(series)
    series = hp.remove_punctuation(series)
    series = hp.remove_diacritics(series)
    series = hp.remove_stopwords(series)
    series = hp.remove_whitespace(series)
    return series

def cleanD(series):
    series = hp.fillna(series)
    series = hp.lowercase(series)
    series = hp.remove_digits(series)
    series = hp.remove_punctuation(series)
    series = hp.remove_diacritics(series)
    series = hp.remove_stopwords(series)
    series = hp.remove_whitespace(series)
    series = hp.stem(series)
    return series


lemmatizer = WordNetLemmatizer()

def cleanE(series):
    series = hp.fillna(series)
    series = hp.lowercase(series)
    series = hp.remove_digits(series)
    series = hp.remove_punctuation(series)
    series = hp.remove_diacritics(series)
    series = hp.remove_stopwords(series)
    series = hp.remove_whitespace(series)

    series = series.map(lambda quote: ' '.join(list(map(lambda x:lemmatizer.lemmatize(x), word_tokenize(quote)))))

    return series


clean = cleanE

cleaning_functions = [
    cleanA,
    cleanB,
    cleanC,
    cleanD,
    cleanE,
]

#=============================================================================
# Preprocessing Pipeline!

def _run_pipeline(input_paths:list, output_path:str, label_party:bool,
    clean_speaker:bool, clean_quotes:bool, cleaning_mode:int='simple',
    drop_cols:list=[], chunks:int=-1, chunksize:int=100_000):
    """
    input_paths   : Input file(s) to read. Can be a single filepath or a list
                    of filepaths. If a list is provided will read them
                    1 by one and output into a single file.
    output_path   : Output file to write.
    label_party   : Controls if party labeling should be used
    clean_speaker : Controls if speaker_name should be lowercased
    clean_quotes  : Controls if quotes should be cleaned
    cleaning_mode : 'simple' apply clean.
                    'multi' apply all cleaning functions
    drop_cols     : List of columns to drop
    chunks        : Number of chunks to execute before stopping. (Default)
                    -1 to run until end of file.
    chunksize     : chunksize
    """

    if type(input_paths) == str:
        input_paths = [input_paths]

    if label_party:
        print('------------------------------------------------------------------')
        print(' Loading and preparing wikidata dump (10s-60s)')
        df_sa = load_wikidata()
        df_sa_labeled = speaker_attribute_processing(df_sa)
        print('DONE')
        print()

    print('------------------------------------------------------------------')
    print(' Starting file preprocessing')
    print(' \tWriting outputs to: ' + output_path)

    # Open output file
    with bz2.open(output_path, 'wb') as output_file:
        for input_path in input_paths:
            print('------------------------------------------------------------------')
            print('Processing file: ' + input_path)

            i=0
            print('Chunks done: ',end='')

            # Batched file processing
            with pd.read_json(input_path, lines=True, compression='bz2', chunksize=chunksize) as df_reader:
                for df_quotes_chunk in df_reader:

                    # Drop specified columns
                    df = df_quotes_chunk.drop(drop_cols, axis=1)

                    # Merge quotes to speakers to get party labels
                    if label_party:
                        df = merge_quotes_to_speakers(df, df_sa_labeled)

                    # Cleaning quotations
                    if clean_quotes:
                        if cleaning_mode == 'simple':
                            df['quotation_clean'] = clean(df['quotation'])
                        elif cleaning_mode == 'multi':
                            for clean_func in cleaning_functions:
                               df[f'quotation_{clean_func.__name__}'] = clean_func(df['quotation'])
                        else:
                            raise ValueError('Invalid cleaning_mode')

                    # Cleaning speaker name
                    if clean_speaker:
                        df['speaker'] = df['speaker'].apply(lambda x: x.lower())

                    # write to output
                    df.to_json(output_file, orient='records', lines=True)

                    # Print progress
                    print(i, end='  ')
                    sys.stdout.flush()
                    i += 1
                    if chunks != -1 and i > chunks: # Uncomment to not run on full file
                        break

            print('\n------------------------------------------------------------------')


def run_party_labeling(input_paths, output_path, drop_cols=['phase', 'urls', 'probas'], chunks:int=-1, chunksize:int=100_000):
    print('==================================================================')
    print(' Starting party_labeling')

    _run_pipeline(input_paths, output_path, label_party=True, clean_speaker=True, clean_quotes=False, drop_cols=drop_cols, chunks=chunks, chunksize=chunksize)

def _run_cleaning(input_path, output_path, cleaning_mode, drop_cols=[], chunks:int=-1, chunksize:int=100_000):
    print('==================================================================')
    print(f' Starting cleaning. mode={cleaning_mode}')
    _run_pipeline(input_path, output_path, label_party=False, clean_speaker=False, clean_quotes=True, cleaning_mode=cleaning_mode, drop_cols=drop_cols, chunks=chunks, chunksize=chunksize)

def run_cleaning(input_path, output_path, drop_cols=[], chunks:int=-1, chunksize:int=100_000):
    _run_cleaning(input_path, output_path, cleaning_mode='simple', drop_cols=drop_cols, chunks=chunks, chunksize=chunksize)

def run_cleaning_multi(input_path, output_path, drop_cols=[], chunks:int=-1, chunksize:int=100_000):
    _run_cleaning(input_path, output_path, cleaning_mode='multi', drop_cols=drop_cols, chunks=chunks, chunksize=chunksize)
