from collections import deque
import copy
from Statistics import Statistics


class State:
    def __init__(self, board, zero_position, parent, move, g, h):
        self.board = board  # Obiekt planszy
        self.zero_position = zero_position  # Pozycja pustego kafelka
        self.parent = parent  # Poprzedni stan
        self.move = move  # Ruch, który doprowadził do tego stanu
        self.g = g  # Koszt (liczba ruchów od stanu początkowego)
        self.h = h  # Heurystyka (odległość Manhattan)
        self.f = g + h  # Całkowity koszt (f = g + h)


def heuristic(board):
    """Oblicza heurystykę (odległość Manhattan) dla obecnego stanu"""
    h = 0
    solution = list(range(1, board.rows * board.cols)) + [0]

    for y in range(board.rows):
        for x in range(board.cols):
            val = board.board[y][x]
            if val != 0:
                goal_pos = solution.index(val)
                goal_y, goal_x = goal_pos // board.cols, goal_pos % board.cols
                h += abs(y - goal_y) + abs(x - goal_x)
    return h


def a_star(board, statistics):
    open_list = deque()
    closed_list = set()

    start_h = heuristic(board)
    start_state = State(board, (board.x_0, board.y_0), None, None, 0, start_h)
    open_list.append(start_state)

    while open_list:
        # Sortujemy kolejkę przed wyjęciem elementu o najniższym koszcie
        open_list = deque(sorted(open_list, key=lambda x: x.f))

        # Pobieramy stan z otwartej listy
        current_state = open_list.popleft()

        # Sprawdzamy, czy znaleźliśmy rozwiązanie
        if current_state.h == 0:
            path = []
            while current_state.parent:
                path.append(current_state.move)
                current_state = current_state.parent
            statistics.stop_timer()
            statistics.path = ''.join(path[::-1])
            return statistics

        # Oznaczamy stan jako odwiedzony
        closed_list.add(tuple(map(tuple, current_state.board.board)))
        statistics.processed_states += 1

        # Generujemy nowe stany na podstawie możliwych ruchów
        possible_moves = current_state.board.get_possible_moves()
        for direction in possible_moves:
            new_board = copy.deepcopy(current_state.board)
            new_board.move(direction)
            new_h = heuristic(new_board)
            new_g = current_state.g + 1
            new_state = State(new_board, (new_board.x_0, new_board.y_0), current_state, direction, new_g, new_h)

            if tuple(map(tuple, new_board.board)) not in closed_list:
                open_list.append(new_state)
                closed_list.add(tuple(map(tuple, new_board.board)))
                statistics.visited_states += 1

    return None
