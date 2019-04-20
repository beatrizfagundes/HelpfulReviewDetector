#!/bin/bash

echo Started

echo Feature extractor
echo Musical Instruments
python3 feature_extractor_sentiment.py ../datasets/Musical_Instruments_5_label.csv
gzip ../datasets/Musical_Instruments_5_senti.csv
echo Digital Music
python3 feature_extractor_sentiment.py ../datasets/Digital_Music_5_label.csv
gzip ../datasets/Digital_Music_5_senti.csv
echo Pets Supplies
python3 feature_extractor_sentiment.py ../datasets/Pet_Supplies_5_label.csv
gzip ../datasets/Pet_Supplies_5_senti.csv
echo Beauty
python3 feature_extractor_sentiment.py ../datasets/Beauty_5_label.csv
gzip ../datasets/Beauty_5_senti.csv
echo Video games
python3 feature_extractor_sentiment.py ../datasets/Video_Games_5_label.csv
gzip ../datasets/Video_Games_5_senti.csv
echo Sports and Outdoors
python3 feature_extractor_sentiment.py ../datasets/Sports_and_Outdoors_5_label.csv
gzip ../datasets/Sports_and_Outdoors_5_senti.csv
echo Cell phones and Accessories
python3 feature_extractor_sentiment.py ../datasets/Cell_Phones_and_Accessories_5_label.csv
gzip ../datasets/Cell_Phones_and_Accessories_5_senti.csv


echo Finished
