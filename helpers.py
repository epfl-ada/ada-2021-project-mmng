
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
# QUOTES_2020_PARTY_LABELED_MINI_PATH = DATA_MINI_FOLDER + 'quotes-2020-party_labeled_mini.json'
# QUOTES_2020_PARTY_LABELED_SMALL_PATH = DATA_MINI_FOLDER + 'quotes-2020-party_labeled_small.json.bz2'

#=============================================================================
# Preprocessed files

DATA_FOLDER = 'data.nosync/' #DATA_MINI_FOLDER

PREPROCESSED_FOLDER = DATA_FOLDER + 'processed/'

#-----------------------------------------------------------------------------
# New file sets

# File for final version of labeled and cleaned data WIP
QUOTES_LABELED_CLEANED_PATH = PREPROCESSED_FOLDER + 'quotes_labeled_cleaned.json.bz2'

# File containing 5 different variants of preprocessing. (To be used to find best level of preprosessing on 2020 quotes)
QUOTES_2020_LABELED_CLEANED_VARIANTS = PREPROCESSED_FOLDER + 'quotes-2020-labeled_cleaned_variants.json.bz2'
QUOTES_2020_LABELED_CLEANED_VARIANTS_MINI = PREPROCESSED_FOLDER + 'quotes-2020-labeled_cleaned_variants_mini.json.bz2'

#-----------------------------------------------------------------------------

QUOTES_ALL_TIME_PROCESSED = PREPROCESSED_FOLDER + 'fulldataset_fullypreprocessed.json.bz2'

GLOVE_EMBEDDING_FOLDER = DATA_FOLDER +'glove/'
GLOVE_EMBEDDING_TWITTER = DATA_FOLDER + 'glove_twitter/'

GLOVE_300D = GLOVE_EMBEDDING_FOLDER + 'glove.6B.300d.txt'
GLOVE_50D = GLOVE_EMBEDDING_FOLDER + 'glove.6B.50d.txt'
GLOVE_100D = GLOVE_EMBEDDING_FOLDER + 'glove.6B.100d.txt'
GLOVE_200D = GLOVE_EMBEDDING_FOLDER + 'glove.6B.200d.txt'
GLOVE_840_300D = GLOVE_EMBEDDING_FOLDER + 'glove.840B.300d.txt'

GLOVE_TWITTER_25D = GLOVE_EMBEDDING_TWITTER + 'glove.twitter.27B.25d.txt'
GLOVE_TWITTER_50D = GLOVE_EMBEDDING_TWITTER + 'glove.twitter.27B.50d.txt'
GLOVE_TWITTER_100D = GLOVE_EMBEDDING_TWITTER + 'glove.twitter.27B.100d.txt'
GLOVE_TWITTER_200D = GLOVE_EMBEDDING_TWITTER + 'glove.twitter.27B.200d.txt'

QUOTES_PARTY_LABELED_CLEANED_PATH = PREPROCESSED_FOLDER + 'quotes_party_labeled_cleaned.json.bz2'

QUOTES_2020_PARTY_LABELED_PATH = PREPROCESSED_FOLDER + 'quotes-2020-party_labeled.json.bz2'
QUOTES_2020_PARTY_LABELED_CLEANED_PATH = PREPROCESSED_FOLDER + 'quotes-2020-party_labeled_cleaned.json.bz2'

# This should be a subset of our fully preprocessed data
QUOTES_2020_PARTY_LABELED_CLEANED_DROPSIM_PATH = PREPROCESSED_FOLDER + 'quotes-2020-party_labeled_cleaned_dropsim.json.bz2'

# Not really used anymore
QUOTES_2020_PARTY_LABELED_CONGRESS_ONLY_PATH = PREPROCESSED_FOLDER + 'quotes-2020-party_labeled_congress_only.json.bz2'
QUOTES_2020_PARTY_LABELED_CONGRESS_ONLY_CLEANED_PATH = PREPROCESSED_FOLDER + 'quotes-2020-party_labeled_congress_only_cleaned.json.bz2'
QUOTES_2020_PARTY_LABELED_CONGRESS_ONLY_TFIDF_PATH = PREPROCESSED_FOLDER + 'quotes-2020-party_labeled_congress_only_tfidf.json.bz2'
QUOTES_2020_PARTY_LABELED_COMPLETE =  PREPROCESSED_FOLDER + 'quotes-2020-party_labeled_all_cols.json.bz2'
QUOTES_2020_PARTY_LABELED_NO_DUPLICATES = PREPROCESSED_FOLDER + 'quotes-2020-party_no_duplicates.json.bz2'
QUOTES_2020_PARTY_LABELED_WITH_STOP_WORDS = PREPROCESSED_FOLDER +  'keep_stop_words.json.bz2'

QUOTES_2020_EMBEDDED_TWITTER = PREPROCESSED_FOLDER + 'glove_encoded_df.json.bz2'

QUOTES_2020_FOR_BERT = PREPROCESSED_FOLDER + 'bert_preprocessing_keep_lower_case.json.bz2'
#=============================================================================

# Fixing paths for different os's
import os
def fixpath(path):
    return os.path.abspath(os.path.expanduser(path))


#=============================================================================
