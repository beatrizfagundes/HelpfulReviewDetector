import sys
import logging
import pandas as pd
import numpy as np

def main():
    # init log file
    logging.basicConfig(format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO,
                        filename='merge_rows.log')
    if len(sys.argv) != 3:
        logging.info('ERROR! Wrong number of params, you must follow the \
usage:')
        logging.info("python3 merge_rows.py [filename] [number of files]")
        # e.g.: python3 merge_rows.py ../datasets/Digital_Music_5_senti 8
        return
    dataset = sys.argv[1]
    num_files = int(sys.argv[2])
    logging.info('with dataset: %s' % dataset)
    logging.info('with %s files' % str(num_files))
    dfs = []
    for i in range(1, num_files+1):
        dfs.append(pd.read_csv(dataset+str(i)+'.csv'))
    final_df = pd.concat(dfs, ignore_index=True)
    logging.info('Number of documents: %s' % str(final_df.shape[0]))
    print(final_df.shape[0])
    final_df.to_csv(dataset+'.csv', header=True, index=None)


main()
