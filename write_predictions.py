import bz2
import json
import sys
import pandas as pd

import pickle
from helpers import *

#Input file without predictions
input_file  = PREPROCESSED_FOLDER + 'quotes_rd_labeled_cleaned.json.bz2'

#Output file where we add predictions
output_file = PREPROCESSED_FOLDER + 'quotes_labeled_cleaned_predicted.json.bz2'

#Given quotes score them using a model
def predict(quotes):
    y_proba = clf_loaded.predict_proba(vectorizer_loaded.transform(quotes))
    return y_proba[:,1]

#Load the pretrained model
with open(TEMP_FOLDER + 'model-tfidf_ngram=(1,3)-multinomialnb.pkl', 'rb') as file:
    clf_loaded = pickle.load(file)
    
#Load the vectorizer to vectorize quotes before feeding them to the model
with open(TEMP_FOLDER + 'vectorizer_ngram=(1,3)-multinomialnb.pkl', 'rb') as file:
    vectorizer_loaded = pickle.load(file)
    

#Read input file, vectorize and predict, write inputs and prediction to the output file. (in chunks)
i = 0
with bz2.open(output_file, 'wb') as d_file:
    with pd.read_json(input_file, lines=True, orient='records', compression='bz2', chunksize=100000) as df_reader:
        for df_quotes_chunk in df_reader:
            df_quotes_chunk['prob_dem'] = predict(df_quotes_chunk.quotation_clean)
            df_quotes_chunk.to_json(d_file, orient='records', lines=True)

            # Print progress
            print(i, end='  ')
            sys.stdout.flush()
            i += 1