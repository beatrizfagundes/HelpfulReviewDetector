#!/bin/bash

echo Started

echo Feature extractor
echo Musical Instruments
#python3 feature_extractor_sentiment.py ../datasets/Musical_Instruments_5_label.csv
#gzip ../datasets/Musical_Instruments_5_senti.csv
echo Digital Music
python3 feature_extractor_sentiment.py ../datasets/Digital_Music_5_label1.csv
gzip ../datasets/Digital_Music_5_senti1.csv
python3 feature_extractor_sentiment.py ../datasets/Digital_Music_5_label2.csv
gzip ../datasets/Digital_Music_5_senti2.csv
python3 feature_extractor_sentiment.py ../datasets/Digital_Music_5_label3.csv
gzip ../datasets/Digital_Music_5_senti3.csv
python3 feature_extractor_sentiment.py ../datasets/Digital_Music_5_label4.csv
gzip ../datasets/Digital_Music_5_senti4.csv
python3 feature_extractor_sentiment.py ../datasets/Digital_Music_5_label5.csv
gzip ../datasets/Digital_Music_5_senti5.csv
python3 feature_extractor_sentiment.py ../datasets/Digital_Music_5_label6.csv
gzip ../datasets/Digital_Music_5_senti6.csv
python3 feature_extractor_sentiment.py ../datasets/Digital_Music_5_label7.csv
gzip ../datasets/Digital_Music_5_senti7.csv
python3 feature_extractor_sentiment.py ../datasets/Digital_Music_5_label8.csv
gzip ../datasets/Digital_Music_5_senti8.csv
#echo Pets Supplies
#python3 feature_extractor_sentiment.py ../datasets/Pet_Supplies_5_label.csv
#gzip ../datasets/Pet_Supplies_5_senti.csv
#echo Beauty
#python3 feature_extractor_sentiment.py ../datasets/Beauty_5_label.csv
#gzip ../datasets/Beauty_5_senti.csv
#echo Video games
#python3 feature_extractor_sentiment.py ../datasets/Video_Games_5_label.csv
#gzip ../datasets/Video_Games_5_senti.csv
#echo Sports and Outdoors
#python3 feature_extractor_sentiment.py ../datasets/Sports_and_Outdoors_5_label.csv
#gzip ../datasets/Sports_and_Outdoors_5_senti.csv
echo Cell phones and Accessories
python3 feature_extractor_sentiment.py ../datasets/Cell_Phones_and_Accessories_5_label1.csv
gzip ../datasets/Cell_Phones_and_Accessories_5_senti1.csv
python3 feature_extractor_sentiment.py ../datasets/Cell_Phones_and_Accessories_5_label2.csv
gzip ../datasets/Cell_Phones_and_Accessories_5_senti2.csv
python3 feature_extractor_sentiment.py ../datasets/Cell_Phones_and_Accessories_5_label3.csv
gzip ../datasets/Cell_Phones_and_Accessories_5_senti3.csv
python3 feature_extractor_sentiment.py ../datasets/Cell_Phones_and_Accessories_5_label4.csv
gzip ../datasets/Cell_Phones_and_Accessories_5_senti4.csv
python3 feature_extractor_sentiment.py ../datasets/Cell_Phones_and_Accessories_5_label5.csv
gzip ../datasets/Cell_Phones_and_Accessories_5_senti5.csv
python3 feature_extractor_sentiment.py ../datasets/Cell_Phones_and_Accessories_5_label6.csv
gzip ../datasets/Cell_Phones_and_Accessories_5_senti6.csv
python3 feature_extractor_sentiment.py ../datasets/Cell_Phones_and_Accessories_5_label7.csv
gzip ../datasets/Cell_Phones_and_Accessories_5_senti7.csv
python3 feature_extractor_sentiment.py ../datasets/Cell_Phones_and_Accessories_5_label8.csv
gzip ../datasets/Cell_Phones_and_Accessories_5_senti8.csv


echo Finished
