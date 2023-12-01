"""
Heuristic.py

Implements a rough heuristic for a game state.
"""

from board import GoBoard
from board_base import opponent

class Heuristic:

    @staticmethod
    def decay(mul, b, exp):
        return mul * pow(b, exp)
        
    def heuristicEval(self, board: GoBoard, classifications) -> float:
        result = 0

        #1/2 the score contribution will come from captures
        captureScore = self._captureScore(board)
        if abs(captureScore) == 1:
            #captureScore was evaluated to be an exact win/loss
            return captureScore

        #1/2 the score contribution will come from evaluation of classified moves.
        moveScore = self._moveScore(classifications)
        if abs(moveScore) == 1:
            #moveScore was evaluated to be an exact win/loss
            return moveScore

        result = (0.5 * captureScore) + (0.5 * moveScore)
        
        assert -1 <= result <= 1

    def _boardScore(self, classifications) -> float:

        scoreSum = lambda x : values.get(x) * len(classifications.get(x))

        scoreWeights = {
                CAP: 0.1,
                TRIPLE: 0.075,
                NOMATCH: 0.001
            }
        
        if classifications.get(WIN) or classifications.get(OPEN):
            return 1
        elif len(classifications.get(BLOCK)) >= 2:
            #Can't block multiple threats
            return -1
        else:
            score = sum([scoreSum(score) for score in scoreWeights.keys()])
            #Avoid exact evaluation
            return min(score, 0.99)

    def _captureScore(self, board):
        
        #Swaps around s.t nth stone -> 10, 0th stone -> 0
        b = lambda x: 10 - board.get_captures(x)

        #Weigh the current player's captures slightly more
        if b(board.current_player) <= 0:
            return 1
        elif b(opponent(board.current_board)) <= 0:
            return -1
        else:
            score = self.decay(1, b(board.current_player), 0.85)
            opponentScore = self.decay(1, b(opponent(board.current_player)), 0.80)

        return score - opponentScore