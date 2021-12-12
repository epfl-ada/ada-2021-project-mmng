
Setup - Commands for env install:
```shell
conda create -y -n ada python=3.8.12 scipy pandas numpy matplotlib

conda activate ada

conda install jupyterlab bokeh seaborn nb_conda_kernels

pip install texthero sklearn pyarrow

# XGBoost
conda install -c conda-forge xgboost
```

TODO
- Perform same pipeline that was succesful using uncleaned data (try adding cleaning into pipeline)
