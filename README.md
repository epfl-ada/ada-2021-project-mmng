# ADA Quotebank Project - The AI Politologist

Mauro Leidi, Gioele Monopoli, Nicky Baldwin, Michael Roust

- Readme.md file containing the detailed project proposal (up to 1000 words). Your README.md should contain:

    - *Abstract: A 150 word description of the project idea and goals. What’s the motivation behind your project? What story would you like to tell, and why?*

    - *Research Questions: A list of research questions you would like to address during the project.*

    - *Proposed additional datasets (if any): List the additional dataset(s) you want to use (if any), and some ideas on how you expect to get, manage, process, and enrich it/them. Show us that you’ve read the docs and some examples, and that you have a clear idea on what to expect. Discuss data size and format if relevant. It is your responsibility to check that what you propose is feasible.*

    - *Proposed timeline Organization within the team: A list of internal milestones up until project Milestone 3.
    Questions for TAs (optional): Add here any questions you have for us related to the proposed project.*

- Notebook containing initial analyses and data handling pipelines. We will grade the correctness, quality of code, and quality of textual descriptions.

# Abstract
In this project Quotebank is used to analyze American politics in depth. It is therefore necessary to label the quotes with their political inclination.
Subsequently, a model is trained to predict the quote political inclination. In addition, thanks to the value predicted by the model, it is possible to analyze how polarized the prediction is, and therefore discover how much the quote is representative of the political vision of the political party itself. 
Using this model, all the quotes of one senator can be summarized in a time series of political scores. These time series can be used in various ways to extract meaningful insights about American politics. We will study the trend of the political position of a selected senator and how influential a politician is within his political group. The goal is to make these analyzes interactive and fast.
# Research Questions
The main questions we want to answer are:
- How does a senator's political vision evolve over time?
- How much is a senator influenced by the statements of another senator?
- How influential is a senator within a political group?
One of the advantages of our approach is that it is not specific to the questions posed above, therefore once the model is created it is easy to be able to answer other different questions as well. For example, we would be able to see which party members have more distant positions or which members of different parties have a higher negative correlation.
# Additional stuff
In order to deal with such a big dataset we are thinking about rewriting our datasets either in pickle format or in parquet. This would allow for fast reading and writing. In addition, as suggested, we always process data either line-by-line either in chunks. We encountered a RAM overload problem when tring to vectorize the data with tf-idf model, but managed to solve them thanks to algorithms that allows iterable as imputs, and do not load all data into memory.
Everything we have done is absolutely not to be seen as a definitive choice, but rather as a first exploration to see what results we can try to achieve. In this case, keeping other data from the wikidata such as sex or other characteristics of the speaker could greatly improve our method. To get a first idea of the difficulty of the task we faced, we have visualized the PCA of 40000 datapoints. As we can see the data does not appear linearly separable with such a simple method. As a second test we tried to predict the class thanks to a simple sklearn random forest classifier, the result is quite comforting, giving a cross-validation precision just under 70%.
# Proposed timeline Organization within the team
A summary of the workflow we have imagined is presented in the following image:
![picture](https://github.com/epfl-ada/ada-2021-project-mmng.git/media/workflow.png)
1) Merging Quotebank with wikidatas, keeping only senators quotes
2) Preprocess data for the moment we are doing:  1. Replace not assigned values with empty spaces, 2. Lowercase all text, 3.Remove all blocks of digits, 4. Remove all string.punctuation (!"#$%&'()*+,-./:;<=>?@[]^_`{|}~) , 5. Remove all accents from strings, 6. Remove all stop words, 7.Remove all white space between words.
3) Vectorization of the data, for the moment we are representing data with the TF-IDF model. We encountered some RAM problems, but we found many solutions online thanks to algorithms that do not requirer the full dataset load in memory but works with chunks of data.
4) Model creation: We need to create a model for classification. We have in mind two main approaches: 1. Using NLP trained models and fine tuning for our purpose. 2. Training a model from scratch with our data.
5) Graphic User Interface creation and presentation of results.
# Questions for TAs
The first question we ask ourselves is whether it is worth trying to identify apolitical messages as a supplementary class. For example we thought that if a politician, Democrat or Republican, makes a statement about sport it should not be classified as politics by our model. In this direction, the statements of some groups of people (such as sportspeople) could be classified as apolitical. However, this task remains difficult to do cleanly (a politician might be politically engaged) and we'd love to have some advice on it.




