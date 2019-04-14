#
# Author: Beatriz Fagundes
#
#

import sys
import csv
import logging
import json
import math
from csv_converter import save_csv, read_csv
import os
import spacy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#from joblib import Parallel, delayed
from sklearn.externals.joblib import Parallel, delayed
import itertools


def sentiment_features(review_sents):
    num_pos = 0
    num_neg = 0
    num_neutral = 0
    emotional_balance = 0
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


def argument_features(review):
    num_non_args = 0 # number of non-argumentative sentences
    num_claims = 0
    num_evidences = 0
    # Words that belong both to a claim and to a piece of evidence
    num_claim_evidence = 0

    # running MARGOT
    run_margot_cmd = './run_margot.sh'
    output_path = '.' # current directory
    review = review.replace('"', '')
    input_file = '"' + review + '"'
    full_cmd = run_margot_cmd + ' ' + input_file + ' ' + output_path
    os.system(full_cmd)
    # handles the MARGOT output file
    f = open('OUTPUT.json', 'r')
    try:
        for json_instance in f:
            doc = json.loads(json_instance)['document']
            for sent in doc:
                if 'evidence' in sent:
                    num_evidences += 1
                if 'claim' in sent:
                    num_claims += 1
                if 'claim_evidence' in sent:
                    num_claim_evidence += 1
                if not 'evidence' in sent and not 'claim' in sent and not 'claim_evidence' in sent:
                    num_non_args += 1
    finally:
        f.close()
    total_sents = num_evidences + num_claims + num_claim_evidence + num_non_args
    if total_sents == 0:
        return (0, 0, 0, 0)
    else:
        return (float(num_evidences)/float(total_sents),
                float(num_claims)/float(total_sents),
                float(num_claim_evidence)/float(total_sents),
                float(num_non_args)/float(total_sents))


def tokenize(review):
    tokens = []
    lemmas = []
    pos_tags = []
    syntactic_dep = []
    stopwords = []
    sentences = []
#    oovs = []
    nlp = spacy.load("en_core_web_sm")
    preprocessed_review = nlp(review)
    for sent in preprocessed_review.sents:
        sentences.append(str(sent))
    for token in preprocessed_review:
        token_text = token.text.lower()
        tokens.append(token_text)
        lemmas.append(token.lemma_)
        pos_tags.append(token.pos_)
        syntactic_dep.append(token.dep_)
        if token.is_stop == True:
            stopwords.append(token.text)
#        if token.is_oov == True:
#            oovs.append(token.text)
    return (tokens, lemmas, pos_tags, syntactic_dep, stopwords, sentences)


def extract_features(corpus):
    reviews_preprocessed = []
#    features_names = ['Evidences%', 'Claims%', 'ClaimEvidence%', 'NonArgs%', 'PosSents%', 'NegSents%', 'NeutralSents%', 'EmotionBalance', 'NewsDegreeIDF']
    features_names = []
#    unigrams = set()
#    tokens_per_review = []
    reviews = []
    N = len(corpus)
#    count = 0
#    for review_info in corpus:
#        count += 1
#        print(str(count))
#        review = review_info['reviewText']
#        if count == 1:
#            logging.info('Extracting linguistic features...')
#        tokens, lemmas, pos_tags, syntactic_dep, stopwords, sentences = tokenize(review)
#        unigrams.update(tokens)
#        tokens_per_review.append(tokens)
#        logging.info('Extracting argumentative features...')
#        num_evidences, num_claims, num_claim_evidence, num_non_args = argument_features(review)
#        logging.info('Extracting sentiment features...')
#        num_pos_sents, num_neg_sents, num_neutral_sents, emotional_balance = sentiment_features(sentences)
#        review_features = [num_evidences, num_claims, num_claim_evidence, num_non_args, num_pos_sents, num_neg_sents, num_neutral_sents, emotional_balance]
    tokens_per_review = Parallel(n_jobs=-1)(delayed(extract_tokens)(review_info) for review_info in corpus)
    unigrams = set(list( itertools.chain.from_iterable(tokens_per_review) ))
    print('tokens per review')
    print(str(len(tokens_per_review)))
    print('unigrams size')
    print(str(len(unigrams)))
    # compute IDF = log(number of documents / document frequency)
    logging.info('Extracting average IDF feature...')
    unigram_idf = {}
    vocab_df = {}
    for u in unigrams:
        vocab_df[u] = 0
        for r in tokens_per_review:
            if u in r:
                vocab_df[u] += 1
    for u in vocab_df:
        unigram_idf[u] = math.log(float(N)/float(vocab_df[u]))

    features_names = list(unigrams)
    reviews = Parallel(n_jobs=-1)(delayed(tfidf)(i, corpus[i], features_names, tokens_per_review[i], unigram_idf) for i in range(N))
#    # add avarage idf for a review as a feature
#    for idx in range(N):
#        total_idf = 0
#        for t in tokens_per_review[idx]:
#            total_idf += unigram_idf[t]
#        if len(tokens_per_review[idx]) == 0:
#            avg_idf = 0
#        else:
#            avg_idf = float(total_idf)/len(tokens_per_review[idx])
#        reviews_preprocessed[idx].append(avg_idf)
#
#        # create a hash with all the necessary info of the review
#        instance_to_save = {
#                'reviewClass': corpus[idx]['reviewClass']
#        }
#        for f in range(len(features_names)):
#            instance_to_save[features_names[f]] = reviews_preprocessed[idx][f]
#        reviews.append(instance_to_save)
#    import ipdb; ipdb.set_trace()
    logging.info('Number of features extracted: %s' % str(len(features_names)))
    return reviews


def extract_tokens(review_info):
    review = review_info['reviewText']
    tokens, lemmas, pos_tags, syntactic_dep, stopwords, sentences = tokenize(review)
    return tokens

def tfidf(idx, review, features, review_tokens, idf):
    instance_to_save = {
        'reviewClass': review['reviewClass']
    }
    for f in range(len(features)):
        token = features[f]
        instance_to_save[token] = float(review_tokens.count(token)) / idf[token]

    return instance_to_save


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

    corpus = read_csv(dataset)
    previous_dir = os.getcwd()
    full_margot_path = '../third-party/margot-modified/predictor'
#    os.chdir(full_margot_path)
    preprocessed = extract_features(corpus)
    logging.info('Storing the preprocessed dataset at: %s' % previous_dir)
    os.chdir(previous_dir)
    save_csv(preprocessed, dataset.replace('label', 'tfidf'))


main()
