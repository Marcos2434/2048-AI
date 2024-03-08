from Board import Board, Actions
from numpy import array
from ai import Player, expectimax
from time import sleep
from enum import Enum

n_games = 20

depth = 1 # cutoff depth

class gameType(Enum):
    AI = 0
    USER = 1
    PERFORMANCE_TEST = 2

game = gameType.PERFORMANCE_TEST

def main():
    match game:
        case gameType.USER:
            b = Board()
            print(b)
        
            # Ask user for action (this will be replaced by AI)
            action = input("Enter action, 'q' to quit: ")
            while action != 'q':
                if action == 'a':
                    b.perform_action(Actions.LEFT)
                elif action == 's':
                    b.perform_action(Actions.DOWN)
                elif action == 'd':
                    b.perform_action(Actions.RIGHT)
                elif action == 'w':
                    b.perform_action(Actions.UP)

                print(b)
                
                # Ask for new action
                action = input("Enter action, 'q' to quit: ")
        case gameType.AI:
            b = Board()
            print(b)
            won = False
            while not b.terminal_test():
                moves = {}
                for a in Actions:
                    new_board : Board = b.copy()
                    if new_board.perform_action(a): # if action is valid     
                        moves.update({a: expectimax(new_board, Player.MAX, depth)})
                best_move = max(moves, key=lambda k: moves[k])

                b.perform_action(best_move)
                print(f"Best move: {best_move}")
                print(b)
                if b.goal_test():
                    print("You won! :)")
                    won = True
                    break
                print()
            
            if not won:
                print("Game over :( You suck.")
            print("Score: ", b.score)
            
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