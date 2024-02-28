from Board import Board, Action
from numpy import array



def main():
    
    # random initial state
    
    #b = Board()
    b = Board(array([[2, 2, 0, 0], [2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]))
    print(b)
    b.perform_action(Action.UP)
    print(b)
    # b.add_new_number()
    # print(b)
    #b.reverse_mat()
    #print(b)



if __name__ == "__main__":
    main()