from Statistics import Statistics
import heapq
import copy

# f = q + h(board) - f = prioritise q = depth h(board) = odległość
"""
    Algorytm przeszukiwania 'najpeirw najlepszy' względem priorytetu.
    Uzupełnia path, visited_states, max_depth_reached,processed_states,time,found 
    w obiekcie statystyk

        Zwracany jest obiekt statistics przy powodzeniu i niepowodzeniu.
        
    Priorytet(koszt) liczony jest na podstawie sumy głębokości i wartości heuryskyki. 
        f = q + h(board)  
            f = priorytet, q = głębokość, h(board) = wartość heurystyki
        heurystyka hamminga - ilość elemntów, które nie są na swoim miejscu
        heurystyka manhattan - suma ilości ruchów dla każdej liczby, które są potrzebe 
            aby liczba była na swoim miejscu, przy pominięciu ruchów pustego miejsca
"""


def aStar(board, heuristic, max_level=20):
    statistics = Statistics()
    statistics.path = ""

    """
    heapq - jest to kolejka priorytetowa, struktura danych, która pozwala na szybkie dodawanie
          i usuwanie elementów z najmniejszym priorytetem (w tym przypadku koszt f)
          moduł, który implementuje min-heap, 
          czyli strukturę danych umożliwiającą szybkie wyciąganie najmniejszego elementu.
          Wyższy priorytet do wyciągnięcia jako pierwsze bedą miały stany, których koszt jest mniejszy  
    """

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
            statistics.found = True
            return statistics

        if depth > statistics.max_depth_reached:
            statistics.max_depth_reached = depth

        if max_level == depth:
            break

        possible_moves = current_board.get_possible_moves()

        for direction in possible_moves:
            new_board = current_board.clone()
            new_board.move(direction)

            if str(new_board.getBoard()) not in visited:
                visited.add(str(new_board.getBoard()))
                statistics.visited_states += 1

                if heuristic == "hamm":
                    h = heuristic_hamming(new_board)
                elif heuristic == "manh":
                    h = heuristic_manhattan(new_board)
                else:
                    print("zła heurystyka")
                    return None
                depth += 1
                f = depth + h
                new_board.setPriority(f)

                heapq.heappush(queue, (f, depth, new_board, statistics.path + direction))

    statistics.stop_timer()
    return statistics


def heuristic_manhattan(board):
    h = 0
    # solution jest lista od 1 do rozmiaru planszy
    solution = list(range(1, board.rows * board.cols)) + [0]

    # znajdowanie docelowych pozycji kazdego z pol
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
    _, wrong = board.check_positions()
    return wrong
