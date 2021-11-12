from helpers import *

from IPython.display import clear_output

import bz2
import json

import pandas as pd

import numpy as np

from pprint import *

import matplotlib.pyplot as plt

def build_stat_dics(path_to_file):
    year = "null"
    years = ['2015','2016','2017','2018','2019','2020']
    for y in years:
        if y in path_to_file:
            year = y
            
    stats = {
        'year': year,
        'count': 0,
        'count_no_speaker':0,
        'quotation': {
            'chars': {
                'min_length': 1000000,
                'max_length': 0,
                'sum_length': 0,
                'length_bins': np.zeros(20000)
                },
            'words': {
                'min_length': 1000000,
                'max_length': 0,
                'sum_length': 0,
                'length_bins': np.zeros(20000)
            },
        }
    }


    i=0
    with pd.read_json(path_to_file, lines=True, compression='bz2', chunksize=100000) as df_reader:
        for chunk in df_reader:
            print(i)

            #--------------------------------------------------------------------

            stats['count'] += chunk.shape[0]

            chunk_quote = chunk['quotation']
            #--------------------------------------------------------------------
            # Compute Quote Character Statistics

            stats_qc = stats['quotation']['chars']

            chunk_lengths = chunk_quote.map(lambda x: len(x))

            chunk_min_length = chunk_lengths.min()
            if stats_qc['min_length'] > chunk_min_length:
                stats_qc['min_length'] = chunk_min_length

            chunk_max_length = chunk_lengths.max()
            if stats_qc['max_length'] < chunk_max_length:
                stats_qc['max_length'] = chunk_max_length

            stats_qc['sum_length'] += chunk_lengths.sum()

            # stats_qc['length_bins'][chunk_lengths]+=np.bincount(chunk_lengths.to_numpy())[chunk_lengths]

            for l in chunk_lengths.to_numpy():
                stats_qc['length_bins'][l] += 1

            #--------------------------------------------------------------------
            # Compute Quote Word Statistics

            stats_qw = stats['quotation']['words']

            chunk_word_lengths = chunk_quote.map(lambda x: len(x.split(" ")))

            chunk_min_length = chunk_word_lengths.min()
            if stats_qw['min_length'] > chunk_min_length:
                stats_qw['min_length'] = chunk_min_length

            chunk_max_length = chunk_word_lengths.max()
            if stats_qw['max_length'] < chunk_max_length:
                stats_qw['max_length'] = chunk_max_length

            stats_qw['sum_length'] += chunk_word_lengths.sum()

            # stats_qw['length_bins'][chunk_word_lengths]+=np.bincount(chunk_word_lengths.to_numpy())[chunk_word_lengths]

            for l in chunk_word_lengths.to_numpy():
                stats_qw['length_bins'][l] += 1

            #--------------------------------------------------------------------
            
            # Compute no speakers count
            stats['count_no_speaker'] += len(chunk[chunk["speaker"] == "None"])
            
            #--------------------------------------------------------------------
            i+=1
            # if i>2:
            #    break

    stats['quotation']['chars']['avg_length'] = round(stats['quotation']['chars']['sum_length'] / stats['count'], 2)
    stats['quotation']['words']['avg_length'] = round(stats['quotation']['words']['sum_length'] / stats['count'], 2)

    # chunk.head()

    clear_output(wait=True)
    print("#Chunks=" + str(i))
    print(stats)
    pprint(stats)
    return stats


def build_total_dict(all_stats):
    #dictionary containing all the stats
    total_stats = {
            'count': 0,
            'count_no_speaker':0,
            'quotation': {
                'words': {
                    'min_length': 1000000,
                    'max_length': 0,
                    'sum_length': 0,
                },
                'chars': {
                    'min_length': 1000000,
                    'max_length': 0,
                    'sum_length': 0,
                    },
            }
        }
    #operations for aggregation
    total_stats['count'] = sum(stats.get('count', 0) for stats in all_stats)
    total_stats['count_no_speaker'] = sum(stats.get('count_no_speaker', 0) for stats in all_stats)
    total_stats['quotation']['words']['min_length'] = min(stats.get('quotation', {}).get('words').get('min_length', 0) for stats in all_stats)
    total_stats['quotation']['words']['max_length'] = max(stats.get('quotation', {}).get('words').get('max_length', 0) for stats in all_stats)
    total_stats['quotation']['words']['sum_length'] = sum(stats.get('quotation', {}).get('words').get('sum_length', 0) for stats in all_stats)
    total_stats['quotation']['words']['avg_length'] = total_stats['quotation']['words']['sum_length']/total_stats['count']
    total_stats['quotation']['chars']['min_length'] = min(stats.get('quotation', {}).get('chars').get('min_length', 0) for stats in all_stats)
    total_stats['quotation']['chars']['max_length'] = max(stats.get('quotation', {}).get('chars').get('max_length', 0) for stats in all_stats)
    total_stats['quotation']['chars']['sum_length'] = sum(stats.get('quotation', {}).get('chars').get('sum_length', 0) for stats in all_stats)
    total_stats['quotation']['chars']['avg_length'] = total_stats['quotation']['chars']['sum_length']/total_stats['count']
    return total_stats