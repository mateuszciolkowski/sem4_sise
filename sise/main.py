from ProgramOptions import ProgramOptions
from Statistics import Statistics
from Solutions import *

#ODCZYT ARGUMENTOW FUNKCJI I WYPISANIE JAKIE ZOSTALY PODANEs

# program_options = ProgramOptions.options()
# if program_options is not None:
#     solve_board(program_options)


# bfs_files = get_files_by_type("bfs")
# sorted_files = sort_files_permutations(bfs_files)

# for key, files in sorted_files.items():
#     print(f"{key}: {files}")


#DO TESTOW
# program bfs RDUL 4x4_01_0001.txt 4x4_01_0001_bfs_rdul_sol.txt 4x4_01_0001_bfs_rdul_stats.txt
# program dfs LUDR 4x4_01_0001.txt 4x4_01_0001_dfs_ludr_sol.txt 4x4_01_0001_dfs_ludr_stats.txt
# program astr manh 4x4_01_0001.txt 4x4_01_0001_astr_manh_sol.txt 4x4_01_0001_astr_manh_stats.txt
# python main.py astr hamm 4x4_01_0001.txt 4x4_01_0001_bfs_rdul_sol.txt 4x4_01_0001_bfs_rdul_stats.txt

# board = Board('resources/input_board/4x4_01_0001.txt')
# board.print_board()
# permutation =['U','D','R','L']
# print("")
# bfs(board,permutation).to_string()
# print("")
# dfs(board,"",20,permutation).to_string()
# print("")
# statistics = Statistics()int(
# aStar(board,30,permutation,"manh").to_string()
# print("\n")
# aStar(board,30,permutation,"hamm").to_string()

# print(file_reader("4x4_07","bfs","*"))
# print(results_bfs_by_permutations())
# print(results_manh())
print(plot_all_criteria())
