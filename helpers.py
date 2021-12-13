
import os
import pandas as pd
import pickle

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

QUOTEBANK_PATHS = [
    QUOTES_2015_PATH,
    QUOTES_2016_PATH,
    QUOTES_2017_PATH,
    QUOTES_2018_PATH,
    QUOTES_2019_PATH,
    QUOTES_2020_PATH
    ]

#-----------------------------------------------------------------------------

WIKIDATA_FOLDER = DATA_FOLDER + 'wikidata/'

SPEAKER_ATTRIBUTES_PATH = WIKIDATA_FOLDER + 'speaker_attributes.parquet/'

#=============================================================================
# Small/mini versions of files for easily inspecting them

# Folder is meant to contain small snapshots of data files
DATA_MINI_FOLDER = 'data_mini/'
# QUOTES_2020_PARTY_LABELED_MINI_PATH = DATA_MINI_FOLDER + 'quotes-2020-party_labeled_mini.json'
# QUOTES_2020_PARTY_LABELED_SMALL_PATH = DATA_MINI_FOLDER + 'quotes-2020-party_labeled_small.json.bz2'

#=============================================================================
# Temporary files

TEMP_FOLDER = 'temp/'
TEMP_FILE = TEMP_FOLDER + 'temp.json.bz2'

#=============================================================================
# Preprocessed files

DATA_FOLDER = 'data.nosync/' #DATA_MINI_FOLDER

PREPROCESSED_FOLDER = DATA_FOLDER + 'processed/'

#-----------------------------------------------------------------------------
# New file sets

QUOTES_LABELED = PREPROCESSED_FOLDER + 'quotes_labeled.json.bz2'
QUOTES_2020_LABELED = PREPROCESSED_FOLDER + 'quotes-2020_labeled.json.bz2'

QUOTES_RD_LABELED = PREPROCESSED_FOLDER + 'quotes_rd_labeled.json.bz2'
QUOTES_2020_RD_LABELED = PREPROCESSED_FOLDER + 'quotes-2020_rd_labeled.json.bz2'

# File for final version of labeled and cleaned data WIP
QUOTES_LABELED_CLEANED = PREPROCESSED_FOLDER + 'quotes_labeled_cleaned.json.bz2'
QUOTES_2020_LABELED_CLEANED = PREPROCESSED_FOLDER + 'quotes-2020_labeled_cleaned.json.bz2'

QUOTES_RD_LABELED_CLEANED = PREPROCESSED_FOLDER + 'quotes_rd_labeled_cleaned.json.bz2'
QUOTES_2020_RD_LABELED_CLEANED = PREPROCESSED_FOLDER + 'quotes-2020_rd_labeled_cleaned.json.bz2'

# File containing 5 different variants of preprocessing. (To be used to find best level of preprosessing on 2020 quotes)
QUOTES_2020_LABELED_CLEANED_VARIANTS = PREPROCESSED_FOLDER + 'quotes-2020-labeled_cleaned_variants.json.bz2'
# QUOTES_2020_LABELED_CLEANED_VARIANTS_MINI = PREPROCESSED_FOLDER + 'quotes-2020-labeled_cleaned_variants_mini.json.bz2'

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
# Trained Models, Vectorizers and Vectorized Quotes

MODELS_FOLDER = DATA_FOLDER + 'models/'

VECTORIZER_NGRAM13 = MODELS_FOLDER + 'vectorizer_tfidf_ngram=(1,3).pkl'
MODEL_MULTINOMIALNB_NGRAM13 = MODELS_FOLDER + 'model_multinomialnb_tfidf_ngram=(1,3).pkl'

#=============================================================================

# Fixing paths for different os's
def fixpath(path):
    return os.path.abspath(os.path.expanduser(path))


#=============================================================================
# Model loading

def load_pickle(path):
    """Load a pickle file. Returns the loaded model/object"""
    with open(path, 'rb') as file:
        return pickle.load(file)


def save_pickle(model, path):
    """Save a model/object into a pickle file"""
    with open(path, 'wb') as file:
        pickle.dump(model, file)


#=============================================================================

def downsample(df:pd.DataFrame, label_col_name:str, force_sample_n=None) -> pd.DataFrame:
    # find the number of observations in the smallest group

    if force_sample_n != None:
        nmin = force_sample_n
    else:
        nmin = df[label_col_name].value_counts().min()
    return (df
            # split the dataframe per group
            .groupby(label_col_name)
            # sample nmin observations from each group
            .apply(lambda x: x.sample(nmin))
            # recombine the dataframes
            .reset_index(drop=True)
            )


def drop_short_quotes(df, threshold_quantile, quote_col_name='quotation_clean'):
    """
    Calculates the length of all given quotes and drops any quotes that are
    shorter than the given threshold quantile/percentile.
    """

    lengths_of_df = df[quote_col_name].apply(lambda x: len(x))
    lengths_of_df.median()

    # Droping quotes
    df = df[lengths_of_df > lengths_of_df.quantile(threshold_quantile)]

    # Code to drop both short and long quotes
    # df = df[np.logical_and(lengths_of_df > lengths_of_df.quantile(0.3), lengths_of_df < lengths_of_df.quantile(0.9))]

    return df


def aggregate_cross_validate_results(res):
    return {item: (value.mean(), value.std()) for (item, value) in res.items()}


def print_cross_validate_results(res):
    # scoring=['accuracy', 'precision', 'recall', 'f1']
    # res = cross_validate(pipeline, X, y, scoring=scoring, cv=3)
    res = aggregate_cross_validate_results(res)

    # Code isn't pretty but prints nice output!
    # print(f'Col: {col}')

    # print(f'X shape: {X.shape}')

    for (key, value) in res.items():
        print(f'\t{key:20} - \tavg: {value[0]:.3f}\tstd: {value[1]:.3f}')
