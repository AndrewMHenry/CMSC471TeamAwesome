#!/bin/bash
NUM_DISCRETE_QUESTIONS=5
REDUCE_FACTOR=20
TQ_PATH=$(pwd)
FILE_NAME="report_test.txt"
> $TQ_PATH/saved-logs/$FILE_NAME
echo "Running test on twenty questions based on optimal values" >> $TQ_PATH/saved-logs/$FILE_NAME 
player -r $REDUCE_FACTOR -d $NUM_DISCRETE_QUESTIONS -w $TQ_PATH/tq/continuous_weights.json --test >> $TQ_PATH/saved-logs/$FILE_NAME
