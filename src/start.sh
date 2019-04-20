#!/bin/bash

echo Installing dependencies...

sudo apt update
sudo apt install git
sudo apt install gcc
sudo apt install unzip
sudo apt install megatools
sudo apt install silversearcher-ag
sudo apt install python3
sudo apt install python3-pip
sudo apt install default-jdk
sudo update-alternatives --config java

echo Installing Python libs...

pip3 install -U spacy
python3 -m spacy download en
python3 -m spacy download en_core_web_sm
pip3 install nltk
python3 -m nltk download vader_lexicon
pip3 install sklearn
pip3 install pandas
pip3 install torch
pip3 install joblib
pip3 install ipdb

echo Cloning HelpfulReviewDetector repository...
git clone https://github.com/beatrizfagundes/HelpfulReviewDetector.git
cd HelpfulReviewDetector

echo Downloading datasets...
mkdir datasets && cd datasets
#wget http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Video_Games_5.json.gz
#wget http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Musical_Instruments_5.json.gz
#wget http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Digital_Music_5.json.gz
#wget http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Pet_Supplies_5.json.gz
#wget http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Beauty_5.json.gz
#wget http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Cell_Phones_and_Accessories_5.json.gz
#wget http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Sports_and_Outdoors_5.json.gz
# Beauty label
megadl 'https://mega.nz/#!NmoXzAaD!0MeoFfJBOsm2nimaq6aIbgagdvfJQYBjhPB9WLY3VSo'
# Cell phones label
megadl 'https://mega.nz/#!NrwRmKjT!9SK3QNg-EqyXY0D28EcTwMwZYX3Mk2auJ3daRDyIpLE'
# Digital Music label
megadl 'https://mega.nz/#!An5x3KhI!tNOvBZOrvXI7Ow_QUcKMbYmViK3jpqyhKu9sxEtGPa0'
# Musical Instruments label
megadl 'https://mega.nz/#!hjgH2I7R!qadsj3740MGaVIc-PqB89t9_1AZJjRnNKoYtaRlz2b8'
# Pet supplies label
megadl 'https://mega.nz/#!N7gVWQzQ!hwm5HUJhBLO4ovpx0A3z45DbcDKnfQM5IYJERplHTgw'
# Sports label
megadl 'https://mega.nz/#!RihRhSqK!WTavqsJuGGmRMIPlumWtyjIpqAVqvPYYkHXLYKl4bHs'
# Video games label
#megadl ''

echo Unzipping the datasets...
#gzip -d reviews_Musical_Instruments_5.json.gz
#mv reviews_Musical_Instruments_5.json Musical_Instruments_5.json
gunzip *.csv.gz

