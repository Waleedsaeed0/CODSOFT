import sys
import random
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from enum import Enum

# Constants for the players
HUMAN = 'X'
AI = 'O'
EMPTY = ' '

class AIDifficulty(Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2

class TicTacToeGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Tic-Tac-Toe - AI vs Human")
        self.setMinimumSize(300, 350)  # Set the minimum size

        self.board_size = 3
        self.ai_difficulty = AIDifficulty.EASY
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)  # Set the spacing between items
        self.central_widget.setLayout(self.layout)

        self.init_game()

        self.restart_button = QPushButton("Restart", self)
        self.restart_button.setStyleSheet(
            "QPushButton {"
            "background-color: #C3B1E1;"
            "border: 1px solid black;"
            "border-radius: 5px;"
            "padding: 1px;"
            "font-size: 15px;"
            "}"
            "QPushButton:pressed {"
            "background-color: #DCC6F2;"
            "}"
        )
        self.restart_button.clicked.connect(self.new_game)
        self.layout.addWidget(self.restart_button)
        self.difficulty_selector.setStyleSheet(
            "background-color: #C3B1E1;"
            "border: 2px solid black;"
            "border-radius: 5px;"
            "padding: 5px;"
            "font-size: 14px;"
        )
        self.setStyleSheet(
            "QPushButton {"
            "background-color: #C3B1E1;"
            "border: 2px solid black;"
            "border-radius: 5px;"
            "font-size: 58px;"
            "}"
            "QPushButton:pressed {"
            "background-color: #DCC6F2;"
            "}"
        )

    def init_game(self):
        self.board = [[EMPTY] * self.board_size for _ in range(self.board_size)]
        self.buttons = []

        for i in range(self.board_size):
            row = []
            for j in range(self.board_size):
                button = QPushButton('', self)
                button.setFont(QFont('Arial', 58 ))
                size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                button.setSizePolicy(size_policy)  # Set size policy
                button.clicked.connect(lambda _, i=i, j=j: self.make_move(i, j))
                row.append(button)
            self.buttons.append(row)

        self.layout.addWidget(self.create_difficulty_selector())
        for row in self.buttons:
            row_layout = QHBoxLayout()
            row_layout.setSpacing(10)  # Set the spacing between items
            for button in row:
                row_layout.addWidget(button)
            self.layout.addLayout(row_layout)

    def create_difficulty_selector(self):
        self.difficulty_selector = QComboBox(self)
        self.difficulty_selector.addItem("Easy")
        self.difficulty_selector.addItem("Medium")
        self.difficulty_selector.addItem("Hard")
        size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.difficulty_selector.setSizePolicy(size_policy)  # Set size policy
        self.difficulty_selector.currentIndexChanged.connect(self.set_ai_difficulty)
        return self.difficulty_selector

    def set_ai_difficulty(self):
        selected_difficulty = self.difficulty_selector.currentIndex()
        self.ai_difficulty = AIDifficulty(selected_difficulty)
        self.new_game()

    def new_game(self):
        self.clear_board()
        self.enable_buttons()

    def clear_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.buttons[i][j].setText("")
                self.board[i][j] = EMPTY

    def enable_buttons(self):
        for row in self.buttons:
            for button in row:
                button.setEnabled(True)

    def make_move(self, i, j):
        if self.board[i][j] == EMPTY:
            self.board[i][j] = HUMAN
            self.buttons[i][j].setText(HUMAN)
            self.buttons[i][j].setEnabled(False)
            self.check_game_status()
            self.ai_move()

    def ai_move(self):
        if not self.is_full() and not self.is_winner(HUMAN) and not self.is_winner(AI):
            i, j = self.get_best_move()
            self.board[i][j] = AI
            self.buttons[i][j].setText(AI)
            self.buttons[i][j].setEnabled(False)
            self.check_game_status()

    def is_full(self):
        return all(self.board[i][j] != EMPTY for i in range(self.board_size) for j in range(self.board_size))

    def get_best_move(self):
        if self.ai_difficulty == AIDifficulty.EASY:
            return random.choice(self.get_empty_cells())
        elif self.ai_difficulty == AIDifficulty.MEDIUM:
            return self.minimax(self.board, AI, 2)[1]
        elif self.ai_difficulty == AIDifficulty.HARD:
            return self.minimax_alpha_beta(self.board, AI, float('-inf'), float('inf'))[1]

    def evaluate(self, board):
        if self.is_winner(AI):
            return 10
        elif self.is_winner(HUMAN):
            return -10
        else:
            return 0

    def minimax(self, board, player, depth):
        if player == AI:
            best_score = float('-inf')
            best_move = None
        else:
            best_score = float('inf')
            best_move = None

        if depth == 0 or self.is_full():
            return self.evaluate(board), best_move

        for move in self.get_empty_cells():
            i, j = move
            board[i][j] = player
            if player == AI:
                score = self.minimax(board, HUMAN, depth - 1)[0]
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                score = self.minimax(board, AI, depth - 1)[0]
                if score < best_score:
                    best_score = score
                    best_move = move
            board[i][j] = EMPTY

        return best_score, best_move

    def minimax_alpha_beta(self, board, player, alpha, beta):
        if player == AI:
            best_score = float('-inf')
            best_move = None
        else:
            best_score = float('inf')
            best_move = None

        if self.is_winner(AI):
            return 10, None
        elif self.is_winner(HUMAN):
            return -10, None
        elif self.is_full():
            return 0, None

        for move in self.get_empty_cells():
            i, j = move
            board[i][j] = player
            if player == AI:
                score, _ = self.minimax_alpha_beta(board, HUMAN, alpha, beta)
                if score > best_score:
                    best_score = score
                    best_move = move
                alpha = max(alpha, best_score)
            else:
                score, _ = self.minimax_alpha_beta(board, AI, alpha, beta)
                if score < best_score:
                    best_score = score
                    best_move = move
                beta = min(beta, best_score)
            board[i][j] = EMPTY
            if alpha >= beta:
                break

        return best_score, best_move

    def get_empty_cells(self):
        return [(i, j) for i in range(self.board_size) for j in range(self.board_size) if self.board[i][j] == EMPTY]
    
    def is_winner(self, player):
        for i in range(self.board_size):
            if all(self.board[i][j] == player for j in range(self.board_size)) or \
            all(self.board[j][i] == player for j in range(self.board_size)):
                return True
        if all(self.board[i][i] == player for i in range(self.board_size)) or \
        all(self.board[i][self.board_size - 1 - i] == player for i in range(self.board_size)):
            return True
        return False

    def check_game_status(self):
        if self.is_winner(HUMAN):
            self.show_message("You win!")
            self.disable_buttons()
        elif self.is_winner(AI):
            self.show_message("AI wins!")
            self.disable_buttons()
        elif self.is_full():
            self.show_message("It's a draw!")
            self.disable_buttons()

    def show_message(self, message):
        msg_box = QMessageBox()
        msg_box.setWindowTitle("Game Over")
        msg_box.setText(message)
        msg_box.exec()

    def disable_buttons(self):
        for row in self.buttons:
            for button in row:
                button.setEnabled(False)

def main():
    app = QApplication(sys.argv)
    game_window = TicTacToeGUI()
    game_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
