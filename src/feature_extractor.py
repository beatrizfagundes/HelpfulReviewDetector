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
    if review[0] == '"' and review[len(review)-1] == '"':
        input_file = review
    else:
        input_file = '"' + review + '"'
    os.system(run_margot_cmd + ' ' + input_file + ' ' + output_path)
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
        # compute the document frequency of each token
        if not token_text in tokens:
            if token_text in vocab_df:
                vocab_df[token_text] += 1
            else:
                vocab_df[token_text] = 1
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
    features_names = ['Evidences%', 'Claims%', 'ClaimEvidence%', 'NonArgs%', 'PosSents%', 'NegSents%', 'NeutralSents%', 'EmotionBalance', 'NewsDegreeIDF']
    unigrams = set()
    tokens_per_review = []
    reviews = []
    N = len(corpus)
    for review_info in corpus:
        review = review_info['reviewText']
        logging.info('Extracting linguistic features...')
        tokens, lemmas, pos_tags, syntactic_dep, stopwords, sentences = tokenize(review)
        unigrams.update(tokens)
        tokens_per_review.append(tokens)
        logging.info('Extracting argumentative features...')
        num_evidences, num_claims, num_claim_evidence, num_non_args = argument_features(review)
        logging.info('Extracting sentiment features...')
        num_pos_sents, num_neg_sents, num_neutral_sents, emotional_balance = sentiment_features(sentences)
        review_features = [num_evidences, num_claims, num_claim_evidence, num_non_args, num_pos_sents, num_neg_sents, num_neutral_sents, emotional_balance]
        reviews_preprocessed.append(review_features)
    # compute IDF = log(number of documents / document frequency)
    logging.info('Extracting average IDF feature...')
    unigram_idf = {}
    for u in unigrams:
        unigram_idf[u] = math.log(float(N)/float(vocab_df[u]))
    # add avarage idf for a review as a feature
    for idx in range(N):
        total_idf = 0
        for t in tokens_per_review[idx]:
            total_idf += unigram_idf[t]
        avg_idf = float(total_idf)/len(tokens_per_review[idx])
        reviews_preprocessed[idx].append(avg_idf)
        # create a hash with all the necessary info of the review
        instance_to_save = {
                'reviewClass': corpus[idx]['reviewClass']
        }
        for f in range(len(features_names)):
            instance_to_save[features_names[f]] = reviews_preprocessed[idx][f]
        reviews.append(instance_to_save)
#    import ipdb; ipdb.set_trace()
    logging.info('Number of features extracted: %s' % str(len(features_names)))
    return reviews

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
    full_margot_path = '../third-party/predictor'
    os.chdir(full_margot_path)
    preprocessed = extract_features(corpus)
    logging.info('Storing the preprocessed dataset at: %s' % previous_dir)
    os.chdir(previous_dir)
    save_csv(preprocessed, dataset.replace('_label.csv', '_features.csv'))


vocab_df = {}
main()
