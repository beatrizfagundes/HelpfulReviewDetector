#!/bin/bash
  
echo Started
counter=1
while [ $counter -le 16 ]
do
  echo $counter
  cp -r HelpfulReviewDetector 'HelpfulReviewDetector'$counter
  find 'HelpfulReviewDetector'$counter/datasets ! -name 'Musical_Instruments_5_label'$counter'.csv' -type f -exec rm -f {} +
  mv 'HelpfulReviewDetector'$counter/datasets/'Musical_Instruments_5_label'$counter'.csv' 'HelpfulReviewDetector'$counter/datasets/'Musical_Instruments_5_label.csv'
  ((counter++))
done
echo Finished
