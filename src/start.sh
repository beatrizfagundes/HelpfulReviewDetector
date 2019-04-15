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
wget http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Video_Games_5.json.gz
wget http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Musical_Instruments_5.json.gz
wget http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Digital_Music_5.json.gz
wget http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Pet_Supplies_5.json.gz
wget http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Beauty_5.json.gz
wget http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Cell_Phones_and_Accessories_5.json.gz
wget http://snap.stanford.edu/data/amazon/productGraph/categoryFiles/reviews_Sports_and_Outdoors_5.json.gz

echo Unzipping the datasets...
gzip -d reviews_Musical_Instruments_5.json.gz
mv reviews_Musical_Instruments_5.json Musical_Instruments_5.json

