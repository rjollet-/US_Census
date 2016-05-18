#US Census

This project use US Census data and aims to predict people with income higher than 50K.

## Dataset

The dataset is in the folder /data you can find the metadata in data/census_income_metadata.txt. There is a train dataset called census_income_learn.csv and a learn dataset called census_income_test.csv.

## Dependencies and preprocessing

First you need to install the dependencies. This project use python 3.5.

```
pip install -r requirements.txt
```

Then you can run the preprocessing script

```
python preprocessing.py
```

## Statistical look on the dataset

You can find the Statistical analysis in statistic.html or using Rstudio to open statistic.Rmd.

## Model to predict income higher than 50K

You can find different model analysis in US_census_model.html or in the ipython notebook US_census_model.ipynb.
