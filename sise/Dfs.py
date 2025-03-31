from Statistics import Statistics


def dfs(board, path, max_depth, permutation, depth=0, visited=None, statistics=None):
    if visited is None:
        visited = set()
        statistics = Statistics()
        path = ""

    # Sprawdzenie czy plansza jest już rozwiązana (czy to jedno-ruchowe rozwiązanie)
    if board.is_solved():
        statistics.stop_timer()
        statistics.path = path
        return statistics

    # Aktualizacja maksymalnej osiągniętej głębokości
    if depth > statistics.max_depth_reached:
        statistics.max_depth_reached = depth

    if depth == max_depth:
        return None  # Przekroczona maksymalna głębokość

    # Użycie krotek zamiast stringów dla oszczędności pamięci
    board_tuple = tuple(map(tuple, board.getBoard()))

    if board_tuple not in visited:
        visited.add(board_tuple)
        statistics.processed_states += 1

    possible_moves = board.get_possible_moves()

    # Iteracja po permutacjach kierunków
    for direction in permutation:
        if direction in possible_moves:
            board.move(direction)
            new_board_tuple = tuple(map(tuple, board.getBoard()))

            # Sprawdzamy, czy stan nie był jeszcze odwiedzony
            if new_board_tuple not in visited:
                statistics.visited_states += 1
                result = dfs(board, path + direction, max_depth, permutation, depth + 1, visited, statistics)

                # Jeśli znaleziono rozwiązanie, natychmiast zwracamy wynik
                if result:
                    return result

            # Cofnięcie ruchu (eliminacja deepcopy)
            board.undo_move(direction)
            print("undo")

    return None
