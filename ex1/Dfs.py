from Statistics import Statistics
from collections import deque

"""
    Algorytm przeszukiwania w głąb z ograniczeniem głębokości i z podaną permutacją.
    Uzupełnia path, visited_states, max_depth_reached,processed_states,time,found 
    w obiekcie statystyk

        Zwracany jest obiekt statistics przy powodzeniu i niepowodzeniu.

    W zbiorze visited przetrzymywany jest stan planszy i głębokość; jeśli dostaniemy taki sam stan z mniejszą 
    głębokością (niż jest w zbiorze viesited), będzie on przetwarzany
"""


def dfs(board, max_depth, permutation):
    statistics = Statistics()
    statistics.path = ""
    depth = 0

    """
        deque() 
            pusta kolejna dwukierunkowa, wykorzystywana w algorytmie jako stos - funkcja pop()
            LIFO 
    """

    stack = deque()
    stack.append((board, statistics.path, depth))

    """
        set() 
            może przechowywać tylko hashowalne (niemutowalne) elementy
            przechowuje unikalne elementy zbioru danych 
            szybkie sprawdzanie, czy coś już istnieje w zbiorze (O(1) średnio)
                 O(1) — stała złożoność czasowa
                Oznacza, że czas wykonania nie zależy od ilości danych.
                Działa równie szybko dla małych i dużych zbiorów
                
        visited.add((str(board.getBoard()), depth))
            Dodaje aktualny stan planszy (zamieniony na string, ponieważ listy nie są hashowalne)
            wraz z aktualną głębokością do zbioru.
    """
    visited = set()
    visited.add((str(board.getBoard()), depth))

    while stack:
        current_board, statistics.path, depth = stack.pop()
        statistics.processed_states += 1

        if depth > statistics.max_depth_reached:
            statistics.max_depth_reached = depth

        if current_board.is_solved():
            statistics.stop_timer()
            statistics.found = True
            return statistics

        if depth == max_depth:
            continue

        for direction in permutation:
            new_board = current_board.clone()
            new_board.move(direction)
            board_state = str(new_board.getBoard())
            if direction in current_board.get_possible_moves() and (board_state, depth) not in visited:
                visited.add((board_state, depth))
                statistics.visited_states += 1

                stack.append((new_board, statistics.path + direction, depth + 1))

    statistics.stop_timer()
    return statistics
