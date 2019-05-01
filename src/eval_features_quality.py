import sys
import logging
import pandas as pd
import numpy as np
from sklearn.feature_selection import chi2, mutual_info_classif
from sklearn import ensemble
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

def chi(X, y):
    print('chi2')
    features_names = X.columns.values.tolist()
    chi2score = chi2(X, y)[0]
    wscores = zip(features_names, chi2score)
    wchi2 = sorted(wscores, key=lambda x:x[1], reverse=True)
    print(wchi2[:14])

def mutual_info(X, y):
    print('mutual information')
    features_names = X.columns.values.tolist()
    mi_score = mutual_info_classif(X, y)
    wscores = zip(features_names, mi_score)
    wmi = sorted(wscores, key=lambda x:x[1], reverse=True)
    print(wmi[:14])


def gini_index(X, y):
    print('gini')
    rf = ensemble.RandomForestClassifier()
    rf.fit(X, y)
    features_names = X.columns.values.tolist()
    gini_scores = zip(features_names, rf.feature_importances_)
    sorted_gini_scores = sorted(gini_scores, key=lambda x:x[1], reverse=True)
    print(sorted_gini_scores[:14])


def calculate_pearson_correlation(df):
    plt.figure(figsize=(12,10))
    cor = df.corr()
    sns.heatmap(cor, annot=True, cmap=plt.cm.Reds)
    plt.show()


def main():
    # init log file
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO,
                        filename='feature_quality_evaluator.log')
    if len(sys.argv) != 2:
        logging.info('ERROR! Wrong number of params, you must follow the \
usage:')
        logging.info("python3 eval_features_quality.py [csv file]")
        return
    dataset = sys.argv[1]
    logging.info('with dataset: %s' % dataset)
    df = pd.read_csv(dataset)
    X = df.drop('reviewClass', axis=1)
    y = df.reviewClass
    chi(X, y)
    mutual_info(X, y)
    gini_index(X, y)
#    calculate_pearson_correlation(df)

main()
