import pandas as pd
import numpy as np


def jaccard_sim(str_pair):
    if type(str_pair) != type(tuple()):
        return 0.0
    a = set(str_pair[0].split(' '))
    b = set(str_pair[1].split(' '))
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


## This function isn't meant to work on chunks of files, however one can work around this (by calling multiple times the function)
def remove_duplicates(dataframe,threshold):
    """removes quotes of speakers that have a jaccard similarity larger than a certain threshold"""
    def clean_row(row):
        """return the list of quotes that are going to be removed for
        one speaker because their jaccard similarity to another quote is
        larger than a certain threshold """
        to_remove = []

        #row is a the list of quotes of a speaker
        for i in range(len(row)):
            #check if we are above the maximum index because we are actively removing
            #quotes from the list that have already been determined to be removed
            # this done to optimize the algorithm
            if(i >= len(row)):
                break
            row_i = row[i]
            for j in range(i+1,len(row)):
                #check if we are above the maximum index because we are actively removing
                #quotes from the list that have already been determined to be removed
                # this done to optimize the algorithm
                if j >= len(row):
                    break
                row_j = row[j]
                sim = jaccard_sim((row_i,row_j))
                if sim > threshold:
                    #remove the shorter quote from row and add it to the to_remove list
                    if len(row_i) < len(row_j):
                        row.remove(row_i)
                        to_remove.append(row_i)
                        break
                    else:
                        row.remove(row_j)
                        to_remove.append(row_j)

        return to_remove

    df = dataframe.drop_duplicates(subset = 'quotation')
    #list of the dataframes that have been cleaned
    #every element of the list contains a dataframe wiht the quotes of a single speaker.
    #all quotes have a similarity < threshold among each other
    df_clean =[]

    #create a numbered id for every speaker (for optimization reasons (filtering a dataframe using an integer column is
    # slightly quicker than with a String column))
    speakers = df['speaker'].drop_duplicates()
    speaker_dict = dict(zip(speakers,range(0,len(speakers))))
    df['speaker_id'] = df['speaker'].apply(lambda x: speaker_dict[x])

    #group quotes by speaker ids and put them all in a list
    quotes_by_speaker = df.groupby('speaker_id').agg(lambda x: list(x)).reset_index()[['speaker_id','quotation']]
    for i,row in quotes_by_speaker.iterrows():
        #identify the quotes that must be removed because they're too similar to another
        sentences_to_remove = clean_row(row.quotation)

        #remove the 'duplicate' quotes
        filt = df[df['speaker_id'] == row.speaker_id]
        filt = filt[np.logical_not(filt['quotation'].isin(sentences_to_remove))]

        df_clean.append(filt)
    #concatenate all results together
    return pd.concat(df_clean).drop(columns= 'speaker_id')
