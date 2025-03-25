import copy
from traceback import print_tb
from Statistics import Statistics
from Board import Board


def dfs(board,path,max_depth, permutation, depth = 0, visited = None,statistics = None):
    if visited is None:
        visited = set()
        statistics = Statistics()
        path = ""

    if board.is_solved() and statistics is not None:
        statistics.stop_timer()
        statistics.path = path
        return statistics

    if depth > statistics.max_depth_reached:
        statistics.max_depth_reached = depth

    if depth == max_depth:
        return None


    current_board = board.getBoard()
    # visited.add(tuple(map(tuple, current_board)))
    if str(current_board) not in visited:
        visited.add(str(current_board))  # Dodajemy stan do odwiedzonych
        statistics.processed_states += 1

    possible_moves = board.get_possible_moves()

    for direction in permutation:
        if direction is not board.reversed_last_move:
            new_board = copy.deepcopy(board)
            new_board.move(direction)
        if direction in possible_moves and str(new_board.getBoard()) not in visited:
            statistics.visited_states += 1  # Zwiększamy licznik odwiedzonych stanów
            result = dfs(new_board,path + direction,max_depth,permutation,depth + 1,visited,statistics)

            if result:
                return result
    return None





