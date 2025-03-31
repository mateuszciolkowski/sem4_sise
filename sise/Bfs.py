import copy
from traceback import print_tb
import queue
from collections import deque
from Board import *
from Statistics import Statistics

def bfs(board, max_depth, permutation, depth = 1):
    statistics = Statistics()
    statistics.path = ""
    # que = queue.Queue()
    # que.put((board, path , 0))
    que = deque()
    que.append((board,statistics.path,depth))

    visited = set()
    # visited.add(tuple(map(tuple, board.getBoard())))
    visited.add(str(board.getBoard()))

    while que:
        current_board, statistics.path, depth = que.popleft()
        statistics.processed_states += 1

        if current_board.is_solved():
            statistics.stop_timer()
            return statistics

        if depth > statistics.max_depth_reached:
            statistics.max_depth_reached = depth

        if depth == max_depth:
            return None

        possible_moves = current_board.get_possible_moves()

        for direction in permutation:
            new_board = copy.deepcopy(current_board)
            new_board.move(direction)
            if direction in possible_moves and str(new_board.getBoard()) not in visited:
                visited.add(str(new_board.getBoard()))
                statistics.visited_states += 1

                que.append((new_board, statistics.path + direction, depth + 1))

    return None



