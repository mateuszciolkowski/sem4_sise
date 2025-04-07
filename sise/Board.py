class Board:
    def __init__(self, filename):
        self.cols = None
        self.rows = None
        self.board = []
        self.x_0 = None
        self.y_0 = None
        self.reversed_last_move = None
        self.priority = 0
        if filename:
            self.load_from_file(filename)

    def __lt__(self, other):
        return self.priority < other.priority

    # def __eq__(self, other):
    #     if not isinstance(other, Board):
    #         return False
    #     return self.board == other.board and self.reversed_last_move == other.reversed_last_move
    #
    # def __hash__(self):
    #     return hash((self.board,self.reversed_last_move))

    def clone(self):
        new_board = Board(None)
        new_board.board = [row[:] for row in self.board]
        new_board.reversed_last_move = self.reversed_last_move
        new_board.x_0 = self.x_0
        new_board.y_0 = self.y_0
        new_board.rows = self.rows
        new_board.cols = self.cols
        return new_board

    def setPriority(self, priority):
        self.priority = priority

    def load_from_file(self, filename):
        with open(filename, 'r') as file:
            self.rows, self.cols = map(int, file.readline().split())
            self.board = []

            for y in range(self.rows):
                row = list(map(int, file.readline().split()))
                self.board.append(row)
        self.find_zero()

    def getBoard(self):
        return self.board

    def print_board(self):
        for row in self.board:
            print(' '.join(map(str, row)))

    def move(self, direction):
        if direction == 'U' and self.y_0 > 0:
            self.board[self.y_0][self.x_0], self.board[self.y_0 - 1][self.x_0] = self.board[self.y_0 - 1][self.x_0], self.board[self.y_0][self.x_0]
            self.y_0 -= 1
            self.reversed_last_move = "D"
        elif direction == 'D' and self.y_0 < self.rows - 1:
            self.board[self.y_0][self.x_0], self.board[self.y_0 + 1][self.x_0] = self.board[self.y_0 + 1][self.x_0], self.board[self.y_0][self.x_0]
            self.y_0 += 1
            self.reversed_last_move = "U"
        elif direction == 'L' and self.x_0 > 0:
            self.board[self.y_0][self.x_0], self.board[self.y_0][self.x_0 - 1] = self.board[self.y_0][self.x_0 - 1], self.board[self.y_0][self.x_0]
            self.x_0 -= 1
            self.reversed_last_move= "R"
        elif direction == 'R' and self.x_0 < self.cols - 1:
            self.board[self.y_0][self.x_0], self.board[self.y_0][self.x_0 + 1] = self.board[self.y_0][self.x_0 + 1], self.board[self.y_0][self.x_0]
            self.x_0 += 1
            self.reversed_last_move = "L"

    def find_zero(self):
        for y in range(self.rows):
            for x in range(self.cols):
                if self.board[y][x] == 0:
                    self.x_0 = x
                    self.y_0 = y
                    return

    def get_possible_moves(self):
        possible_moves = []

        if self.y_0 > 0:
            possible_moves.append('U')
        if self.y_0 < self.rows - 1:
            possible_moves.append('D')
        if self.x_0 > 0:
            possible_moves.append('L')
        if self.x_0 < self.cols - 1:
            possible_moves.append('R')


        if self.reversed_last_move in possible_moves:
            possible_moves.remove(self.reversed_last_move)

        return possible_moves

    def is_solved(self):
        solution = list(range(1, self.rows * self.cols)) + [0]
        correct_solution = [solution[i:i + self.cols] for i in range(0, len(solution), self.cols)]
        return self.board == correct_solution

    def check_positions(self):
        solution = list(range(1, self.rows * self.cols)) + [0]
        correct_solution = [solution[i:i + self.cols] for i in range(0, len(solution), self.cols)]

        correct_positions = 0
        wrong_positions = 0

        for y in range(self.rows):
            for x in range(self.cols):
                if self.board[y][x] == correct_solution[y][x]:
                    correct_positions += 1
                else:
                    wrong_positions += 1

        return correct_positions, wrong_positions
