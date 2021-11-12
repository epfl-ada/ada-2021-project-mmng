
import bz2
import json

import pandas as pd

# import texthero as hero
# import texthero.preprocessing as hp

from helpers import *
from drop_similar_quotes import *


#=============================================================================
# RUN PARAMETERS
# Tweakable setting to control our pipeline

# Input files
input_filepath = QUOTES_2020_PARTY_LABELED_CLEANED_PATH

# Output files
output_filepath = QUOTES_2020_PARTY_LABELED_CLEANED_DROPSIM_PATH

#-----------------------------------------------------------------------------
# Pipeline control

# TODO remove
LABEL_PARTY = True      # labeling by merging with wikidata dump
CLEAN_QUOTES = True     # clean quotes using clean function below
CLEAN_SPEAKER = True    # clean speaker name (by applying str.lower())

#=============================================================================
# Helper functions

#=============================================================================
# 2nd Preprocessing Pipeline: droping similar quotes

