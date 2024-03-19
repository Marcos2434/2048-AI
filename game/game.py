from Board import Board, Actions
from numpy import array
from ai import Player, expectimax
from time import sleep
from enum import Enum
import tkinter.messagebox as messagebox

n_games = 10
depth = 4 # cutoff depth (only even values make sense, as we cannot predict chance's moves)

class gameType(Enum):
    AI = 0
    USER = 1
    PERFORMANCE_TEST = 2

game = gameType.AI

UP_KEYS = ('w', 'W', 'Up')
LEFT_KEYS = ('a', 'A', 'Left')
DOWN_KEYS = ('s', 'S', 'Down')
RIGHT_KEYS = ('d', 'D', 'Right')
FONT = ('Verdana', 24, 'bold')




from GUI.gui import Grid, GamePanel

def main():    
    size = 4
    grid = Grid(size)
    panel = GamePanel(grid)
    b = Board()
    
    def key_handler(event):
        key_value = event.keysym
        print('{} key pressed'.format(key_value))
        if key_value in UP_KEYS:
            b.perform_action(Actions.UP)
        elif key_value in LEFT_KEYS:
            b.perform_action(Actions.LEFT)
        elif key_value in DOWN_KEYS:
            b.perform_action(Actions.DOWN)
        elif key_value in RIGHT_KEYS:
            b.perform_action(Actions.RIGHT)
        else:
            pass

        panel.paint(b.state)
        
        # print('Score: {}'.format(grid.current_score))
        # if self.grid.found_2048():
        #     print('You Win!')
        #     if messagebox.askyesno('2048', 'You Win!\n'
        #                                 'Are you going to continue the 2048 game?'):

        # if self.grid.moved:
        #     self.grid.random_cell()

        # self.panel.paint()
        # if not self.can_move():
        #     self.over = True
        #     self.game_over()
    
    
    

    
    match game:
        case gameType.USER:
            print(b)
        
            # # Ask user for action (this will be replaced by AI)
            # action = input("Enter action, 'q' to quit: ")
            # while action != 'q':
            #     if action == 'a':
            #         b.perform_action(Actions.LEFT)
            #     elif action == 's':
            #         b.perform_action(Actions.DOWN)
            #     elif action == 'd':
            #         b.perform_action(Actions.RIGHT)
            #     elif action == 'w':
            #         b.perform_action(Actions.UP)

            #     print(b)
                
            #     # Ask for new action
            #     action = input("Enter action, 'q' to quit: ")
            
            panel.paint(b.state)
            panel.root.bind('<Key>', key_handler)
            panel.root.mainloop()
            
        case gameType.AI:
            print("AI Playing...\n")
            b = Board()
            print(b)

            won = False
            while not b.terminal_test():
                moves = {}
                for a in Actions:
                    new_board : Board = b.copy()
                    if new_board.perform_action(a): # if action is valid     
                        e = expectimax(new_board, Player.MAX, depth)
                        moves.update({a: e})
                print("Expected ", e)
                best_move = max(moves, key=lambda k: moves[k])

                b.perform_action(best_move)
                print(f"Best move: {best_move}")
                print(b)
                panel.paint(b.state)
                panel.root.update()
                # panel.root.mainloop()
                if b.goal_test():
                    print("You won! :)")
                    won = True
                print()
            
            if not won:
                print("Game over :( You suck.")
            print("Score: ", b.score)
            panel.root.mainloop()
            
        case gameType.PERFORMANCE_TEST:
            scores = []
            for i in range(n_games):
                b = Board()
                while not b.terminal_test():
                    moves = {}
                    for a in Actions:
                        new_board : Board = b.copy()
                        if new_board.perform_action(a):
                            moves.update({a: expectimax(new_board, Player.MAX, depth)})
                    best_move = max(moves, key=lambda k: moves[k])
                    b.perform_action(best_move)
                print(f"Game {i} Score: ", b.score)
                scores.append(b.score)
            avg_score = sum(scores)/n_games
            print("Average Game Score: ", avg_score)



if __name__ == "__main__":
    main()