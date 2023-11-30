"""
evaluator.py

Implements a hieuristic function for a Ninuki state, given a Board object.

General Ideas:
    - Wins, OpenFour, Capture to Limit give MAX hieristic evaluation. (MIN if opponent has this)
    - Captured stones should not be weighed equally. The 8th stone(s) captured are far more valuable than the 2nd stone(s)
    - Likewise, existing stones should be summed up. Three stones connected is more valuable than a stand-alone.

The board uses a 1-dimensional representation with padding
"""

#May not even be neccessary for MCTS purposes
from classifier import Classifier

class Evaluator