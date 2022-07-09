# Made by:
# Carlota Tracana
# Henrique Silva

from operator import le
from pickle import TRUE
import numpy as np
from sys import stdin
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    compare_searchers,
    depth_first_graph_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)

class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = np.copy(board)
        self.size = 0
        self.half_size = 0
        self.free_spc = 0


    def __lt__(self, other):
        return self.state_id < other.state_id

class Board:
    """Internal representation of a takuzu board."""
    def __init__(self):
        self.bd = []

    def get_number(self, row: int, col: int):
        """Returns the value from a space on the board"""
        return self[row][col]

    def adjacent_vertical_numbers(self, row: int, col: int, max_len:int):
        """Checks if the values on top and bottom of a given space on the board are the same as
        the given position."""
        if(row != 0 and row != max_len - 1 and self[row-1][col] == self[row][col] and self[row][col] == self[row+1][col]):
            return True
        return False

    def adjacent_horizontal_numbers(self, row: int, col: int, max_len:int):
        """Checks if the values of the left and right spaces of a given position on the board 
        are the same as the one in the provided position."""
        if(col != 0 and col != max_len - 1 and self[row][col-1] == self[row][col] and self[row][col] == self[row][col+1]):
            return True
        return False

    def up_numbers(self, row:int, col:int):
        """Checks top positions."""
        if(row > 1 and self[row-1][col] != 2 and self[row][col] == 2 and self[row-1][col] == self[row-2][col]):
            return True
        return False
    
    def down_numbers(self, row:int, col:int, max_len:int):
        """Checks down positions."""
        if(row < max_len - 2 and self[row+1][col] != 2 and self[row][col] == 2 and self[row+1][col] == self[row+2][col]):
            return True
        return False

    def left_numbers(self, row:int, col:int):
        """Checks left positions."""
        if(col > 1 and self[row][col-1] != 2 and self[row][col] == 2 and self[row][col-1] == self[row][col-2]):
            return True
        return False

    def right_numbers(self, row:int, col:int, max_len:int):
        """Checks right positions."""
        if(col < max_len - 2 and self[row][col+1] != 2 and self[row][col] == 2 and self[row][col+1] == self[row][col+2]):
            return True
        return False

    

    @staticmethod
    def parse_instance_from_stdin():
        """Reads the test in standar input (stdin) which becomes and arg and returns
        board which is of class type Board."""
        num = int(stdin.readline())
        board = Board()
        #python3 takuzu.py < testes_takuzu.input_T01
        for i in range(num): 
            line = stdin.readline().split()
            line = list(map(int, line))
            board.bd.append(line)
        return board


