Team Awesome's AI project.

Dependencies
-------------------
Dependencies can be found in the setup.py file. 
Some dependencies might not install correctly through
the setup.py so commands to manually install some dependency
have been provided.

Set up SciKit manually
----------------------
1. Requires NumPy and SciPy installed
```
python3 -m pip install --user numpy scipy
```
2. Install SciKit
```
python3 -m pip install --user -U scikit-learn
```

Set up Project automatically
---------------------------
1. Set up project 
```
pip3 install --upgrade --user -e .
```
in the root directory of this project, which should
automatically install twenty questions and its dependencies.

2. Run the game
```
twenty
```
Typing the command twenty will run the project.


Training & Testing Project
----------------------------
To verify that our model is performing as expected, there
are shell scripts written to run our python code. The shell scripts
will generate logs that appear in the saved-logs folder to indicate 
the accuracy of the model. The code is set up to split the training data
has 80% of the entire data and the test data as 20%. The training
indicates the optimal number of discrete questions and continuous weights
to use.

1. To figure out the optimal number of discrete questions to ask within
the 20 questions, use the runplayer.sh
```
./runplayer.sh
```
This script generates report_player.txt and shows the number of discrete
questions that yields the highest accuracy

2. To figure out the weights of the continuous features, use
runplayer_weight.sh 
```
./runplayer_weight.sh
```
This script generates report_player_weights.txt and shows the best
weight to use on the continuous features

3. To perform the testing after the training has been completed,
use runtest.sh
```
./runtest.sh
```
