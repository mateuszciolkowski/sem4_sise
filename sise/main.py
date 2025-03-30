# Przykład użycia
import sys
from Board import Board
from Dfs import dfs
from Bfs import bfs
from ProgramOptions import ProgramOptions
from A_star import aStar
from Statistics import Statistics
from Solutions import solved_statistics, solve_board

#ODCZYT ARGUMENTOW FUNKCJI I WYPISANIE JAKIE ZOSTALY PODANEs
program_options = ProgramOptions.options()
solve_board(program_options)

#DO TESTOW
# program bfs RDUL 4x4_01_0001.txt 4x4_01_0001_bfs_rdul_sol.txt 4x4_01_0001_bfs_rdul_stats.txt
# program dfs LUDR 4x4_01_0001.txt 4x4_01_0001_dfs_ludr_sol.txt 4x4_01_0001_dfs_ludr_stats.txt
# program astr manh 4x4_01_0001.txt 4x4_01_0001_astr_manh_sol.txt 4x4_01_0001_astr_manh_stats.txt
# python main.py astr hamm 4x4_01_0001.txt 4x4_01_0001_bfs_rdul_sol.txt 4x4_01_0001_bfs_rdul_stats.txt

# board = Board('resources/input_board/rafal.txt')
# board.print_board()
# print("")
# bfs(board,20,permutation).to_string()
# print("")
# dfs(board,"",32,permutation).to_string()
# print("")
# statistics = Statistics()
# aStar(board,30,permutation,"manh").to_string()
# print("\n")
# aStar(board,30,permutation,"hamm").to_string()

