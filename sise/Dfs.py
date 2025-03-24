import copy
from traceback import print_tb
from Board import Board

#zminic get_possible_moves by przekazywac ostatni ruch
#zobaczyc jak dziala tuple i po co to jest
#visited tworzy sie przy kazdym wykonaniu

def dfs(board, path, max_depth, permutation, depth = 0, visited = None):
    if visited is None:
        visited = set()

    if board.is_solved():
        return path
    if depth == max_depth:
        return None

    current_board = board.getBoard()
    visited.add(tuple(map(tuple, current_board)))

    possible_moves = board.get_possible_moves()

    for direction in permutation:
        new_board = copy.deepcopy(board)
        new_board.move(direction)
        if direction in possible_moves and tuple(map(tuple, new_board.getBoard())) not in visited:
            result = dfs(new_board,path + direction,max_depth,permutation,depth + 1,visited)
            if result:
                return result
    return None





