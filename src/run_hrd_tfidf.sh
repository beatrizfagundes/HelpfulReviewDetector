#!/bin/bash

echo Started

#echo Musical Instruments
#echo CSV converter
#python3 csv_converter.py json ../datasets/Musical_Instruments_5.json
#echo Labelize dataset
#python3 labelize_dataset.py ../datasets/Musical_Instruments_5.csv
#rm ../datasets/Musical_Instruments_5.json
#rm ../datasets/Musical_Instruments_5.csv
#
#echo Digital Music
#gzip -d ../datasets/reviews_Digital_Music_5.json.gz
#mv ../datasets/reviews_Digital_Music_5.json ../datasets/Digital_Music_5.json
#echo CSV converter
#python3 csv_converter.py json ../datasets/Digital_Music_5.json
#echo Labelize dataset
#python3 labelize_dataset.py ../datasets/Digital_Music_5.csv
#rm ../datasets/Digital_Music_5.json
#rm ../datasets/Digital_Music_5.csv
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
#
#echo Cell phones and Accessories
#gzip -d ../datasets/reviews_Cell_Phones_and_Accessories_5.json.gz
#mv ../datasets/reviews_Cell_Phones_and_Accessories_5.json ../datasets/Cell_Phones_and_Accessories_5.json
#echo CSV converter
#python3 csv_converter.py json ../datasets/Cell_Phones_and_Accessories_5.json
#echo Labelize dataset
#python3 labelize_dataset.py ../datasets/Cell_Phones_and_Accessories_5.csv
#rm ../datasets/Cell_Phones_and_Accessories_5.json
#rm ../datasets/Cell_Phones_and_Accessories_5.csv
#
#echo Sports and Outdoors
#gzip -d ../datasets/reviews_Sports_and_Outdoors_5.json.gz
#mv ../datasets/reviews_Sports_and_Outdoors_5.json ../datasets/Sports_and_Outdoors_5.json
#echo CSV converter
#python3 csv_converter.py json ../datasets/Sports_and_Outdoors_5.json
#echo Labelize dataset
#python3 labelize_dataset.py ../datasets/Sports_and_Outdoors_5.csv
#rm ../datasets/Sports_and_Outdoors_5.json
#rm ../datasets/Sports_and_Outdoors_5.csv

echo Feature extractor
echo Musical Instruments
python3 feature_extractor_tfidf.py ../datasets/Musical_Instruments_5_label.csv
gzip ../datasets/Musical_Instruments_5_tfidf.csv
echo Digital Music
python3 feature_extractor_tfidf.py ../datasets/Digital_Music_5_label.csv
gzip ../datasets/Digital_Music_5_tfidf.csv
echo Pets Supplies
python3 feature_extractor_tfidf.py ../datasets/Pet_Supplies_5_label.csv
gzip ../datasets/Pet_Supplies_5_tfidf.csv
echo Beauty
python3 feature_extractor_tfidf.py ../datasets/Beauty_5_label.csv
gzip ../datasets/Beauty_5_tfidf.csv
echo Video games
python3 feature_extractor_tfidf.py ../datasets/Video_Games_5_label.csv
gzip ../datasets/Video_Games_5_tfidf.csv
echo Sports and Outdoors
python3 feature_extractor_tfidf.py ../datasets/Sports_and_Outdoors_5_label.csv
gzip ../datasets/Sports_and_Outdoors_5_tfidf.csv
echo Cell phones and Accessories
python3 feature_extractor_tfidf.py ../datasets/Cell_Phones_and_Accessories_5_label.csv
gzip ../datasets/Cell_Phones_and_Accessories_5_tfidf.csv

echo Classification
echo Musical Instruments
gzip -d ../datasets/Musical_Instruments_5_tfidf.csv.gz
python3 classifiers.py ../datasets/Musical_Instruments_5_tfidf.csv
gzip ../datasets/Musical_Instruments_5_tfidf.csv
echo Digital Music
gzip -d ../datasets/Digital_Music_5_tfidf.csv.gz
python3 classifiers.py ../datasets/Digital_Music_5_tfidf.csv
gzip ../datasets/Digital_Music_5_tfidf.csv
echo Pets Supplies
gzip -d ../datasets/Pet_Supplies_5_tfidf.csv.gz
python3 classifiers.py ../datasets/Pet_Supplies_5_tfidf.csv
gzip ../datasets/Pet_Supplies_5_tfidf.csv
echo Beauty
gzip -d ../datasets/Beauty_5_tfidf.csv.gz
python3 classifiers.py ../datasets/Beauty_5_tfidf.csv
gzip ../datasets/Beauty_5_tfidf.csv
echo Video games
gzip -d ../datasets/Video_Games_5_tfidf.csv.gz
python3 classifiers.py ../datasets/Video_Games_5_tfidf.csv
gzip ../datasets/Video_Games_5_tfidf.csv
#echo Sports and Outdoors
#python3 feature_extractor_tfidf.py ../datasets/Sports_and_Outdoors_5_label.csv
#gzip ../datasets/Sports_and_Outdoors_5_tfidf.csv
#echo Cell phones and Accessories
#python3 feature_extractor_tfidf.py ../datasets/Cell_Phones_and_Accessories_5_label.csv
#gzip ../datasets/Cell_Phones_and_Accessories_5_tfidf.csv


echo Finished
