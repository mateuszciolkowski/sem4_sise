from collections import deque
from Statistics import Statistics

"""
    Algorytm przeszukiwania wszerz z podaną permutacją.
    Uzupełnia path, visited_states, max_depth_reached,processed_states,time,found
    w obiekcie statystyk
    
        Zwracany jest obiekt statistics przy powodzeniu i niepowodzeniu.
    
"""

def bfs(board, permutation, max_level = 20):
    statistics = Statistics()
    statistics.path = ""

    """
          deque() 
              pusta kolejna dwukierunkowa - funkcja popleft() 
    """

    que = deque()
    que.append((board,statistics.path,0))

    """
         set() 
             przechowuje unikalne elementy zbioru danych 
             szybkie sprawdzanie, czy coś już istnieje w zbiorze (O(1) średnio)
    """
    visited = set()
    visited.add(str(board.getBoard()))

    while que:
        current_board, statistics.path, depth = que.popleft()
        statistics.processed_states += 1

        if depth > statistics.max_depth_reached:
            statistics.max_depth_reached = depth

        if current_board.is_solved():
            statistics.stop_timer()
            statistics.found = True
            return statistics

        if max_level == statistics.max_depth_reached:
            break

        possible_moves = current_board.get_possible_moves()

        for direction in permutation:
            new_board = current_board.clone()
            new_board.move(direction)
            if direction in possible_moves and str(new_board.getBoard()) not in visited:
                visited.add(str(new_board.getBoard()))
                statistics.visited_states += 1

                que.append((new_board, statistics.path + direction, depth + 1))

    statistics.stop_timer()
    return statistics



