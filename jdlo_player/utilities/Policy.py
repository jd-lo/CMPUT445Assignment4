"""
Policy.py

Implements the policy for a simulation given a game state.
"""

from board import GoBoard
from Classifier import Classifier, WIN, BLOCK, OPEN, CAP, TRIPLE, NOMATCH
from random import choice, random

class Policy:
    
    #random shit goes here that a board might need to evaluate for.

    def getPolicyMove(self, board: GoBoard) -> int:
        '''
        Returns the move to play given a board state.
        '''

        #NOTE: It may not be worth the computational power required to heuristically evaluate the board so many times

        #TODO: Implement psuedo-decay (more pieces roughly means deeper game, therefore rely less on heuristics)

        #e.g)
        #   classifiedMoves = {
        #       WIN: [(18, 1), (3, 1)],
        #       BLOCK: [(4, 0.53), (2, 0.22), (45, 0.41)]
        #       OPEN: [(15, 1), (17, 1)]
        #       CAP: [(26, 1), (8, 0.78)]                   26 may capture 4 stones and put us above the threshold for example, while 8 may only capture 2, putting us at 8
        #       TRIPLE: [(34, 0.76)]                        Triples are good because they can't be captured, and may threaten open four.
        #       NOMATCH: [(23, 0.4), (39, 0.33)]            This was up to random in a3, but now we'll choose the one with the best heuristic eval. 
        # }

        classifiedMoves = Classifier.classifier(board) #Returns a tuple value of heuristic/exact evaluation, move

        get = lambda key : classifiedMoves.get(key, None)

        if get(WIN):
            return get(WIN)[0]
        elif get(BLOCK):
            return self.heuristicSort(get(BLOCK))[0]
        elif get(OPEN):
            return get(OPEN)[0]
        elif get(TRIPLE) or get(CAP):
            combined = classifiedMoves[TRIPLE] + classifiedMoves[CAP]  #TODO: Weigh s.t for low capture amounts, triples are better, for high capture amounts, captures are better.
            return self.heuristicSort(combined)[0]
        else:
            return self.heuristicSort(get(NOMATCH))[0]

    def heuristicSort(self, unranked: list):
        return sorted(unranked, key = lambda x: x[1], reverse = True)
    
    def fixedOrRand(self, movelist: list, board: GoBoard):
        '''
        Returns a value given how many stones are on the board (roughly corresponding to depth) 
        Very many stones (complicated), favour randomness.
        (Only for classifications that aren't obvious wins)
        '''

        #Some equation that maps stone count to probability to play random move
        #if random() > p:
        #   return choice(movelist)
        #else:
        #   return self.heuristicSort(movelist)[0] #best heuristic eval

        raise NotImplementedError
        
