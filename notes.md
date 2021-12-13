
## Setup

Commands for env install:
```shell
conda create -y -n ada python=3.8.12 scipy pandas numpy matplotlib

conda activate ada

conda install jupyterlab bokeh seaborn nb_conda_kernels

pip install texthero sklearn pyarrow

# OPTIONAL - XGBoost
conda install -c conda-forge xgboost
```

## Preprocessing Pipeline

All preprocessing is in files like `prepro_______.py`

To run any preprocessing just use `prepro_run.py`. Its a small file take a look

I split preprocessing into 2 separate stages labeling and cleaning.

## Saving models

Use functions `load_pickle` or `save_pickle`. You can use this to save/load (almost) any python object afaik.

As usual I'm using paths defined in `helper.py` for consistency.

Loading example:
``` python
vectorizer = load_pickle(VECTORIZER_NGRAM13)
clf = load_pickle(MODEL_MULTINOMIALNB_NGRAM13)

X_vectorized = vectorizer.transform(X)
clf.predict(X)
```

Saving example:
```
vectorizer = TfidfVectorizer(ngram_range=(1,3))
X_vectorized = vectorizer.fit_transform(X)

save_pickle(vectorizer, VECTORIZER_NGRAM13)
```

---

## Misc

Michael TODO
- Loading of models
- Add RD to pipeline
- Add cleaning variants exploration to final_final
- (optional) logistic regression
