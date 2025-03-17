import copy
from traceback import print_tb
from Board import Board

def dfs(board, path, max_depth, permutation, depth = 0, visited = None):
    if visited is None:
        visited = set()

    if board.is_solved():
        return path         #sprawdzamy, czy jest rozwiązane
    if depth == max_depth:
        return None         # osiągniecie maksymalnej głębokości

    current_board = board.getBoard()
    visited.add(tuple(map(tuple, current_board))) # można stworzyć nowy obiekt, który będzie przechowywał

    possible_moves = board.get_possible_moves()

    for direction in permutation:
        new_board = copy.deepcopy(board)
        new_board.move(direction)
        if direction in possible_moves and tuple(map(tuple, new_board.getBoard())) not in visited:
            result = dfs(new_board,path + direction,max_depth,permutation,depth + 1)
            if result:
                return result
    return None





