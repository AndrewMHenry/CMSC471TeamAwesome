Team Awesome's AI project.

Dependencies
-------------------
Dependencies can be found in the setup.py file. 
Some dependencies might not install correctly through
the setup.py so commands to manually install some dependency
have been provided.

Set up SciKit manually
----------------------
1.Requires NumPy and SciPy installed
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
