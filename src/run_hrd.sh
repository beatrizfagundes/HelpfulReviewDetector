#!/bin/bash

echo Started

echo Musical Instruments
echo Feature extractor
python3 feature_extractor.py ../datasets/AmazonReviews-UCSD/Musical_Instruments_5_label.csv
echo Classification
python3 classifiers.py ../datasets/AmazonReviews-UCSD/Musical_Instruments_5_features.csv

echo Digital Music
echo CSV converter
python3 csv_converter.py json ../datasets/AmazonReviews-UCSD/Digital_Music_5.json
echo Labelize dataset
python3 labelize_dataset.py ../datasets/AmazonReviews-UCSD/Digital_Music_5.csv
echo Feature extractor
python3 feature_extractor.py ../datasets/AmazonReviews-UCSD/Digital_Music_5_label.csv
echo Classification
python3 classifiers.py ../datasets/AmazonReviews-UCSD/Digital_Music_5_features.csv

echo Pets Supplies
echo CSV converter
python3 csv_converter.py json ../datasets/AmazonReviews-UCSD/Pet_Supplies_5.json
echo Labelize dataset
python3 labelize_dataset.py ../datasets/AmazonReviews-UCSD/Pet_Supplies_5.csv
echo Feature extractor
python3 feature_extractor.py ../datasets/AmazonReviews-UCSD/Pet_Supplies_5_label.csv
echo Classification
python3 classifiers.py ../datasets/AmazonReviews-UCSD/Pet_Supplies_5_features.csv

echo Finished
