
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

QUOTES_PARTY_LABELED_CLEANED_PATH = PREPROCESSED_FOLDER + 'quotes_party_labeled_cleaned.json.bz2'

QUOTES_2020_PARTY_LABELED_PATH = PREPROCESSED_FOLDER + 'quotes-2020-party_labeled.json.bz2'
QUOTES_2020_PARTY_LABELED_CLEANED_PATH = PREPROCESSED_FOLDER + 'quotes-2020-party_labeled_cleaned.json.bz2'

QUOTES_2020_PARTY_LABELED_CONGRESS_ONLY_PATH = PREPROCESSED_FOLDER + 'quotes-2020-party_labeled_congress_only.json.bz2'
QUOTES_2020_PARTY_LABELED_CONGRESS_ONLY_CLEANED_PATH = PREPROCESSED_FOLDER + 'quotes-2020-party_labeled_congress_only_cleaned.json.bz2'
QUOTES_2020_PARTY_LABELED_CONGRESS_ONLY_TFIDF_PATH = PREPROCESSED_FOLDER + 'quotes-2020-party_labeled_congress_only_tfidf.json.bz2'
QUOTES_2020_PARTY_LABELED_COMPLETE =  PREPROCESSED_FOLDER + 'quotes-2020-party_labeled_all_cols.json.bz2'

#=============================================================================

# Fixing paths for different os's
import os
def fixpath(path):
    return os.path.abspath(os.path.expanduser(path))


#=============================================================================
