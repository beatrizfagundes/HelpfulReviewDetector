import sys
import logging
import pandas as pd
import numpy as np

def main():
    # init log file
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO,
                        filename='merge_features.log')
    if len(sys.argv) != 2:
        logging.info('ERROR! Wrong number of params, you must follow the \
usage:')
        logging.info("python3 merge_features.py [filename]")
        # e.g.: python3 merge_features.py Digital_Music_5
        return
    dataset = sys.argv[1]
    logging.info('with dataset: %s' % dataset)
    args = pd.read_csv('../datasets/argument/'+dataset+'_args.csv')
    args.drop('reviewClass', axis=1, inplace=True)
    senti = pd.read_csv('../datasets/sentiment/'+dataset+'_senti.csv')
    senti.drop('reviewClass', axis=1, inplace=True)
    novelty = pd.read_csv('../datasets/novelty/'+dataset+'_novelty.csv')
    novelty.drop('reviewClass', axis=1, inplace=True)
    spec = pd.read_csv('../datasets/specificity/'+dataset+'_spec.csv')
    final_df = pd.concat([args, senti, novelty, spec], axis=1)
#    spec.drop('reviewClass', axis=1, inplace=True)
#    tfidf = pd.read_csv('../datasets/tfidf/'+dataset+'_tfidf.csv')
#    final_df = pd.concat([args, senti, novelty, spec, tfidf], axis=1)
#    final_df = pd.concat([spec, tfidf], axis=1)
    logging.info('Number of documents: %s' % str(final_df.shape[0]))
    logging.info('Number of features: %s' % str(final_df.shape[1]))
    print(final_df.shape)
    final_df.to_csv('../datasets/'+dataset+'_features.csv', header=True, index=None)
#    final_df.to_csv('../datasets/'+dataset+'_tfidf_spec.csv', header=True, index=None)


main()
