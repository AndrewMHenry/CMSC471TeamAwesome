# suggestion based on StackOverflow
rm -f questions answers
mkfifo questions answers
twenty < answers | tee questions
player < questions | tee answers
