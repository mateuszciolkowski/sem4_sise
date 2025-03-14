# Przykład użycia
from numpy.random import permutation

from Board import Board
from dfs import dfs

board = Board('resources/initBoard.txt')  # Wczytanie planszy z pliku
board.print_board()  # Wyświetlanie planszy

# Pokaż początkową planszę
print("Początkowa plansza:")
board.print_board()

# Symulacja ruchów
# while (True):
#     correct, wrong = board.check_positions()
#     print(f"\nPrawidłowe miejsca: {correct}, Nieprawidłowe miejsca: {wrong}")
#     move = input("Podaj ruch (up, down, left, right): ").strip()
#     if move in ['U', 'D', 'L', 'R'] and move in board.get_possible_moves():
#         board.move(move)
#         print(f"\nPlansza po ruchu '{move}':")
#         board.print_board()
#     else:
#         print("Nieprawidłowy ruch! Podaj 'up', 'down', 'left' lub 'right'.")
permutation = ['R','D','U','L']
print(dfs(board,"",7,permutation))
