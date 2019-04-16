#
# Author: Beatriz Fagundes
#
#

import sys
import logging
import os
import random
from time import time
import numpy as np
import pandas as pd
from sklearn import svm, naive_bayes, tree, neighbors, linear_model, metrics
from sklearn.model_selection import cross_validate, StratifiedKFold
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score


def classify(X, result_file):
    tlabels = np.array(X.reviewClass.values.astype('int32'))
    X.drop('reviewClass', axis=1, inplace=True)
    X = np.array(X.values.astype('float32'))
    f = open(result_file, 'w')
    try:
        clfs = [svm.LinearSVC(), naive_bayes.MultinomialNB(), linear_model.Perceptron(), linear_model.SGDClassifier()]
        for clf in clfs:
            logging.info('Classifying data with %s' % clf)
            print(clf)
            t0 = time()
            print(t0)
            cv_results = cross_validate(clf, X, tlabels, cv=10, scoring=('accuracy', 'f1', 'precision', 'recall', 'roc_auc'), n_jobs=-1)
            # import ipdb; ipdb.set_trace()
            logging.info('done in %0.3fs' % (time() - t0))
            cv_accuracy = cv_results['test_accuracy']
            cv_precision = cv_results['test_precision']
            cv_recall = cv_results['test_recall']
            cv_f1 = cv_results['test_f1']
            cv_auc = cv_results['test_roc_auc']
            f.write(clf)
            f.write('Accuracy: %0.4f (+/- %0.2f)\n' % (cv_accuracy.mean(), cv_accuracy.std() * 2))
            f.write('Precision: %0.4f (+/- %0.2f)\n' % (cv_precision.mean(), cv_precision.std() * 2))
            f.write('Recall: %0.4f (+/- %0.2f)\n' % (cv_recall.mean(), cv_recall.std() * 2))
            f.write('F1: %0.4f (+/- %0.2f)\n' % (cv_f1.mean(), cv_f1.std() * 2))
            f.write('ROC AUC: %0.4f (+/- %0.2f)\n' % (cv_auc.mean(), cv_auc.std() * 2))
            logging.info('done in %0.3fs' % (time() - t0))
            print(time() - t0)
    finally:
        f.close()


def main():
    random.seed(2)

    # init log file
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO,
                        filename='classifiers.log')
    logging.info('Starting Classification task...')
    if len(sys.argv) != 2:
        logging.info('ERROR! Wrong number of params, you must follow the \
usage:')
        logging.info("python classifiers.py [csv file]")
        return
    dataset = sys.argv[1]
    logging.info('with dataset: %s' % dataset)

    corpus = pd.read_csv(dataset)
    corpus.reviewClass = corpus.reviewClass.map({'helpful': 1, 'not_helpful': 0})
#    X, tlabels, helpful_class = split_class_from_features(corpus)
    classify(corpus, dataset.replace('_tfidf.csv', '_results.txt'))


main()
