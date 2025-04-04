import itertools
import os
import glob


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
        statistics = bfs(board, 20, program_options.order)
    elif program_options.strategy == "dfs":
        statistics = dfs(board, 20, program_options.order)
    elif program_options.strategy == "astr":
        statistics = aStar(board, 30, program_options.order)
    else:
        return None

    solved_statistics(statistics, program_options.solution_file)
    solved_solutions(statistics, program_options.stats_file)


def solved_statistics(statistics, output_statistics, automatic=0):
    try:
        if automatic == 0:
            os.makedirs("resources/output_statistics", exist_ok=True)
            filepath = os.path.join("resources/output_statistics", output_statistics)
        else:
            os.makedirs("resources/output_statistics_boards", exist_ok=True)
            filepath = os.path.join("resources/output_statistics_boards", output_statistics)

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


def solved_solutions(statistics, output_solutions, automatic=0):
    try:
        if automatic == 0:
            os.makedirs("resources/output_solutions", exist_ok=True)
            filepath = os.path.join("resources/output_solutions", output_solutions)
        else:
            os.makedirs("resources/output_solutions_boards", exist_ok=True)
            filepath = os.path.join("resources/output_solutions_boards", output_solutions)

        with open(filepath, "w") as file:
            if statistics.path is None:
                file.write("Length of finded solution: -1\n")
            else:
                file.write("Length of finded solution: " + str(len(statistics.path)) + "\n")
            file.write(statistics.path)
    except Exception as e:
        print(e)


def research_part():
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

            # if "4x4_01" in filename:
            #     move_categories["one_move"].append(filename)
            # elif "4x4_02" in filename:
            #     move_categories["two_move"].append(filename)
            # elif "4x4_03" in filename:
            #     move_categories["three_move"].append(filename)
            # elif "4x4_04" in filename:
            #     move_categories["four_move"].append(filename)
            # elif "4x4_05" in filename:
            #     move_categories["five_move"].append(filename)
            if "4x4_06" in filename:
                move_categories["six_move"].append(filename)
            else:
                move_categories["seven_move"].append(filename)

    order_list = ['RDUL','RDLU','DRUL', 'DRLU','LUDR','LURD','ULDR','ULRD']
    # order_list = ['DRUL']
    for category in move_categories:
        print(category)
        for filename in move_categories[category]:
            print(filename)
            base_name = os.path.splitext(filename)[0]
            board = Board(f"resources/boards/{filename}")
            for order in order_list:
                statistics = bfs(board,order)
                nazwa = f"{base_name}_bfs_{order}_stats.txt"
                solved_statistics(statistics, nazwa, automatic=True)
                nazwa = f"{base_name}_bfs_{order}_sol.txt"
                solved_solutions(statistics, nazwa, automatic=True)

                statistics = dfs(board, 20, order)
                nazwa = f"{base_name}_dfs_{order}_stats.txt"
                solved_statistics(statistics, nazwa, automatic=True)
                nazwa = f"{base_name}_dfs_{order}_sol.txt"
                solved_solutions(statistics, nazwa, automatic=True)


                statistics = aStar(board,"manh")
                nazwa = f"{base_name}_astr_manh_stats.txt"
                solved_statistics(statistics, nazwa, automatic=True)
                nazwa = f"{base_name}_astr_manh_sol.txt"
                solved_solutions(statistics, nazwa, automatic=True)


                statistics = aStar(board, "hamm")
                nazwa = f"{base_name}_astr_hamm_stats.txt"
                solved_statistics(statistics, nazwa, automatic=True)
                nazwa = f"{base_name}_astr_hamm_sol.txt"
                solved_solutions(statistics, nazwa, automatic=True)


def file_reader(phrase_a,phrase_b,phrase_c):
    folder_path = "resources/output_statistics_boards"

    pattern = os.path.join(folder_path, f"*{phrase_a}*{phrase_b}*{phrase_c}*")
    files = glob.glob(pattern)

    table = []


    for filepath in files:
        values = []
        with open(filepath, "r") as file:
            for line in file:
                word = line.strip().split()
                values.append(word[-1])
            table.append(values)

    # 0 --> length of path
    # 1 --> visited_states
    # 2 --> processed_states
    # 3 --> max_depth
    # 4 --> time
    average_table = []
    for i in range(len(values)):
       average_table.append(get_average(table,i))
    print(table)
    return average_table


def get_average(table_with_data,index):
    column_sum = sum(float(row[index]) for row in table_with_data)
    return column_sum / len(table_with_data)