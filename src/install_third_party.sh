#!/bin/bash

echo Installing third-party tools...
mkdir lib && cd lib
echo "######### Margot - Argument Mining tool"
megadl 'https://mega.nz/#!R6pyCaxZ!AOxuX24h-dWhOMZGTGv3dj-7xAPG7g2UC9jK3LY3g6c'
unzip svm-light-TK-1.5.zip
rm -rf __MACOSX/
cd SVM-Light-1.5-to-be-released
make
cd ..
git clone https://github.com/beatrizfagundes/margot-modified.git
cd margot-modified/predictor
mkdir bin
mkdir lib
# before installing the dependencies, sometimes we need to modify the Makefile from svm_hmm folder
# and insert LIBS = -lm right below LDFLAGS
./install_dependencies.sh
cp ../../SVM-Light-1.5-to-be-released/svm_classify bin/.
./compile.sh

echo "######### SPECITELLER - Specific sentences detector"
cd ../..
mkdir speciteller && cd speciteller
git clone https://github.com/beatrizfagundes/Domain-Agnostic-Sentence-Specificity-Prediction.git
cd Domain-Agnostic-Sentence-Specificity-Prediction
wget https://nlp.stanford.edu/data/glove.840B.300d.zip
unzip glove.840B.300d.zip

