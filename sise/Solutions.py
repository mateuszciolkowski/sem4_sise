import os
from ProgramOptions import *
from Statistics import *
from A_star import aStar
from Board import Board
from Bfs import *
from Dfs import *
from A_star import *

def solve_board(program_options):
    board = Board(f"resources/input_board/{program_options.initial_file}")
    board.print_board()

    if program_options.strategy == "bfs":
        statistics = bfs(board,20,program_options.order)
    elif program_options.strategy == "dfs":
        statistics = dfs(board,"",32,program_options.order)
    elif program_options.strategy == "astr":
        statistics = aStar(board,30,program_options.order)
    else:
        return None

    solved_statistics(statistics,str(program_options.solution_file))
    solved_solutions(statistics,str(program_options.stats_file))


def solved_statistics(statistics, output_statistics):
    try:
        os.makedirs("resources/output_statistics", exist_ok=True)
        filepath = os.path.join("resources/output_statistics", output_statistics)

        with open(filepath, "w") as file:
            if statistics.path is None:
                file.write("Length of finded solution: -1\n")
            else:
                file.write("Length of finded solution: " + str(len(statistics.path)) + "\n")
            file.write("Visited states: " + str(statistics.visited_states) + "\n")
            file.write("Processed states: " + str(statistics.processed_states) + "\n")
            file.write("Max depth: " + str(statistics.max_depth_reached) + "\n")
            file.write("Time to solve: " + str(statistics.time_reached) + "\n")
    except Exception as e:
        print(e)


def solved_solutions(statistics, output_solutions):
    try:
        os.makedirs("resources/output_solutions", exist_ok=True)
        filepath = os.path.join("resources/output_solutions", output_solutions)

        with open(filepath, "w") as file:
            if statistics.path is None:
                file.write("Length of finded solution: -1\n")
            else:
                file.write("Length of finded solution: "+str(len(statistics.path))+"\n")
            file.write(statistics.path)
    except Exception as e:
        print(e)

