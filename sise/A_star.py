from Statistics import Statistics
import heapq
import copy

# f = q + h(board) - f = prioritise q = depth h(board) = odległość


def aStar(board, max_depth, permutation):
    statistics = Statistics()
    statistics.path = ""

    queue = []
    # Przygotowanie, w której pierwszy element to f (koszt), a reszta to inne dane
    heapq.heappush(queue, (0, 1, board, statistics.path))  # (f, depth, board, path)
    visited = set()

    visited.add(str(board.getBoard()))

    while queue:
        f, depth, current_board, statistics.path = heapq.heappop(queue)
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

            statistics.visited_states += 1

            if direction in possible_moves and str(new_board.getBoard()) not in visited:
                visited.add(str(new_board.getBoard()))
                statistics.visited_states += 1

                h = heuristic(new_board)
                new_board.setPriority(h)
                f = depth + 1 + h

                heapq.heappush(queue, (f, depth + 1, new_board, statistics.path + direction))

    return None

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
