import itertools
import os
import glob
from tkinter.font import names

import numpy as np
from matplotlib import pyplot as plt
from unicodedata import category

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

    order_list = ['RDUL', 'RDLU', 'DRUL', 'DRLU', 'LUDR', 'LURD', 'ULDR', 'ULRD']
    for category in move_categories:
        print(category)
        for filename in move_categories["seven_move"]:
            print(filename)
            base_name = os.path.splitext(filename)[0]
            board = Board(f"resources/boards/{filename}")
            for order in order_list:
                statistics = bfs(board, order)
                nazwa = f"{base_name}_bfs_{order}_stats.txt"
                solved_statistics(statistics, nazwa, automatic=True)
                nazwa = f"{base_name}_bfs_{order}_sol.txt"
                solved_solutions(statistics, nazwa, automatic=True)

                statistics = dfs(board, 20, order)
                nazwa = f"{base_name}_dfs_{order}_stats.txt"
                solved_statistics(statistics, nazwa, automatic=True)
                nazwa = f"{base_name}_dfs_{order}_sol.txt"
                solved_solutions(statistics, nazwa, automatic=True)

                statistics = aStar(board, "manh")
                nazwa = f"{base_name}_astr_manh_stats.txt"
                solved_statistics(statistics, nazwa, automatic=True)
                nazwa = f"{base_name}_astr_manh_sol.txt"
                solved_solutions(statistics, nazwa, automatic=True)

                statistics = aStar(board, "hamm")
                nazwa = f"{base_name}_astr_hamm_stats.txt"
                solved_statistics(statistics, nazwa, automatic=True)
                nazwa = f"{base_name}_astr_hamm_sol.txt"
                solved_solutions(statistics, nazwa, automatic=True)


def file_reader(phrase_a, phrase_b, phrase_c):
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
        average_table.append(get_average(table, i))
    # print(table)
    return average_table


def get_average(table_with_data, index):
    column_sum = sum(float(row[index]) for row in table_with_data)
    return column_sum / len(table_with_data)


def results_bfs():
    names = ["4x4_01", "4x4_02", "4x4_03", "4x4_04", "4x4_05", "4x4_06", "4x4_07"]
    keys = ["one_move", "two_move", "three_move", "four_move", "five_move", "six_move", "seven_move"]

    move_categories = {}

    for key, name in zip(keys, names):
        move_categories[key] = file_reader(name, "bfs", "*")
        # print(f"{key}: {move_categories[key]}")

    return move_categories


def results_dfs():
    names = ["4x4_01", "4x4_02", "4x4_03", "4x4_04", "4x4_05", "4x4_06", "4x4_07"]
    keys = ["one_move", "two_move", "three_move", "four_move", "five_move", "six_move", "seven_move"]

    move_categories = {}

    for key, name in zip(keys, names):
        move_categories[key] = file_reader(name, "dfs", "*")
        # print(f"{key}: {move_categories[key]}")

    return move_categories


def results_bfs_by_permutations():
    names = ["4x4_01", "4x4_02", "4x4_03", "4x4_04", "4x4_05", "4x4_06", "4x4_07"]
    keys = ["one_move", "two_move", "three_move", "four_move", "five_move", "six_move", "seven_move"]
    order_list = ['RDUL', 'RDLU', 'DRUL', 'DRLU', 'LUDR', 'LURD', 'ULDR', 'ULRD']

    move_categories = {}

    for key, name in zip(keys, names):
        move_categories[key] = {}
        for order in order_list:
            result = file_reader(name, "bfs", order)
            move_categories[key][order] = result
            # print(f"{key}, order {order}: {result}")

    return move_categories


def results_dfs_by_permutations():
    names = ["4x4_01", "4x4_02", "4x4_03", "4x4_04", "4x4_05", "4x4_06", "4x4_07"]
    keys = ["one_move", "two_move", "three_move", "four_move", "five_move", "six_move", "seven_move"]
    order_list = ['RDUL', 'RDLU', 'DRUL', 'DRLU', 'LUDR', 'LURD', 'ULDR', 'ULRD']

    move_categories = {}

    for key, name in zip(keys, names):
        move_categories[key] = {}
        for order in order_list:
            result = file_reader(name, "dfs", order)
            move_categories[key][order] = result
            # print(f"{key}, order {order}: {result}")

    return move_categories


def results_hamm():
    names = ["4x4_01", "4x4_02", "4x4_03", "4x4_04", "4x4_05", "4x4_06", "4x4_07"]
    keys = ["one_move", "two_move", "three_move", "four_move", "five_move", "six_move", "seven_move"]

    move_categories = {}

    for key, name in zip(keys, names):
        move_categories[key] = file_reader(name, "hamm", "*")
        # print(f"{key}: {move_categories[key]}")

    return move_categories


