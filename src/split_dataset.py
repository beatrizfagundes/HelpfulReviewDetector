import sys
import logging
import pandas as pd
import numpy as np

def main():
    # init log file
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO,
                        filename='split_dataset.log')
    if len(sys.argv) != 2:
        logging.info('ERROR! Wrong number of params, you must follow the \
usage:')
        logging.info("python split_dataset.py [csv file]")
        return
    dataset = sys.argv[1]
    logging.info('with dataset: %s' % dataset)
    df = pd.read_csv(dataset)
    count = 1
    for chunk in np.array_split(df, 8):
        logging.info(chunk.shape)
        chunk.to_csv(dataset.replace('.csv', str(count)+'.csv'), header=True, index=None)
        count += 1


main()
