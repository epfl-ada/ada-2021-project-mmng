
from helpers import *
from prepro_pipeline import *

# Uncomment all code to run all the required preprocessing
#-----------------------------------------------------------------------------
# Part 1: Party labeling

# Run
run_party_labeling(QUOTES_2020_PATH, QUOTES_2020_LABELED)
# run_party_labeling(QUOTEBANK_PATHS, QUOTES_LABELED)

#-----------------------------------------------------------------------------
# Part 2: Cleaning

run_cleaning(QUOTES_2020_LABELED, QUOTES_2020_LABELED_CLEANED)
# run_cleaning(QUOTES_LABELED, QUOTES_LABELED_CLEANED)

# Part 2b: Different variants of cleaning
run_cleaning_multi(QUOTES_2020_LABELED, QUOTES_2020_LABELED_CLEANED_VARIANTS)