def results_manh():
    names = ["4x4_01", "4x4_02", "4x4_03", "4x4_04", "4x4_05", "4x4_06", "4x4_07"]
    keys = ["one_move", "two_move", "three_move", "four_move", "five_move", "six_move", "seven_move"]

    move_categories = {}

    for key, name in zip(keys, names):
        move_categories[key] = file_reader(name, "manh", "*")
        # print(f"{key}: {move_categories[key]}")

    return move_categories


def plot_all_criteria():
    bfs_results = results_bfs()
    dfs_results = results_dfs()
    hamm_results = results_hamm()
    manh_results = results_manh()
    bfs_permutations = results_bfs_by_permutations()
    dfs_permutations = results_dfs_by_permutations()

    keys = list(bfs_results.keys())  # one_move ... seven_move
    depths = list(range(1, 8))  # odpowiadają głębokościom
    num_criteria = 5  # 0: path length, 1: visited, 2: processed, 3: depth, 4: time

    criteria_labels = ["Długość ścieżki", "Odwiedzone stany", "Przetworzone stany", "Maksymalna głębokość", "Czas [ms]"]

    for crit_index in range(num_criteria):
        fig, axs = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle(f'Kryterium: {criteria_labels[crit_index]}', fontsize=16)

        # 1. Ogólne porównanie: BFS vs DFS vs A*
        bfs_vals = [bfs_results[k][crit_index] for k in keys]
        dfs_vals = [dfs_results[k][crit_index] for k in keys]
        astar_vals = [(hamm_results[k][crit_index] + manh_results[k][crit_index]) / 2 for k in keys]

        axs[0, 0].bar(depths, bfs_vals, width=0.25, label='BFS', align='center')
        axs[0, 0].bar([d + 0.25 for d in depths], dfs_vals, width=0.25, label='DFS')
        axs[0, 0].bar([d + 0.5 for d in depths], astar_vals, width=0.25, label='A*')
        axs[0, 0].set_title("Ogółem")
        axs[0, 0].legend()
        axs[0, 0].set_xlabel("Głębokość")
        axs[0, 0].set_ylabel(criteria_labels[crit_index])
        axs[0, 0].set_yscale("log")  # <-- Skala logarytmiczna

        # 2. A*: Hamming vs Manhattan
        hamm_vals = [hamm_results[k][crit_index] for k in keys]
        manh_vals = [manh_results[k][crit_index] for k in keys]

        axs[0, 1].bar(depths, hamm_vals, width=0.35, label='Hamming', align='center')
        axs[0, 1].bar([d + 0.35 for d in depths], manh_vals, width=0.35, label='Manhattan')
        axs[0, 1].set_title("A*")
        axs[0, 1].legend()
        axs[0, 1].set_xlabel("Głębokość")
        # 3. BFS - różne kolejności ruchów (słupki względem permutacji)
        bar_width = 0.1
        x = np.arange(len(depths))
        order_list = ['RDUL', 'RDLU', 'DRUL', 'DRLU', 'LUDR', 'LURD', 'ULDR', 'ULRD']

        for i, order in enumerate(order_list):
            vals = [bfs_permutations[k][order][crit_index] for k in keys]
            axs[1, 0].bar(x + i * bar_width, vals, width=bar_width, label=order)

        axs[1, 0].set_title("BFS (różne permutacje)")
        axs[1, 0].legend(title="Permutacje", fontsize='x-small', ncol=2)
        axs[1, 0].set_xlabel("Głębokość")
        axs[1, 0].set_ylabel(criteria_labels[crit_index])
        axs[1, 0].set_xticks(x + (len(order_list) / 2 - 0.5) * bar_width)
        axs[1, 0].set_xticklabels(depths)

        # 4. DFS - różne kolejności ruchów (słupki względem permutacji)
        for i, order in enumerate(order_list):
            vals = [dfs_permutations[k][order][crit_index] for k in keys]
            axs[1, 1].bar(x + i * bar_width, vals, width=bar_width, label=order)

        axs[1, 1].set_title("DFS (różne permutacje)")
        axs[1, 1].set_xlabel("Głębokość")
        axs[1, 1].set_xticks(x + (len(order_list) / 2 - 0.5) * bar_width)
        axs[1, 1].set_xticklabels(depths)

        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.savefig(f'kryterium_{crit_index + 1}.png')
        plt.close()
