import copy
from traceback import print_tb
import queue

from Board import *


def bfs(board, max_depth, permutation, depth = 0):
    path = ""
    que = queue.Queue()
    que.put((board, path , 0))

    #zbiór odwiedzonych stanow
    visited = set()
    visited.add(tuple(map(tuple, board.getBoard())))

    while que.qsize() != 0:
        current_board, path, depth = que.get()

        if current_board.is_solved():
            return path
        if depth == max_depth:
            continue

        possible_moves = current_board.get_possible_moves()

        for direction in permutation:
            new_board = copy.deepcopy(current_board)
            new_board.move(direction)
            if direction in possible_moves and tuple(map(tuple, new_board.getBoard())) not in visited:
                visited.add(tuple(map(tuple, new_board.getBoard())))
                que.put((new_board, path + direction, depth + 1))

    return None



