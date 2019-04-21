#!/bin/bash

echo Started

echo Musical Instruments
echo $(date -u)
echo Sample sentences
python3 get_sentences_sample.py ../datasets/Musical_Instruments_5.txt
echo $(date -u)
echo Train
cd ../lib/speciteller/Domain-Agnostic-Sentence-Specificity-Prediction
python3 train.py --test_data /home/soniassfsl26/HelpfulReviewDetector/datasets/Musical_Instruments_5_train.txt
echo $(date -u)
echo Test
cd ../../../src
python3 feature_extractor_specificity.py ../datasets/Musical_Instruments_5_label.csv
echo $(date -u)
#echo Train with entire comments
#cd ../lib/speciteller/Domain-Agnostic-Sentence-Specificity-Prediction
#python3 train.py --test_data /home/soniassfsl26/HelpfulReviewDetector/datasets/Musical_Instruments_5.txt
#echo $(date -u)
#echo Test
#python3 test.py --test_data /home/soniassfsl26/HelpfulReviewDetector/datasets/Musical_Instruments_5.txt
#echo $(date -u)

#echo Digital Music
##gzip -d ../datasets/reviews_Digital_Music_5.json.gz
##mv ../datasets/reviews_Digital_Music_5.json ../datasets/Digital_Music_5.json
##echo CSV converter
##python3 csv_converter.py json ../datasets/Digital_Music_5.json
##echo Labelize dataset
##python3 labelize_dataset.py ../datasets/Digital_Music_5.csv
##rm ../datasets/Digital_Music_5.json
##rm ../datasets/Digital_Music_5.csv
#echo Feature extractor
#python3 feature_extractor.py ../datasets/Digital_Music_5_label.csv
#gzip ../datasets/Digital_Music_5_tfidf.csv
#
#echo Pets Supplies
#gzip -d ../datasets/reviews_Pet_Supplies_5.json.gz
#mv ../datasets/reviews_Pet_Supplies_5.json ../datasets/Pet_Supplies_5.json
#echo CSV converter
#python3 csv_converter.py json ../datasets/Pet_Supplies_5.json
#echo Labelize dataset
#python3 labelize_dataset.py ../datasets/Pet_Supplies_5.csv
#rm ../datasets/Pet_Supplies_5.json
#rm ../datasets/Pet_Supplies_5.csv
#echo Feature extractor
#python3 feature_extractor.py ../datasets/Pet_Supplies_5_label.csv
#gzip ../datasets/Pet_Supplies_5_tfidf.csv
#
#echo Beauty
#gzip -d ../datasets/reviews_Beauty_5.json.gz
#mv ../datasets/reviews_Beauty_5.json ../datasets/Beauty_5.json
#echo CSV converter
#python3 csv_converter.py json ../datasets/Beauty_5.json
#echo Labelize dataset
#python3 labelize_dataset.py ../datasets/Beauty_5.csv
#rm ../datasets/Beauty_5.json
#rm ../datasets/Beauty_5.csv
#echo Feature extractor
#python3 feature_extractor.py ../datasets/Beauty_5_label.csv
#gzip ../datasets/Beauty_5_tfidf.csv
#
##echo Cell phones and Accessories
##gzip -d ../datasets/reviews_Cell_Phones_and_Accessories_5.json.gz
##mv ../datasets/reviews_reviews_Cell_Phones_and_Accessories_5.json ../datasets/Cell_Phones_and_Accessories_5.json
##echo CSV converter
##python3 csv_converter.py json ../datasets/Cell_Phones_and_Accessories_5.json
##echo Labelize dataset
##python3 labelize_dataset.py ../datasets/Cell_Phones_and_Accessories_5.csv
##echo Feature extractor
##python3 feature_extractor.py ../datasets/Cell_Phones_and_Accessories_5_label.csv
##
##echo Sports and Outdoors
##gzip -d ../datasets/reviews_Sports_and_Outdoors_5.json.gz
##mv ../datasets/reviews_Sports_and_Outdoors_5.json ../datasets/Sports_and_Outdoors_5.json
##echo CSV converter
##python3 csv_converter.py json ../datasets/Sports_and_Outdoors_5.json
##echo Labelize dataset
##python3 labelize_dataset.py ../datasets/Sports_and_Outdoors_5.csv
##rm ../datasets/Sports_and_Outdoors_5.json
##rm ../datasets/Sports_and_Outdoors_5.csv
##echo Feature extractor
##python3 feature_extractor.py ../datasets/Sports_and_Outdoors_5_label.csv
##gzip ../datasets/Sports_and_Outdoors_5_tfidf.csv
#
#echo Video games
#gzip -d ../datasets/reviews_Video_Games_5.json.gz
#mv ../datasets/reviews_Video_Games_5.json ../datasets/Video_Games_5.json
#echo CSV converter
#python3 csv_converter.py json ../datasets/Video_Games_5.json
#echo Labelize dataset
#python3 labelize_dataset.py ../datasets/Video_Games_5.csv
#rm ../datasets/Video_Games_5.json
#rm ../datasets/Video_Games_5.csv
#echo Feature extractor
#python3 feature_extractor.py ../datasets/Video_Games_5_label.csv
#gzip ../datasets/Video_Games_5_tfidf.csv

echo Finished
