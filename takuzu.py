# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 11:
# 99059 Carlota Tracana
# 99082 Henrique Silva

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

#python3 takuzu.py <instance_file>
class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = np.copy(board)
        self.size = 0
        self.half_size = 0
        self.free_spc = 0


    def __lt__(self, other):
        return self.state_id < other.state_id

    # TODO: outros metodos da classe

class Board:
    """Representação interna de um tabuleiro de Takuzu."""
    def __init__(self):
        self.bd = []

    def get_number(self, row: int, col: int):
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self[row][col]

    def adjacent_vertical_numbers(self, row: int, col: int, max_len:int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        if(row != 0 and row != max_len - 1 and self[row-1][col] == self[row][col] and self[row][col] == self[row+1][col]):
            return True
        return False

    def adjacent_horizontal_numbers(self, row: int, col: int, max_len:int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if(col != 0 and col != max_len - 1 and self[row][col-1] == self[row][col] and self[row][col] == self[row][col+1]):
            return True
        return False

    def ck_adjacent_vertical_numbers(self, row: int, col: int, max_len:int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        if(row != 0 and row != max_len - 1 and self[row-1][col] != 2 and self[row][col] == 2 and self[row-1][col] == self[row+1][col]):
            return True
        return False
    
    def ck_adjacent_horizontal_numbers(self, row: int, col: int, max_len:int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        if(col != 0 and col != max_len - 1 and self[row][col] == 2 and self[row][col-1] != 2 and self[row][col-1] == self[row][col+1]):
            return True
        return False

    def up_numbers(self, row:int, col:int):
        if(row > 1 and self[row-1][col] != 2 and self[row][col] == 2 and self[row-1][col] == self[row-2][col]):
            return True
        return False
    
    def down_numbers(self, row:int, col:int, max_len:int):
        if(row < max_len - 2 and self[row+1][col] != 2 and self[row][col] == 2 and self[row+1][col] == self[row+2][col]):
            return True
        return False

    def left_numbers(self, row:int, col:int):
        if(col > 1 and self[row][col-1] != 2 and self[row][col] == 2 and self[row][col-1] == self[row][col-2]):
            return True
        return False

    def right_numbers(self, row:int, col:int, max_len:int):
        if(col < max_len - 2 and self[row][col+1] != 2 and self[row][col] == 2 and self[row][col+1] == self[row][col+2]):
            return True
        return False

    

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board."""
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
        """O construtor especifica o estado inicial."""
        self.initial = TakuzuState(np.array(board.bd))
        self.initial.size = len(board.bd)
        if(self.initial.size % 2 == 0):
            self.initial.half_size = self.initial.size / 2
        else:
            self.initial.half_size = (self.initial.size - 1) / 2 + 1
        self.initial.free_spc = np.count_nonzero(np.array(board.bd) == 2)

    def check_row(self, board, max_len, half_size):
        """Verifica se existe uma linha com uma posicao vazia e com um numero de zeros maior
        que uns ou vice versa"""
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
        """Verifica se existe uma coluna com uma posicao vazia e com um numero de zeros maior
        que uns ou vice versa"""
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
        """Verifica se existem 2 posicoes consecutivas iguais"""
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

                elif(Board.ck_adjacent_horizontal_numbers(board, row, col, max_len)):
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
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
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
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        new_state = TakuzuState(state.board)
        new_state.state_id = state.state_id + 1
        new_state.size = state.size
        new_state.half_size = state.half_size
        new_state.free_spc = state.free_spc - 1
        new_state.board[action[0]][action[1]] = action[2]
        return new_state
    
    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
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

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        value = np.count_nonzero(np.array(node.state.board) == 2) * 2
        value += np.count_nonzero(np.array(node.state.board) == 1)
        return value


if __name__ == "__main__":
    board = Board.parse_instance_from_stdin()
    problem = Takuzu(board)
    #compare_searchers(problems = [problem], header = ['Searcher', 'Nós'])
    final = depth_first_tree_search(problem)
    for row in range(final.state.size):
        for col in range(final.state.size):
            if(col < final.state.size - 1):
                print('{}'.format(final.state.board[row][col]), end='\t')
                
            else:
                print('{}'.format(final.state.board[row][col]), end='\n')
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

