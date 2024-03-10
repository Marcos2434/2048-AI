import numpy as np
from numpy.typing import ArrayLike
from enum import Enum
from Board import Board, Actions
from copy import deepcopy

# Possibly apply machine learning to figure out the best weights for the utility function
# (also consider snake-shaped position weights)
# POSITION_WEIGHTS = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
POSITION_WEIGHTS = np.array([[0, 1, 2, 3], [1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]])
MONOTONICITY_WEIGHT = 0
MAX_TILE_BONUS_WEIGHT = 0
EMPTY_CELLS_BONUS_WEIGHT = 0

class Player(Enum):
    MAX = 0
    CHANCE = 1

class ChanceActions(Enum):
    ADD_2 = 2
    ADD_4 = 4

def utility(s : Board, p : Player) -> int:
    """
    Utility for terminal test is anallogous to eval for cutoff test

    A simple utility function for 2048 could be the sum of the values 
    of all tiles on the board. However, more sophisticated utility 
    functions might take into account factors such as the arrangement 
    of tiles, availability of larger tiles, and potential for future moves.
    """
    
    # these are found by using current state s
    score = 0
    max_tile = 0
    empty_cells = 0

    for row in s.state:
        for cell in row:
            score += cell
            if cell > max_tile:
                max_tile = cell
            if cell == 0:
                empty_cells += 1
    
    position_weights = POSITION_WEIGHTS
    
    if p == Player.MAX:
        # Weighted sum based on position
        for i in range(s.state.shape[0]):
            for j in range(s.state.shape[1]):
                score += s.state[i][j] * position_weights[i][j]
        
        # Monotonicity score
        def calculate_monotonicity_score(s):
            """
            Monotonicity is a measure of how the values of the tiles 
            are arranged in a non-decreasing order along the rows and 
            columns of the board. This is a desirable property because 
            it allows for easier merging of tiles and thus higher scores.
            """
            score = 0
            for i in range(s.state.shape[0]):
                for j in range(s.state.shape[1]-1):
                        if s.state[i][j] >= s.state[i][j+1]:
                            score += s.state[i][j] - s.state[i][j+1]
                        if s.state[j][i] >= s.state[j+1][i]:
                            score += s.state[j][i] - s.state[j+1][i]
            return score
        
        monotonicity_score = calculate_monotonicity_score(s)
        score += monotonicity_score * MONOTONICITY_WEIGHT
        
        # Bonus for larger tiles
        max_tile_bonus_weight = MAX_TILE_BONUS_WEIGHT
        score += max_tile * max_tile_bonus_weight
        
        # Bonus for empty cells
        empty_cells_bonus_weight = EMPTY_CELLS_BONUS_WEIGHT
        score += empty_cells * empty_cells_bonus_weight
    return score
    

def result(s: Board, a: Actions, p : Player) -> set[Board]:
    """
    Returns the resulting state from applying action a to state s
    """
    new_board : Board = s.copy()
    match p:
        case Player.MAX:
            
            new_board.perform_action(a, addNewNumber = False)
            return new_board
        case Player.CHANCE:
            # Initiate set   
            uniques : set[Board] = set()
            
            # If empty cell, add 2 and 4 to the cell and add to set 
            for i in range(new_board.state.shape[0]):
                for j in range(new_board.state.shape[1]):
                    if new_board.state[i, j] == 0:
                        tmp = new_board.copy()
                        tmp.state[i, j] = a.value
                        uniques.add(tmp)
            return uniques

    
def P(a : ChanceActions) -> float:
    """
    Returns the probability of chance chosing action a in s.
    
    s unused because the probability is independent of the state.
    """
    return 0.9 if a == ChanceActions.ADD_2 else 0.1


def expectimax(s : Board, p: Player, d : int) -> int:
    if s.is_cutoff(d): return utility(s, p)
    elif p == Player.MAX:
        return max([expectimax(result(s, a, p), Player.CHANCE, d-1) for a in Actions])
    # elif p == P layer.CHANCE: 
    #     outcomes = [(P(a), expectimax(result(s, a, p), Player.MAX, d-1)) for a in ChanceActions]
    #     return sum(prob * value for prob, value in outcomes) / (len(outcomes) / 2)
    elif p == Player.CHANCE:
        outcomes = []
        for a in ChanceActions:
            for r in result(s, a, p):
                outcomes.append((P(a), expectimax(r, Player.MAX, d-1)))
        if len(outcomes) == 0:
            return 0
        return sum(prob * value for prob, value in outcomes) / (len(outcomes) / 2)



