#
# Author: Beatriz Fagundes
#
#

import sys
import logging
import spacy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from joblib import Parallel, delayed
#from sklearn.externals.joblib import Parallel, delayed
import itertools
import pandas as pd


def extract_sentiment_features(review, nlp):
    num_pos = 0
    num_neg = 0
    num_neutral = 0
    emotional_balance = 0
    review_sents = []
    for sentence in nlp(review).sents:
        review_sents.append(str(sentence))
    total_sents = len(review_sents)
    sentiment_analyzer = SentimentIntensityAnalyzer()
    for s in review_sents:
        sentiment_score = sentiment_analyzer.polarity_scores(s)['compound']
        if sentiment_score == 0:
            num_neutral += 1
        elif sentiment_score > 0:
            num_pos += 1
        else:
            num_neg += 1
    if total_sents == 0:
        return (0, 0, 0, 0)
    else:
        emotional_balance = float(abs(num_pos - num_neg)) / float(total_sents)
        return (float(num_pos)/float(total_sents),
                float(num_neg)/float(total_sents),
                float(num_neutral)/float(total_sents),
                emotional_balance)


def extract_features(corpus):
    # tokenize reviews
    corpus = corpus.dropna()
    print(str(corpus.shape[0]))
    logging.info('Number of valid documents: %s' % str(corpus.shape[0]))
    nlp = spacy.load("en_core_web_sm")
    corpus['sentiment'] = Parallel(n_jobs=-1)(delayed(extract_sentiment_features)(review, nlp) for review in corpus.reviewText)
    features_names = ['PosSents', 'NegSents', 'NeutralSents', 'EmotionBalance']
    for n, col in enumerate(features_names):
        corpus[col] = corpus['sentiment'].apply(lambda sentiment: sentiment[n])
    return corpus[['PosSents', 'NegSents', 'NeutralSents', 'EmotionBalance', 'reviewClass']].copy()


def main():
    # init log file
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO,
                        filename='feature_extractor.log')
    logging.info('Starting Feature Extractor...')
    if len(sys.argv) != 2:
        logging.info('ERROR! Wrong number of params, you must follow the \
usage:')
        logging.info("python feature_extractor.py [csv file]")
        return
    dataset = sys.argv[1]
    logging.info('with dataset: %s' % dataset)

    corpus = pd.read_csv(dataset)
    preprocessed = extract_features(corpus)
    logging.info('Storing the preprocessed dataset...')
    print('Storing the preprocessed dataset...')
    preprocessed.to_csv(dataset.replace('label', 'senti'), header=True, index=None)


main()
