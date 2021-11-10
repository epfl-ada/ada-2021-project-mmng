import bz2
import json

import pandas as pd

import texthero as hero

import texthero.preprocessing as hp

from helpers import *

input_filename = QUOTES_2020_PARTY_LABELED_PATH
output_filename = QUOTES_2020_PARTY_LABELED_CLEANED_PATH

i=0
with pd.read_json(input_filename, lines=True, compression='bz2', chunksize=100000) as df_reader:
    with bz2.open(output_filename, 'wb') as d_file:
        for df_quotes_chunk in df_reader:

            # Counter stuff
            print(i)
            i += 1

            # Cleaning quotations
            df = df_quotes_chunk
            df['quotation'] = clean(df['quotation'])

            # Cleaning other stuff
            df['speaker'] = df['speaker'].apply(lambda x: x.lower())

            # write to output
            df.to_json(d_file, orient='records', lines=True)

            # if i >= 10:
            #     break
