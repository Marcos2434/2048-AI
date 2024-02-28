import numpy as np
from numpy.typing import ArrayLike
import random as rand

from enum import Enum

class Action(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3

class Board:
    def __init__(self, init_state : ArrayLike = None) -> None:
        self.state = self.generate_init_state() if init_state is None else init_state
    
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

            
        
    def rotate_clockwise(self):
        self.state = np.rot90(self.state, k=3)
    
    def rotate_counterclockwise(self):
        self.state = np.rot90(self.state, k=1)
    
    def perform_action(self, action : Action):

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
                self.state[i, j] = 0
                tryMoveRight(i, j+1, merge_counter+1)
        

        if action == Action.UP:
            self.rotate_clockwise()
            for j in range(self.state.shape[1]):
                for i in range(self.state.shape[0]):
                    tryMoveRight(i, j, 0)
            self.rotate_counterclockwise()
            
        elif action == Action.DOWN:
            self.rotate_counterclockwise()
            for j in range(self.state.shape[1]-1, -1, -1):
                for i in range(self.state.shape[0]-1, -1, -1):
                    tryMoveRight(i, j, 0)
            self.rotate_clockwise()
            
        elif action == Action.LEFT:
            self.reverse_mat()
            for i in range(self.state.shape[0]):
                # Iterate from the right:
                for j in range(self.state.shape[1]-1, -1, -1):
                    tryMoveRight(i, j, 0)
            self.reverse_mat()

        elif action == Action.RIGHT:
            for i in range(self.state.shape[0]):
                # Iterate from the right:
                for j in range(self.state.shape[1]-1, -1, -1):
                    tryMoveRight(i, j, 0)
                    
        self.add_new_number()
        if self.goal_test(): print("You won!")
            
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

    def reverse_mat(self):
        self.state = np.fliplr(self.state)