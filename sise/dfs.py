import copy
from traceback import print_tb

from Board import Board


visited = set()

def dfs(Board, path, max_depth, permutation, depth = 0):
    print(f"węzeł depth = {depth}")
    if Board.is_solved():
        print("rozwiązane")
        return path         #sprawdzamy, czy jest rozwiązane
    if depth == max_depth:
        return None         # osiągniecie maksymalnej głębokości

    current_board = Board.getBoard()
    visited.add(tuple(map(tuple, current_board))) # można stworzyć nowy obiekt, który będzie przechowywał

    possible_moves = Board.get_possible_moves()

    for direction in permutation:
        new_board = copy.deepcopy(Board)
        new_board.move(direction)
        print(path)
        if direction in possible_moves and tuple(map(tuple, new_board.getBoard())) not in visited:
            result = dfs(new_board,path + direction,max_depth,permutation,depth + 1)
            if result:
                return result
    print(f"nie znaloziono w tym węźle")
    return None





