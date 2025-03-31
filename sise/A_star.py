from Statistics import Statistics
import heapq
import copy

# f = q + h(board) - f = prioritise q = depth h(board) = odległość


def aStar(board,heuristic):
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

        # if depth == max_depth:
        #     return None


        possible_moves = current_board.get_possible_moves()

        for direction in possible_moves:
            new_board = copy.deepcopy(current_board)
            new_board.move(direction)


            if str(new_board.getBoard()) not in visited:
                visited.add(str(new_board.getBoard()))
                statistics.visited_states += 1

                if heuristic == "hamm":
                    h = heuristic_hamming(new_board)
                elif heuristic == "manh":
                    h = heuristic_manhattan(current_board)
                else:
                    print("zła heurystyka")
                    return None
                new_board.setPriority(h)
                f = depth + 1 + h

                heapq.heappush(queue, (f, depth + 1, new_board, statistics.path + direction))

    return None

def heuristic_manhattan(board):
    #początkowa wartość heurysttki≠+
    h = 0
    #solution jest lista od 1 do rozmiaru planszy
    solution = list(range(1, board.rows * board.cols)) + [0]

    #znajdowanie docelowych pozycji kazdego z pol
    for y in range(board.rows):
        for x in range(board.cols):
            val = board.board[y][x]
            if val != 0:
                goal_position = solution.index(val)
                goal_y = goal_position // board.cols
                goal_x = goal_position % board.cols
                h += abs(y - goal_y) + abs(x - goal_x)
    return h

def heuristic_hamming(board):
    _ , wrong = board.check_positions()
    return wrong