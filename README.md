# ADA Quotebank Project - American Data Analysis

Mauro Leidi, Gioele Monopoli, Nicolas Baldwin, Michael Roust

# Abstract
In this project Quotebank is used to analyze American politics in depth. First, it is necessary to label the quotes with their political inclination.
Subsequently, a model is trained to predict the quote political inclination. Thanks to the value predicted by the model, it is possible to analyze how polarized the prediction is, and therefore discover how much the quote is representative of the political vision of the political party itself.
Using this model, quotes of one politician can be summarized in a time series of political scores. These time series can be used in various ways to extract meaningful insights about American politics. We will study the trend of the political vision and we will be able to analyise the polarization of every politician. The goal is to allow users to make these customized and fast analysis. We will focus on the classification between Republicans and Democrats.
![](media/TimeSerie.PNG)
# Research Questions
The main questions we want to answer are:
- How does a politician's political vision evolve over time?
- How much is a politician vision polarized?
- How similar is the vision of a politician to the vision of his party?
- What differenciate the quotes of Republicans and Democrats?
One of the advantages of our approach is that it is not specific to the questions posed above, therefore once the model is created it is easy to be able to answer other different questions as well. For example, we would be able to see which party members have more distant vision or which members of different parties have a higher negative correlation.
# Workflow
A summary of the workflow is presented in the following image:
![](media/workflow.PNG)
1) Merging Quotebank with wikidatas, keeping only the data where the occupation is politician and where there are not any homonym on wikidata (because in Quotebank we have a little problem... the assignement of the quote is done with a name and not with a id, therefore we will not be able to distinguish quotation of Tim Cahill (politician) and Tim Cahill (american fotball player)).
2) Preprocess data allows for combination of the following operations:
   1) Replace not assigned values with empty spaces
   2) Lowercase all text
   3) Remove all blocks of digits
   4) Remove all string.punctuation (!"#$%&'()*+,-./:;<=>?@[]^_`{|}~)
   5) Remove all accents from strings
   6) Remove all stop words
   7) Remove all extra white spaces at the end of a quote
   8) Lemmatization
   9) Data expantion thanks to n-grams can be perfomed when the data is vectorized
3) Vectorization of the data, for the moment we are representing data with the TF-IDF model. We encountered some RAM problems, but we found many solutions online thanks to algorithms that do not requirer the full dataset load in memory but works with chunks of data.
4) Model creation: We need to create a model for classification. We tried many different classification models including fine tuning an NLP pretrained models for our purpose and a Neural network, different classifiers and decided to use a multinomial naive baesian model (note that linear SVC performed ad good).
5) Time series generation thanks to the model predictions.
6) Study of results, interpretation of the model and Research question answering.

The work was split between the group in the following way (Everyone did a bit of everything this is just indicative of who was the responsable leader of that task (the boss)):

Task                    |Responsable
------------------------|-------------
Data Exploration        |    Mauro
Merge Wikidata Quotebank|    Michael
Preprocess text data    |    Nicky
text data Vectorization |    Gioele
Model exploratios       | Nicky  & Mauro
Time series analyisis   | Gioele & Michael
Data story redaction    | Nicky & Mauro
Web-site creation       | Gioele & Mauro
github/code organization| Michael
pipelines organization  | Nicky & Michael

# Strategy
In order to deal with such a big dataset we are rewriting our datasets in pickle format. This allow for fast reading and writing. In addition, as suggested, when is necessary we always process data either line-by-line either in chunks. We encountered a RAM overload problem when tring to vectorize the data with tf-idf model, but managed to solve them thanks to algorithms that allows iterable as inputs, and do not load all data into memory.
To get a first idea of the difficulty of the task we faced, we have visualized the PCA of NB datapoints.
![](media/pca.png)
As we can see the data does not appear linearly separable with such a simple method.

# Additional remarks
The first question we ask ourselves is whether it is worth trying to identify apolitical messages as a supplementary class. For example we thought that if a politician, Democrat or Republican, makes a statement about sport it should not be classified as politics by our model. In this direction, the statements of some groups of people (such as sportspeople) could be classified as apolitical. However, this task remains difficult to do cleanly (a politician might be politically engaged) and we'd love to have some advice on it. Another solution to reduce the impact of this problem would be to look inside the urls for a substring that represent a topic not related to politics. For example if we find the word "gossip" in the url the quotation will not probably be a political statement. We repete this operation on multiple misleading keywords. Is this a good idea?
# Result analysis
Please take a look at the website: https://ogimgio.github.io/ada-mmng-website/
# Code organization

### Notebooks
- [raw_full_data_exploration.ipynb](raw_full_data_exploration.ipynb): Notebook containing surface analyses on the complete raw Quotebank dataset.
- [final_notebook.ipynb](final_notebook.ipynb): Notebook containing all the in depth analyses of the data. Analyses are ran on (at times samples of) raw and cleaned 2020 datas as performing them on the full dataset would be largely impractical and provide little added benefit.

### Scripts and project wide utilities
- [helpers.py](helpers.py): Project wide constants, file paths, helper and utility functions.
- [prepro_pipeline.py](prepro_pipeline.py): Executable that perfoms the 1st part of our data preprocessing pipeline. Currently performs the following operations:
  - Labels quotes by the political party (Republican or Democrat) of the speaker attributed to each quote. Using functions from [prepro_party_labeling.py](prepro_party_labeling.py)
  - Drops unused columns to reduce dataset footprint.
  - Cleans quotation text. Performs procedures such as lowercasing all characters, removing diacritics and more. See detailed description in
- [prepro_party_labeling.py](prepro_party_labeling.py): Labels data by merging Quotebank quotes data to the Wikidata speaker_attributes dump. Any quotes that have no speaker attributed to them or have a speaker that is neither Republican or Democrat are dropped.
- [perform_general_analysis.py](perform_general_analysis.py) Functions for raw full data exploration.
- [drop_similar_quotes.py](drop_similar_quotes.py) Similar/duplicate quotes removal logic.