class Takuzu(Problem):
    def __init__(self, board: Board):
        """Constructor specifies initial state."""
        self.initial = TakuzuState(np.array(board.bd))
        self.initial.size = len(board.bd)
        if(self.initial.size % 2 == 0):
            self.initial.half_size = self.initial.size / 2
        else:
            self.initial.half_size = (self.initial.size - 1) / 2 + 1
        self.initial.free_spc = np.count_nonzero(np.array(board.bd) == 2)

    def check_row(self, board, max_len, half_size):
        """Checks if a line, which has an empty position, has a sum of ones or zeros
        equal to half the amount of spaces in that line."""
        
        for row in range(max_len - 1, -1, -1):
            if (np.count_nonzero(board[row] == 1) == half_size):
                for col in range(max_len - 1, -1, -1):
                    if (board[row][col] == 2):
                        return [tuple([row, col, 0])]
            elif (np.count_nonzero(board[row] == 0) == half_size):
                for col in range(max_len - 1, -1, -1):
                    if (board[row][col] == 2):
                        return [tuple([row, col, 1])]
            
        return []

    def check_col(self, board, max_len, half_len):
        """Checks if a column, which has an empty position, has a sum of ones or zeros
        equal to half the amount of spaces in that column."""
        col_bd = np.transpose(board)
        for col in range(max_len - 1, -1, -1):
            if(np.count_nonzero(col_bd[col] == 1) == half_len):
                for row in range(max_len - 1, -1, -1):
                    if(col_bd[col][row] == 2):
                        return [tuple([row, col, 0])]

            elif(np.count_nonzero(col_bd[col] == 0) == half_len):
                for row in range(max_len - 1, -1, -1):
                    if(col_bd[col][row] == 2):
                        return [tuple([row, col, 1])]

        return []
    
    def check_three(self, board, max_len):#Returns an action
        """Checks if there are two positions with the same value(0 or 1)"""
        #Check cols first
        for row in range(max_len):
            for col in range(max_len):
                if(Board.up_numbers(board, row, col)):
                    if(board[row-1][col] == 1):
                        return [tuple([row, col, 0])]
                    else:
                        return [tuple([row, col, 1])]


                elif(Board.down_numbers(board, row, col, max_len)):
                    if(board[row+1][col] == 1):
                        return [tuple([row, col, 0])]
                    else:
                        return [tuple([row, col, 1])]


                elif(Board.left_numbers(board, row, col)):
                    if(board[row][col-1] == 1):
                        return [tuple([row, col, 0])]
                    else:
                        return [tuple([row, col, 1])]

                elif(Board.right_numbers(board, row, col, max_len)):
                    if(board[row][col+1] == 1):
                        return [tuple([row, col, 0])]
                    else:
                        return [tuple([row, col, 1])]

                elif(Board.adjacent_horizontal_numbers(board, row, col, max_len)):
                    if(board[row][col-1] == 1):
                        return [tuple([row, col, 0])]
                    else:
                        return [tuple([row, col, 1])]
                

                elif(Board.ck_adjacent_vertical_numbers(board, row, col, max_len)):
                    if(board[row-1][col] == 1):
                        return [tuple([row, col, 0])]
                    else:
                        return [tuple([row, col, 1])]
            
        return []
    
                
    def actions(self, state: TakuzuState): #(linha, coluna, val)
        """Returns a list of actions which can be executed from the state which was
        passed as an argument."""
        free_pos = []
        free_pos += self.check_row(state.board, state.size, state.half_size)
        if(free_pos != []):
            return free_pos
        free_pos += self.check_col(state.board, state.size, state.half_size)
        if(free_pos != []):
            return free_pos

        free_pos += self.check_three(state.board, state.size)
        if(free_pos != []):
            return free_pos

        for linha in range(state.size):
            for coluna in range(state.size):
                if(state.board[linha][coluna] == 2):
                    return [tuple([linha, coluna, 0]), tuple([linha, coluna, 1])]
        return free_pos

    def result(self, state: TakuzuState, action):#(linha, coluna, val)
        """Returns the state resulting from the execution of an 'action' on 'state'
        passed as an argument. The action to execute should be from the list of actions
        obtained from self.actions(state)."""
        new_state = TakuzuState(state.board)
        new_state.state_id = state.state_id + 1
        new_state.size = state.size
        new_state.half_size = state.half_size
        new_state.free_spc = state.free_spc - 1
        new_state.board[action[0]][action[1]] = action[2]
        return new_state
    
    def goal_test(self, state: TakuzuState):
        """Returns True only if the state passed as argument is an objective state. Checks if no
        takuzu rule is being broken."""
        #Teste de posiçoes seguidas com valores iguais
        if not(state.free_spc == 0):
            return False

        for linha in range(state.size):
            for coluna in range(state.size):
                if(Board.adjacent_horizontal_numbers(state.board, linha, coluna, state.size) or 
                    Board.adjacent_vertical_numbers(state.board, linha, coluna, state.size)):
                    return False
        check_col = np.transpose(state.board)
        if(len(np.unique(state.board, axis=0)) != state.size):
            return False
        elif(len(np.unique(check_col, axis=0)) != state.size):
            return False
            
        for num in range(state.size):
            if(np.count_nonzero(state.board[num] == 1) > state.half_size or np.count_nonzero(state.board[num] == 0) > state.half_size or
                np.count_nonzero(check_col[num] == 1) > state.half_size or np.count_nonzero(check_col[num] == 0) > state.half_size):
                return False 

        return True


if __name__ == "__main__":
    board = Board.parse_instance_from_stdin()
    problem = Takuzu(board)
    final = depth_first_tree_search(problem)
    for row in range(final.state.size):
        for col in range(final.state.size):
            if(col < final.state.size - 1):
                print('{}'.format(final.state.board[row][col]), end='\t')
                
            else:
                print('{}'.format(final.state.board[row][col]), end='\n')


