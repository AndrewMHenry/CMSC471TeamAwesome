#!/bin/bash
NUM_DISCRETE_QUESTIONS=5
TQ_PATH=$(pwd)
FILE_NAME="report_player_weights.txt"
> $TQ_PATH/saved-logs/$FILE_NAME
for value in {0..20}
do
  YEAR_WEIGHT=$(($RANDOM%101))
  RUNTIME_WEIGHT=$(($RANDOM % (100 - YEAR_WEIGHT)))
  RATING_WEIGHT=$((100 - RUNTIME_WEIGHT - YEAR_WEIGHT))
  JSON="{\"year\":$YEAR_WEIGHT,\"runtime\":$RUNTIME_WEIGHT,\"rating\":$RATING_WEIGHT}"
  echo $JSON > $TQ_PATH/tq/continuous_weights.json
  echo "Year weight: $YEAR_WEIGHT, Runtime weight: $RUNTIME_WEIGHT, Rating weight: $RATING_WEIGHT" >> $TQ_PATH/saved-logs/$FILE_NAME
  player -d $NUM_DISCRETE_QUESTIONS -w $TQ_PATH/tq/continuous_weights.json --train >> $TQ_PATH/saved-logs/$FILE_NAME
done
