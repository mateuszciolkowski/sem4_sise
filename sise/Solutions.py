import itertools
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

    solved_statistics(statistics,program_options.solution_file)
    solved_solutions(statistics,program_options.stats_file)


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

def research_part():
    # dzielenie plansz ze wzgledu na ilosc ruchów wykonanych do tworzenia wykresów
    move_categories = {
        "one_move": [],
        "two_move": [],
        "three_move": [],
        "four_move": [],
        "five_move": [],
        "six_move": [],
        "seven_move": []
    }

    for entry in os.scandir("resources/boards"):
        if entry.is_file():
            filename = entry.name

            if "4x4_01" in filename:
                move_categories["one_move"].append(filename)
            elif "4x4_02" in filename:
                move_categories["two_move"].append(filename)
            elif "4x4_03" in filename:
                move_categories["three_move"].append(filename)
            elif "4x4_04" in filename:
                move_categories["four_move"].append(filename)
            elif "4x4_05" in filename:
                move_categories["five_move"].append(filename)
            elif "4x4_06" in filename:
                move_categories["six_move"].append(filename)
            else:
                move_categories["seven_move"].append(filename)

    order_list = ['RDUL','RDLU','DRUL', 'DRLU','LUDR','LURD','ULDR','ULRD']

    arithmetical_depth = []
    for category in move_categories:
        print(category)
        depth = 0
        for filename in move_categories[category]:
            print(filename)
            board = Board(f"resources/boards/{filename}")
            for order in order_list:
                statistics = dfs(board,"",8,order)
                if statistics.path is not None:
                    depth += statistics.max_depth_reached
        arithmetical_depth.append(depth/len(move_categories[category]))
    print(arithmetical_depth)

