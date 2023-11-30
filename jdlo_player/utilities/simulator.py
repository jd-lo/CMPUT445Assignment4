"""
simulator.py

Implements a MCTS Simulator for Ninuki, given a Board object.
- For legal moves, order moves in terms of their heuristic potential for simulations.
    > Moves with Win, Winblock, OpenFour, Capture to limit can be played immediately, without any simulation. (Classifier.py)

The board uses a 1-dimensional representation with padding
"""

#Convert the board as a 2D matrix.

from Policy import Policy
from board import GoBoard
from math import log as ln, sqrt
from time import time
from board_base import opponent, EMPTY


class searchNode:

    expConstant = sqrt(2)

    def __init__(self, index: int, parent = None, unexplored: list = []):
        #Parent is none for root node, depth dictates how deep to go until we simulate.
        self.parent = parent
        self.moveIndex = index
        self.children = []
        self.unexplored = unexplored #TODO: Implement get_legal_moves
        self.visits = 0
        self.wins = 0
    
    def getWinRate(self):
        return self.wins / self.visits
    
    def getVisits(self):
        return self.visits

    def UCB1(self):
        #Returns the UCB score of the node
        wr = self.getWinRate()
        parentVisits = self.parent.getVisits()

        ucbScore = wr + self.expConstant * sqrt(ln(parentVisits) / self.visits)
        return ucbScore

    def update(self, outcome):
        self.wins += outcome
        self.visits += 1

class MCTS:

    policy = ...

    def __init__(self, board: GoBoard, timeLimit: int):
        self.root = searchNode(board.last_move, parent = None, moves = board.get_legal_moves())
        self.state = board

        #Add small buffer to be extra safe and avoid timing out.
        self.buffer = timeLimit * (1/12)
        self.timeLimit = timeLimit - self.buffer

    def run(self) -> int:
        '''
        Runs MCTS until time constraint is reached.
        returns:
            Index of best move (int)
        '''

        startTime = time()
        elapsed = startTime
        selectedNode = self.root

        while elapsed - startTime < self.timeLimit:
            
            #Plays moves on the board (Including new child nodes)
            selectedNode = self.traverse(self.root)         
            outcome = self.rollout()

            #Undoes the moves from traversal
            self.backpropagate(selectedNode, outcome)

            elapsed += (time() - elapsed) #Increment the time taken
        
        bestChild = max(self.children, key = lambda node: node.UCB1)
        return bestChild.moveIndex

    def rollout(self) -> float:
        '''
        The "Rollout/Simulation" phase of MCTS. Plays remaining game from a gamestate according to simulation policy. Returns whether it was a win or loss.
        returns:
            outcome of the simulation (1 for win, 0 for loss, 0.01 for draw)
        '''
        simulation = self.state.copy()

        while not simulation.end_of_game():
            pointToPlay = Policy.getPolicyMove(simulation)
            simulation.play_move(pointToPlay, simulation.current_player)
        
        if simulation.winner == self.state.current_player:
            return 1
        elif simulation.winner == EMPTY:
            return 0.01
        else:
            return 0

    def backPropagate(self, node: searchNode, outcome) -> None:
        '''
        The "Update/BackProp" phase of MCTS. Undoes any moves made during traversal.
        args:
            node: The leaf node of the MCT traversal
        '''

        while node:
            node.update(outcome)

            #Traverse up the tree
            node = node.parent

            #Undo move (eventually getting back to original position)
            self.state.undo()
    
    def traverse(self, node: searchNode) -> searchNode:
        '''
        The "Selection" and "Expansion" phase of MCTS. Plays moves on the board
        Recursive implementation to find the best node to explore next based of UCB score.
        '''
        #Base case: Leaf node; no children. Add a node by selecting a child (Expansion)
        if not node.children:
            selectedMove: int = node.unexploredMoves.pop(0)
            self.state.play_move(selectedMove, self.state.current_player)

            newLeaf = searchNode(selectedMove, parent = node, moves = node.unexploredMoves)
            node.children.append(newLeaf)

            return newLeaf

        #Inductive step: Choose the best child and traverse to it. (Selection)
        bestChild = max(self.children, key = lambda node: node.UCB1)

        #Play the move on the board.
        self.initialState.play_move(node.moveIndex, self.initialState.current_player)
        self.traverse(bestChild)






    
