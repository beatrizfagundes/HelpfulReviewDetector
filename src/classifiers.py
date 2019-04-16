#
# Author: Beatriz Fagundes
#
#

import sys
import logging
from csv_converter import save_csv, read_csv
import os
import random
from time import time
import numpy
import pandas as pd
from sklearn import svm, naive_bayes, tree, neighbors, linear_model, metrics
from sklearn.model_selection import cross_validate, StratifiedKFold
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, roc_auc_score


#def split_class_from_features(corpus):
#    X = []
#    tlabels = []
#    for review in corpus:
#        review_vec = []
#        tlabels.append(review['reviewClass'])
#        for feature in review:
#            if feature != 'reviewClass':
#                review_vec.append(float(review[feature]))
#        X.append(review_vec)
#    # transform the nominal classes to numerical classes
#    tlabels_levels = { 'helpful': 1, 'not_helpful': -1 }
##    tlabels_levels = list(set(tlabels))
##    idx_helpful = tlabels.index('helpful')
##    tlabels = [tlabels_levels.index(l) for l in tlabels]
#    tlabels = [tlabels_levels[l] for l in tlabels]
#    X = numpy.array(X)
#    tlabels = numpy.array(tlabels)
#    return (X, tlabels, tlabels[idx_helpful])


def classify(X, result_file):
    tlabels = X.reviewClass.values.tolist()
    X.drop('reviewClass', axis=1, inplace=True)
    f = open(result_file, 'w')
    try:
        clfs = [svm.LinearSVC(), naive_bayes.MultinomialNB(), linear_model.Perceptron(), linear_model.SGDClassifier()]
        for clf in clfs:
            logging.info('Classifying data with %s' % clf)
            t0 = time()
            cv_results = cross_validate(clf, X.as_matrix(), tlabels, cv=10, scoring=('accuracy', 'f1', 'precision', 'recall', 'roc_auc'), n_jobs=-1)
#            skf = StratifiedKFold(n_splits=10)
#            cv_accuracy = []
#            cv_precision = []
#            cv_recall = []
#            cv_f1 = []
#            for train_index, test_index in skf.split(X, tlabels):
#                X_train, X_test = X[train_index], X[test_index]
#                y_train, y_test = tlabels[train_index], tlabels[test_index]
#                clf.fit(X_train, y_train)
#                predicted = clf.predict(X_test)
#                tn, fp, fn, tp = confusion_matrix(y_test, predicted).ravel()
#                print(tn)
#                cv_accuracy.append( accuracy_score(y_test, predicted) )
#                cv_precision.append( precision_score(y_test, predicted) )
#                cv_recall.append( recall_score(y_test, predicted) )
#                cv_f1.append( f1_score(y_test, predicted) )
##                import ipdb; ipdb.set_trace()
            logging.info('done in %0.3fs' % (time() - t0))
            cv_accuracy = cv_results['test_accuracy']
            cv_precision = cv_results['test_precision']
            cv_recall = cv_results['test_recall']
            cv_f1 = cv_results['test_f1']
            cv_auc = cv_results['test_roc_auc']
            f.write('Accuracy: %0.4f (+/- %0.2f)\n' % (cv_accuracy.mean(), cv_accuracy.std() * 2))
            f.write('Precision: %0.4f (+/- %0.2f)\n' % (cv_precision.mean(), cv_precision.std() * 2))
            f.write('Recall: %0.4f (+/- %0.2f)\n' % (cv_recall.mean(), cv_recall.std() * 2))
            f.write('F1: %0.4f (+/- %0.2f)\n' % (cv_f1.mean(), cv_f1.std() * 2))
            f.write('ROC AUC: %0.4f (+/- %0.2f)\n' % (cv_auc.mean(), cv_auc.std() * 2))
            logging.info('done in %0.3fs' % (time() - t0))
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
    corpus.reviewClass = corpus.reviewClass.map({'helpful': 1, 'not_helpful': -1})
#    X, tlabels, helpful_class = split_class_from_features(corpus)
    classify(corpus, dataset.replace('_tfidf.csv', '_results.txt'))


main()
