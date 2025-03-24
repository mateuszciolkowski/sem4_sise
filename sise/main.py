# Przykład użycia
from numpy.random import permutation
import sys
from Board import Board
from Dfs import dfs
from Bfs import bfs
from ProgramOptions import ProgramOptions

#ODCZYT ARGUMENTOW FUNKCJI I WYPISANIE JAKIE ZOSTALY PODANEs
# program_options = ProgramOptions.options()
# program_options.print_options()

#DO TESTOW
# program bfs RDUL 4x4_01_0001.txt 4x4_01_0001_bfs_rdul_sol.txt 4x4_01_0001_bfs_rdul_stats.txt
# program dfs LUDR 4x4_01_0001.txt 4x4_01_0001_dfs_ludr_sol.txt 4x4_01_0001_dfs_ludr_stats.txt
# program astr manh 4x4_01_0001.txt 4x4_01_0001_astr_manh_sol.txt 4x4_01_0001_astr_manh_stats.txt

board = Board('resources/initBoard.txt')
board.print_board()
print("")

permutation = ['R','D','U','L']

bfs(board,20,permutation).to_string()
print("")
dfs(board,"",30,permutation).to_string()

# RULDRUDRUDR
# RULDRURDLULURDRDLULURDLURDRDR