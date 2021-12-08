from helpers import *
from drop_similar_quotes import *
import pandas as pd
import bz2
import numpy as np
import sys

files_to_embed = [QUOTES_2020_PARTY_LABELED_WITH_STOP_WORDS]
write_filename = PREPROCESSED_FOLDER + 'glove_encoded_df.json.bz2'

GLOVE_EMBEDDING = GLOVE_50D
dimensions = 50
max_sentence_length = 100

def load_glove_model(File,dimensions):
    """function that loads the embedded dictionary"""
    #dimensions is the dimension of the embedder

    print("Loading Glove Model")
    glove_model = {}
    line_nb = 0
    with open(File,'r') as f:
        for line in f:
            split_line = line.split()
            word = ' '.join(split_line[:len(split_line)-dimensions])
            embedding = np.array(split_line[(len(split_line)-dimensions):], dtype=np.float64)
            glove_model[word] = embedding
            line_nb +=1
    print(f"{len(glove_model)} words loaded!")
    return glove_model

def embed_quote(sentence,dimensions):
    def assign_vect(word):
        if 'covid' in word:
            return np.expand_dims(glve['virus'],axis = 0)
        elif 'trump' in word:
            return np.expand_dims(glve['trump'], axis = 0)
        elif word not in glve.keys():
            return np.expand_dims(np.zeros(dimensions),axis = 0)
        else:
            return np.expand_dims(glve[word],axis = 0)
    words = sentence.split()
    arr = np.concatenate(list(map(lambda word: assign_vect(word),words)),axis =  0)
    return arr


if __name__ == "__main__":
    #loads the embedder dictionary
    glve = load_glove_model(GLOVE_EMBEDDING,dimensions)

    #write results to file
    with bz2.open(write_filename, 'wb') as d_file:
        for file in files_to_embed:
            print('------------------------------------------------------------------')
            print('Processing file: ' + file)

            i=0
            print('Chunks done: ',end='')
            with pd.read_json(file, lines=True, compression='bz2', chunksize=10000) as df_reader:
                for df_quotes_chunk in df_reader:
                    df = df_quotes_chunk

                    df['quotation_length'] = df['quotation'].apply(lambda x: len(x))
                    df = df[df['quotation_length'] <=  max_sentence_length]
                    df = df[df['quotation_length'] > 0]

                    df['glove_embedding'] = df['quotation'].apply(lambda x: embed_quote(x,dimensions))
                    df['party_number'] = df['party_label'].apply(lambda x: 1 if x == 'R' else 0)

                    df[['quotation','speaker','party_number','glove_embedding']].to_json(d_file, orient='records', lines=True)

                    print(i, end='  ')
                    i+=1

                    sys.stdout.flush()
            print('\n------------------------------------------------------------------')
