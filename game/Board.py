import numpy as np
from numpy.typing import ArrayLike
import random as rand
from copy import deepcopy

from enum import Enum

class Actions(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Board:
    def __init__(self, init_state : ArrayLike = None) -> None:
        self.state = self.generate_init_state() if init_state is None else init_state
        self.score = 0
    
    def copy(self):
        return deepcopy(self)
    
    def is_cutoff(self, d : int) -> bool:
        return d == 0
    
    def __str__(self) -> str:
        return str(self.state)
    
    def generate_init_state(self) -> ArrayLike:
        values = [2, 4]
        probabilities = [0.9, 0.1]

        val1 = rand.choices(values, probabilities, k=1)[0]
        val2 = rand.choices(values, probabilities, k=1)[0]
        
        r1 = rand.randint(0,3)
        r2 = rand.randint(0,3)
        c1 = rand.randint(0,3)
        c2 = rand.randint(0,3)
        
        while (r1 == r2 and c1 == c2):
            r2 = rand.randint(0,3)
            c2 = rand.randint(0,3)
        
        b = np.array([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        b[r1,c1] = val1
        b[r2,c2] = val2
        
        return b
    
    def goal_test(self) -> bool:
        for i in range(self.state.shape[0]):
            for j in range(self.state.shape[1]):
                if self.state[i,j] == 2048:
                    return True
        return False

    def terminal_test(self) -> bool:
        # There are empty squares
        for i in range(self.state.shape[0]):
            for j in range(self.state.shape[1]):
                if self.state[i,j] == 0:
                    return False
        # Two neighbors are the same
        # for i in range(1, self.state.shape[0]-1):
        #     for j in range(1, self.state.shape[1]-1):
        #         if (self.state[i, j] == self.state[i, j+1]) or (self.state[i, j] == self.state[i, j-1]) or (self.state[i, j] == self.state[i+1, j]) or (self.state[i, j] == self.state[i-1, j]):
        #             return False
            # Check for possible merges in rows
        for row in self.state:
            for i in range(len(row) - 1):
                if row[i] == row[i + 1]:
                    return False

        # Check for possible merges in columns
        for col in zip(*self.state):
            for i in range(len(col) - 1):
                if col[i] == col[i + 1]:
                    return False
        return True
            

    def rotate_clockwise(self):
        self.state = np.rot90(self.state, k=3)
    
    def rotate_counterclockwise(self):
        self.state = np.rot90(self.state, k=1)
    
    def reverse_mat(self):
        self.state = np.fliplr(self.state)

    #def is_valid_action(self, a: Actions) -> bool:
    #    old_state : Board = self.copy()
    #    old_state.perform_action(a)
    #    changed = False
    #    for i in range(self.state.shape[0]):
    #        for j in range(self.state.shape[1]):
    #            if old_state[i,j] != self.state[i,j]:
    #                changed = True
        
    
    def perform_action(self, action : Actions, addNewNumber = True) -> bool:
        """
        Save copy of old state (maybe find better solution for this)
        The purpose is to not add a new number if the action performed is not allowed (i.e. trying to move
        right when all numbers are already to the right and no same numbers are neighbors).
        """
        
        old_state = deepcopy(self.state)

        def tryMoveRight(i, j, merge_counter):
            # is the cell a 0 or are we on the last column?
            if self.state[i, j] == 0 or j == self.state.shape[1]-1:
                return
            
            if self.state[i, j+1] == 0:
                self.state[i, j+1] = self.state[i, j]
                self.state[i, j] = 0
                tryMoveRight(i, j+1, merge_counter)
            elif self.state[i, j+1] == self.state[i, j]:
                if merge_counter >= 1: return
                self.state[i, j+1] *= 2
                # Add the merged numbers to the score
                self.score += self.state[i, j+1]
                self.state[i, j] = 0
                tryMoveRight(i, j+1, merge_counter+1)
        

        if action == Actions.UP:
            self.rotate_clockwise()
            for j in range(self.state.shape[1]):
                for i in range(self.state.shape[0]):
                    tryMoveRight(i, j, 0)
            self.rotate_counterclockwise()
            
        elif action == Actions.DOWN:
            self.rotate_counterclockwise()
            for j in range(self.state.shape[1]-1, -1, -1):
                for i in range(self.state.shape[0]-1, -1, -1):
                    tryMoveRight(i, j, 0)
            self.rotate_clockwise()
            
        elif action == Actions.LEFT:
            self.reverse_mat()
            for i in range(self.state.shape[0]):
                # Iterate from the right:
                for j in range(self.state.shape[1]-1, -1, -1):
                    tryMoveRight(i, j, 0)
            self.reverse_mat()

        elif action == Actions.RIGHT:
            for i in range(self.state.shape[0]):
                # Iterate from the right:
                for j in range(self.state.shape[1]-1, -1, -1):
                    tryMoveRight(i, j, 0)

        changed = False
        for i in range(self.state.shape[0]):
            for j in range(self.state.shape[1]):
                if old_state[i,j] != self.state[i,j]:
                    changed = True

        # if self.terminal_test(): 
        #     print("\nYou lost\n")
        #     return True
        if changed:
            # if self.goal_test():
            #     print("\nYou won!\n")
            if addNewNumber: self.add_new_number()
            return True   
        # If the action did not change the state, then the action was not valid
        return False
            
    def add_new_number(self):
        values = [2, 4]
        probabilities = [0.9, 0.1]

        new_number = rand.choices(values, probabilities, k=1)[0]

        row = rand.randint(0,3)
        column = rand.randint(0,3)

        while(self.state[row,column] != 0):
            row = rand.randint(0,3)
            column = rand.randint(0,3)

        self.state[row, column] = new_number
