from Board import Board, Actions
from numpy import array
from ai import Player, expectimax
from time import sleep

userPlaying = False
n_games = 100

def main():
    scores = []
    for i in range(n_games):
    
        # random initial state
        #b = Board(array([[16, 4, 2, 8], [4, 2, 32, 8], [16, 4, 128, 2], [2, 16, 8, 2]]))
        b = Board()
        #print(b)

        if userPlaying:
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
        else:
            # AI playing
            # while not b.terminal_test():
            
            depth = 1 # cutoff depth
            while not b.terminal_test():
                moves = {}
                for a in Actions:
                    new_board : Board = b.copy()
                    if new_board.perform_action(a): # if action is valid     
                        moves.update({a: expectimax(new_board, Player.MAX, depth)})
                best_move = max(moves, key=lambda k: moves[k])

                b.perform_action(best_move)
                #print(f"Best move: {best_move}")
                #print(b)
                if b.goal_test():
                    #print("You won! :)")
                    break
                #print()

            #print("Game over :( You suck.")
            #print("Score: ", b.score)
            #print(scores)
            scores.append(b.score)
    
    avg_score = sum(scores)/n_games
    print(scores)
    print(avg_score)


if __name__ == "__main__":
    main()