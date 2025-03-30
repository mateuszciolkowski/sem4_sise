import sys

class ProgramOptions:
    def __init__(self, strategy, order, initial_file, solution_file, stats_file):
        self.strategy = strategy  # BFS/DFS/A*
        self.order = order  # BFS/DFS lub heurystyka dla A*
        self.initial_file = initial_file  # Plik wejściowy
        self.solution_file = solution_file  # Plik na rozwiązanie
        self.stats_file = stats_file  # Plik ze statystykami

    def print_options(self):
        print("Wybrane opcje programu:")
        print(f"Strategia: {self.strategy}")
        print(f"Porządek przeszukiwania: {self.order}")
        print(f"Plik wejściowy: {self.initial_file}")
        print(f"Plik rozwiązania: {self.solution_file}")
        print(f"Plik statystyk: {self.stats_file}")

    def get_strategy(self):
        return self.strategy

    def get_order(self):
        return self.order

    def get_initial_file(self):
        return self.initial_file

    def get_solution_file(self):
        return self.solution_file

    def get_stats_file(self):
        return self.stats_file


    @staticmethod
    def options():
        if len(sys.argv) != 6:
            print("Nieprawidłowa liczba argumentów!")
            sys.exit(1)

        strategy = sys.argv[1]  # BFS/DFS/A*
        order = sys.argv[2]  # BFS/DFS lub heurystyka dla A*
        initial_file = sys.argv[3]  # Plik wejściowy
        solution_file = sys.argv[4]  # Plik na rozwiązanie
        stats_file = sys.argv[5]  # Plik ze statystykami

        # Walidacja strategii
        valid_strategies = ['bfs', 'dfs', 'astr']
        if strategy not in valid_strategies:
            print(f"Nieprawidłowa strategia! Dozwolone strategie: {', '.join(valid_strategies)}")
            sys.exit(1)

        valid_order_set = {'L', 'R', 'U', 'D'}
        if len(order) == 4 and set(order) == valid_order_set:
            pass
        elif order in ['hamm', 'manh']:
            pass
        else:
            print("Nieprawidłowy parametr przeszukiwania! Parametr 'order' musi zawierać dokładnie 4 litery: L, R, U, D w dowolnej kolejności lub być jednym z parametrów heurystyki: hamm, manh.")
            sys.exit(1)

        return ProgramOptions(strategy, order, initial_file, solution_file, stats_file)

