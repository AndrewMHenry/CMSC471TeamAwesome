#!/bin/bash
TQ_PATH=$(pwd)
echo $TQ_PATH
> $TQ_PATH/saved-logs/report_player.txt
for value in {0..20}
do
  echo "Number of Discrete Questions: $value" >> $TQ_PATH/saved-logs/report_player.txt
  player -d $value >> $TQ_PATH/saved-logs/report_player.txt
done
