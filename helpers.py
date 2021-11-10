
#=============================================================================
# Raw/given data files

# DATA_FOLDER = 'data/'
DATA_FOLDER = 'data.nosync/'
QUOTEBANK_FOLDER = DATA_FOLDER + 'quotebank/'

QUOTES_2020_PATH = QUOTEBANK_FOLDER + 'quotes-2020.json.bz2'
QUOTES_2019_PATH = QUOTEBANK_FOLDER + 'quotes-2019.json.bz2'
QUOTES_2018_PATH = QUOTEBANK_FOLDER + 'quotes-2018.json.bz2'
QUOTES_2017_PATH = QUOTEBANK_FOLDER + 'quotes-2017.json.bz2'
QUOTES_2016_PATH = QUOTEBANK_FOLDER + 'quotes-2016.json.bz2'
QUOTES_2015_PATH = QUOTEBANK_FOLDER + 'quotes-2015.json.bz2'

WIKIDATA_FOLDER = DATA_FOLDER + 'wikidata/'

SPEAKER_ATTRIBUTES_PATH = WIKIDATA_FOLDER + 'speaker_attributes.parquet/'

#=============================================================================
# Small/mini versions of files for easily inspecting them

# Folder is meant to contain small snapshots of data files
DATA_MINI_FOLDER = 'data_mini/'
QUOTES_2020_PARTY_LABELED_MINI_PATH = DATA_MINI_FOLDER + 'quotes-2020-party_labeled_mini.json'
QUOTES_2020_PARTY_LABELED_SMALL_PATH = DATA_MINI_FOLDER + 'quotes-2020-party_labeled_small.json.bz2'

#=============================================================================
# Preprocessed files

PREPROCESSED_FOLDER = DATA_FOLDER + 'processed/'

QUOTES_2020_PARTY_LABELED_CONGRESS_ONLY_PATH = PREPROCESSED_FOLDER + 'quotes-2020-party_labeled_congress_only.json.bz2'
QUOTES_2020_PARTY_LABELED_CONGRESS_ONLY_CLEANED_PATH = PREPROCESSED_FOLDER + 'quotes-2020-party_labeled_congress_only_cleaned.json.bz2'
QUOTES_2020_PARTY_LABELED_CONGRESS_ONLY_TFIDF_PATH = PREPROCESSED_FOLDER + 'quotes-2020-party_labeled_congress_only_tfidf.json.bz2'

#=============================================================================

# import bz2
# import json

# import pandas as pd

# import texthero as hero

import texthero.preprocessing as hp

from helpers import *


def clean(series):
    series = hp.fillna(series)
    series = hp.lowercase(series)
    series = hp.remove_digits(series)
    series = hp.remove_punctuation(series)
    series = hp.remove_diacritics(series)
    series = hp.remove_stopwords(series)
    series = hp.remove_whitespace(series)
    return series
