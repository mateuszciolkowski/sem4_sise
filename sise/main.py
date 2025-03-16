# Przykład użycia
from numpy.random import permutation
import sys
from Board import Board
from dfs import dfs
from ProgramOptions import ProgramOptions

#ODCZYT ARGUMENTOW FUNKCJI I WYPISANIE JAKIE ZOSTALY PODANE
program_options = ProgramOptions.options()
program_options.print_options()

board = Board('resources/initBoard.txt')  # Wczytanie planszy z pliku
board.print_board()  # Wyświetlanie planszy

# Pokaż początkową planszę
print("Początkowa plansza:")
board.print_board()

permutation = ['R','D','U','L']
print(dfs(board,"",7,permutation))
