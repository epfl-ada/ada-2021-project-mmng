import bz2
import json

import pandas as pd

import texthero as hero

import texthero.preprocessing as hp

from helpers import *


i=0
with pd.read_json(QUOTES_2020_PARTY_LABELED_PATH, lines=True, compression='bz2', chunksize=100000) as df_reader:
    with bz2.open(QUOTES_2020_PARTY_LABELED_CLEANED_PATH, 'wb') as d_file:
        for df_quotes_chunk in df_reader:

            print(i)

            df = df_quotes_chunk
            df['quotation'] = clean(df['quotation'])

            df.to_json(d_file, orient='records', lines=True)

            i += 1
            # if i >= 10:
            #     break
