from Solutions import *
from ProgramOptions import *

# python3 main.py dfs LUDR 4x4_tmp.txt 4x4_01_0001_dfs_ludr_sol.txt 4x4_01_0001_dfs_ludr_stats.txt

program_options = ProgramOptions.options()
if program_options is not None:
    solve_board(program_options)


# plot_all_criteria()