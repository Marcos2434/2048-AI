from Board import Board, Action
from numpy import array



def main():
    
    # random initial state
    b = Board()
    print(b)
    
    #b = Board(array([[2, 4, 8, 16], [4, 2, 32, 2], [0, 8, 16, 4], [16, 4, 32, 64]]))

    # Ask user for action (this will be replaced by AI)
    action = input("Enter action, 'q' to quit: ")
    while action != 'q':
        if action == 'j':
            b.perform_action(Action.LEFT)
        elif action == 'k':
            b.perform_action(Action.DOWN)
        elif action == 'l':
            b.perform_action(Action.RIGHT)
        elif action == 'i':
            b.perform_action(Action.UP)

        print(b)
        # Ask for new action
        action = input("Enter action, 'q' to quit: ")




if __name__ == "__main__":
    main()