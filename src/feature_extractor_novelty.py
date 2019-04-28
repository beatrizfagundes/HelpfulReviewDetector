import sys
import logging
import pandas as pd
import numpy as np

def main():
    # init log file
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO,
                        filename='feature_extractor_novelty.log')
    if len(sys.argv) != 2:
        logging.info('ERROR! Wrong number of params, you must follow the \
usage:')
        logging.info("python feature_extractor_novelty.py [csv file]")
        return
    dataset = sys.argv[1]
    logging.info('with dataset: %s' % dataset)
    corpus = pd.read_csv(dataset)

    corpus_class = corpus.reviewClass
    corpus.drop('reviewClass', axis=1, inplace=True)
    sum_idf = corpus.sum(axis=1) # sum the values from each row
    n_terms = corpus.astype(bool).sum(axis=1) # count the features that appeared in each review (count non-zero values)
    avg_idf = sum_idf/n_terms
    novelty = avg_idf.to_frame().rename(columns = {0: 'AvgIDF'})
    corpus.replace(0, np.nan, inplace=True) # to disregard 0 to calculate the min idf
    novelty['MinIDF'] = corpus.min(axis=1)
    novelty['MaxIDF'] = corpus.max(axis=1)
    # if in the preprocessing step all the tokens from a review are filtered by
    # the document frequency cut-offs, stop words removal, etc, the review will
    # have no unigrams and, therefore, all the idf values will be zero. That's
    # why we need to take care of the 0/0 division as well as minIDF = NaN and
    # maxIDF = NaN in the following line
    novelty.replace(np.nan, 0, inplace=True)
    novelty['reviewClass'] = corpus_class
    novelty.to_csv(dataset.replace('idf', 'novelty'), header=True, index=None)


main()
