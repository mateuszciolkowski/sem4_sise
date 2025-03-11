class Board:
    def __init__(self, filename):
        self.board = []
        self.load_from_file(filename)

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            # Wczytanie rozmiaru planszy (wielkość wierszy i kolumn)
            self.rows, self.cols = map(int, file.readline().split())
            self.board = []

            # Wczytanie elementów układanki
            for y in range(self.rows):
                row = list(map(int, file.readline().split()))
                self.board.append(row)

    def print_board(self):
        for row in self.board:
            print(' '.join(map(str, row)))

    def move(self, direction):
        y, x = self.find_zero()
        if direction == 'U' and y > 0:
            self.board[y][x], self.board[y - 1][x] = self.board[y - 1][x], self.board[y][x]
        elif direction == 'D' and y < self.rows - 1:
            self.board[y][x], self.board[y + 1][x] = self.board[y + 1][x], self.board[y][x]
        elif direction == 'L' and x > 0:
            self.board[y][x], self.board[y][x - 1] = self.board[y][x - 1], self.board[y][x]
        elif direction == 'R' and x < self.cols - 1:
            self.board[y][x], self.board[y][x + 1] = self.board[y][x + 1], self.board[y][x]

    def find_zero(self):
        for y in range(self.rows):
            for x in range(self.cols):
                if self.board[y][x] == 0:
                    return (y, x)
        return None

    def get_possible_moves(self):
        # Znajdź pozycję wolnego pola (0)
        y, x = self.find_zero()

        # Lista dostępnych ruchów
        possible_moves = []

        # Sprawdzamy, które ruchy są możliwe
        if y > 0:  # Ruch w górę jest możliwy, jeśli nie jesteśmy w pierwszym wierszu
            possible_moves.append('U')
        if y < self.rows - 1:  # Ruch w dół jest możliwy, jeśli nie jesteśmy w ostatnim wierszu
            possible_moves.append('D')
        if x > 0:  # Ruch w lewo jest możliwy, jeśli nie jesteśmy w pierwszej kolumnie
            possible_moves.append('L')
        if x < self.cols - 1:  # Ruch w prawo jest możliwy, jeśli nie jesteśmy w ostatniej kolumnie
            possible_moves.append('R')

        return possible_moves

    def is_solved(self):
        # Tworzymy rozwiązanie w oparciu o rozmiar planszy
        solution = list(range(1, self.rows * self.cols)) + [0]
        correct_solution = [solution[i:i + self.cols] for i in range(0, len(solution), self.cols)]
        return self.board == correct_solution

    def check_positions(self):
        # Tworzymy rozwiązanie w oparciu o rozmiar planszy
        solution = list(range(1, self.rows * self.cols)) + [0]
        correct_solution = [solution[i:i + self.cols] for i in range(0, len(solution), self.cols)]

        correct_positions = 0
        wrong_positions = 0

        # Porównaj aktualną planszę ze stanem rozwiązania
        for y in range(self.rows):
            for x in range(self.cols):
                if self.board[y][x] == correct_solution[y][x]:
                    correct_positions += 1
                else:
                    wrong_positions += 1

        return correct_positions, wrong_positions


