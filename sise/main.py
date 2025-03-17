# Przykład użycia
from numpy.random import permutation
import sys
from Board import Board
from Dfs import dfs
from Bfs import bfs
from ProgramOptions import ProgramOptions

#ODCZYT ARGUMENTOW FUNKCJI I WYPISANIE JAKIE ZOSTALY PODANE
# program_options = ProgramOptions.options()
# program_options.print_options()

board = Board('resources/initBoard.txt')
board.print_board()

permutation = ['R','D','U','L']
print(dfs(board,"",7,permutation))

print(bfs(board,50,permutation))

