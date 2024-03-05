import Board
import numpy as np
from enum import Enum

# Possibly apply machine learning to figure out the best weights for the utility function
# (also consider snake-shaped position weights)
POSITION_WEIGHTS = np.array([[0, 1, 2, 3], [1, 2, 3, 4], [2, 3, 4, 5], [3, 4, 5, 6]])
MONOTONICITY_WEIGHT = 10
MAX_TILE_BONUS_WEIGHT = 10
EMPTY_CELLS_BONUS_WEIGHT = 10

class Player(Enum):
    MAX = 0
    CHANCE = 1

def utility(s : Board, p : Player) -> int:
    """
    Utility for terminal test is analogous to eval for cutoff test

    A simple utility function for 2048 could be the sum of the values 
    of all tiles on the board. However, more sophisticated utility 
    functions might take into account factors such as the arrangement 
    of tiles, availability of larger tiles, and potential for future moves.
    """
    
    # these are found by using current state s
    score = s.score
    max_tile = s.state.max()
    empty_cells = 0

    for row in s.state:
        for cell in row:
            #score += cell
            #if cell > max_tile:
            #    max_tile = cell
            if cell == 0:
                empty_cells += 1
    
    position_weights = POSITION_WEIGHTS
    
    if p == Player.MAX:
        # Weighted sum based on position
        for i in range(s.size):
            for j in range(s.size):
                score += s.state[i][j] * position_weights[i][j]
        
        # Monotonicity score
        def calculate_monotonicity_score():
            """
            Monotonicity is a measure of how the values of the tiles 
            are arranged in a non-decreasing order along the rows and 
            columns of the board. This is a desirable property because 
            it allows for easier merging of tiles and thus higher scores.
            """
            score = 0
            for i in range(s.size):
                for j in range(s.size-1):
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
    

def expectimax(s : Board, p: Player) -> int:
    if s.terminal_test():
        return utility(s, p)