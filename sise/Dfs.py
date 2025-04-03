import copy
from traceback import print_tb
from Statistics import Statistics
from Board import Board
from collections import deque


def dfs(board,max_depth, permutation):
    statistics = Statistics()
    statistics.path = ""
    depth = 0

    stack = deque()
    stack.append((board,statistics.path,depth))

    visited = set()
    # visited.add(str(board.getBoard(),depth))
    visited.add((tuple(map(tuple, board.getBoard())), depth))

    while stack:
        current_board,statistics.path,depth = stack.pop()
        statistics.processed_states += 1

        if depth > statistics.max_depth_reached:
            statistics.max_depth_reached = depth

        if current_board.is_solved():
            statistics.stop_timer()
            return statistics

        if depth == max_depth:
            continue

        for direction in permutation:
            new_board = copy.deepcopy(current_board)
            new_board.move(direction)
            board_state = tuple(map(tuple, new_board.getBoard()))
            if direction in current_board.get_possible_moves() and (board_state,depth) not in visited:
                visited.add((board_state,depth))
                statistics.visited_states += 1

                stack.append((new_board,statistics.path + direction,depth+1))

    return None
