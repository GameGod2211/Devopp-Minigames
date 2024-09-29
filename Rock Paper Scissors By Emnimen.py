import sys
import random
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QRadioButton, # type: ignore
                             QLineEdit, QMessageBox, QTextEdit)
from PyQt5.QtGui import QFont # type: ignore
from PyQt5.QtCore import Qt # type: ignore
import tkinter as tk
from tkinter import font

class RockPaperScissorsGame(QWidget):
    def __init__(self):
        super().__init__()
        self.user_score = 0
        self.comp_score = 0
        self.current_game_mode = 'rps'
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Devopps Minigames')
        font = QFont("Times New Roman", 12)  
        self.setFont(font)
        self.setGeometry(1000, 700,700, 1000)

        self.mode_label = QLabel('Select Game Mode:', self)
        self.mode_label.setFont(QFont('Arial', 20, QFont.Bold))
        self.mode_label.setStyleSheet("color: #2c3e50;")

        self.single_player_radio = QRadioButton('Single Player', self)
        self.single_player_radio.setChecked(True)
        self.single_player_radio.setStyleSheet("font-size: 18px; color: #2c3e50;")

        self.multiplayer_radio = QRadioButton('Multiplayer', self)
        self.multiplayer_radio.setStyleSheet("font-size: 18px; color: #2c3e50;")

        self.rps_radio = QRadioButton('Rock-Paper-Scissors', self)
        self.rps_radio.setChecked(True)
        self.rps_radio.setStyleSheet("font-size: 18px; color: #2c3e50;")

        self.odd_even_radio = QRadioButton('Odd-Even', self)
        self.odd_even_radio.setStyleSheet("font-size: 18px; color: #2c3e50;")

        self.guess_number_radio = QRadioButton('Guess the Number', self)
        self.guess_number_radio.setStyleSheet("font-size: 18px; color: #2c3e50;")
        
        self.higher_lower_radio = QRadioButton('Higher or Lower', self)
        self.higher_lower_radio.setStyleSheet("font-size: 18px; color: #2c3e50;")
        
        self.sudoku_radio = QRadioButton('Sudoku Solver', self)
        self.sudoku_radio.setStyleSheet("font-size: 18px; color: #2c3e50;")

        self.cricket_radio = QRadioButton('Cricket', self)
        self.cricket_radio.setStyleSheet("font-size: 18px; color: #2c3e50;")

        self.start_button = QPushButton('Start Game', self)
        self.start_button.setStyleSheet(self.get_button_style())
        self.start_button.clicked.connect(self.start_game)

        self.quit_button = QPushButton('Quit', self)
        self.quit_button.setStyleSheet(self.get_button_style())
        self.quit_button.clicked.connect(self.quit_game)

        self.result_label = QLabel('', self)
        self.result_label.setFont(QFont('Arial', 22, QFont.Bold))
        self.result_label.setStyleSheet("color: #e74c3c;")

        self.score_label = QLabel('User: 0 | Computer: 0', self)
        self.score_label.setFont(QFont('Arial', 20, QFont.Bold))
        self.score_label.setStyleSheet("color: #34495e;")

        self.number_input = QLineEdit(self)
        self.number_input.setPlaceholderText("Enter your guess (1-100)")
        self.number_input.setVisible(False)

        self.guess_input = QLineEdit(self)
        self.guess_input.setPlaceholderText("Enter your guess (higher/lower)")
        self.guess_input.setVisible(False)

        self.sudoku_input = QTextEdit(self)
        self.sudoku_input.setPlaceholderText("Enter Sudoku puzzle (9x9 grid with 0 for empty cells)")
        self.sudoku_input.setVisible(False)

        self.cricket_input = QLineEdit(self)
        self.cricket_input.setPlaceholderText("Enter your number (1-6)")
        self.cricket_input.setVisible(False)

        self.solve_sudoku_button = QPushButton('Solve Sudoku', self)
        self.solve_sudoku_button.setStyleSheet(self.get_button_style())
        self.solve_sudoku_button.setVisible(False)
        self.solve_sudoku_button.clicked.connect(self.solve_sudoku)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.quit_button)

        mode_layout = QVBoxLayout()
        mode_layout.addWidget(self.mode_label)
        mode_layout.addWidget(self.single_player_radio)
        mode_layout.addWidget(self.multiplayer_radio)
        mode_layout.addWidget(self.rps_radio)
        mode_layout.addWidget(self.odd_even_radio)
        mode_layout.addWidget(self.guess_number_radio)
        mode_layout.addWidget(self.higher_lower_radio)
        mode_layout.addWidget(self.sudoku_radio)
        mode_layout.addWidget(self.cricket_radio)

        main_layout = QVBoxLayout()
        main_layout.addLayout(mode_layout)
        main_layout.addWidget(self.result_label)
        main_layout.addWidget(self.score_label)
        main_layout.addWidget(self.number_input)
        main_layout.addWidget(self.guess_input)
        main_layout.addWidget(self.sudoku_input)
        main_layout.addWidget(self.solve_sudoku_button)
        main_layout.addWidget(self.cricket_input)
        main_layout.addLayout(button_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)
        self.setStyleSheet("background-color: #f5f6f7;")  # Light background color
        self.show()

    def get_button_style(self):
        return (
            "background-color: #3498db; color: white; font-size: 18px; font-weight: bold;"
            "border-radius: 8px; padding: 12px; min-width: 140px;"
            "border: none; margin: 10px;"
            "transition: background-color 0.3s; "
            "border: 2px solid #2980b9;"
        )

    def start_game(self):
        self.current_game_mode = (
            'rps' if self.rps_radio.isChecked() else
            'odd_even' if self.odd_even_radio.isChecked() else
            'guess_number' if self.guess_number_radio.isChecked() else
            'higher_lower' if self.higher_lower_radio.isChecked() else
            'sudoku' if self.sudoku_radio.isChecked() else
            'cricket'
        )
        self.reset_ui()

    def reset_ui(self):
        self.result_label.setText('')
        self.number_input.setVisible(self.current_game_mode == 'guess_number')
        self.guess_input.setVisible(self.current_game_mode == 'higher_lower')
        self.sudoku_input.setVisible(self.current_game_mode == 'sudoku')
        self.solve_sudoku_button.setVisible(self.current_game_mode == 'sudoku')
        self.cricket_input.setVisible(self.current_game_mode == 'cricket')

        
        for button in self.findChildren(QPushButton):
            button.deleteLater()

        if self.current_game_mode == 'rps':
            self.setWindowTitle('Rock Paper Scissors')
            self.setup_rps_buttons()
        elif self.current_game_mode == 'odd_even':
            self.setWindowTitle('Odd or Even')
            self.setup_odd_even()
        elif self.current_game_mode == 'guess_number':
            self.setWindowTitle('Guess the Number')
            self.setup_guess_number()
        elif self.current_game_mode == 'higher_lower':
            self.setWindowTitle('Higher or Lower')
            self.setup_higher_lower()
        elif self.current_game_mode == 'sudoku':
            self.setWindowTitle('Sudoku Solver')
            self.setup_sudoku()
        elif self.current_game_mode == 'cricket':
            self.setWindowTitle('Cricket')
            self.setup_cricket()

    def setup_rps_buttons(self):
        self.result_label.setText('Choose Rock, Paper, or Scissors!')
        self.score_label.setText(f'User: {self.user_score} | Computer: {self.comp_score}')

        rock_button = QPushButton('Rock', self)
        rock_button.setStyleSheet(self.get_button_style())
        rock_button.clicked.connect(lambda: self.play_rps('rock'))

        paper_button = QPushButton('Paper', self)
        paper_button.setStyleSheet(self.get_button_style())
        paper_button.clicked.connect(lambda: self.play_rps('paper'))

        scissor_button = QPushButton('Scissors', self)
        scissor_button.setStyleSheet(self.get_button_style())
        scissor_button.clicked.connect(lambda: self.play_rps('scissor'))

        button_layout = QHBoxLayout()
        button_layout.addWidget(rock_button)
        button_layout.addWidget(paper_button)
        button_layout.addWidget(scissor_button)

        self.layout().addLayout(button_layout)

    def setup_odd_even(self):
        self.result_label.setText('Select Odd or Even')
        self.score_label.setText(f'User: {self.user_score} | Computer: {self.comp_score}')

        odd_button = QPushButton('Odd', self)
        odd_button.setStyleSheet(self.get_button_style())
        odd_button.clicked.connect(lambda: self.play_odd_even('odd'))

        even_button = QPushButton('Even', self)
        even_button.setStyleSheet(self.get_button_style())
        even_button.clicked.connect(lambda: self.play_odd_even('even'))

        button_layout = QHBoxLayout()
        button_layout.addWidget(odd_button)
        button_layout.addWidget(even_button)

        self.layout().addLayout(button_layout)

    def setup_guess_number(self):
        self.result_label.setText('Guess the Number between 1 and 100!')
        self.score_label.setText(f'User: {self.user_score} | Computer: {self.comp_score}')

        self.number_input.setVisible(True)
        self.number_input.returnPressed.connect(self.play_guess_number)

    def setup_higher_lower(self):
        self.result_label.setText('Guess if the next number will be Higher or Lower')
        self.score_label.setText(f'User: {self.user_score} | Computer: {self.comp_score}')

        self.guess_input.setVisible(True)
        self.guess_input.returnPressed.connect(self.play_higher_lower)

    def setup_sudoku(self):
        self.result_label.setText('Enter Sudoku puzzle and press "Solve Sudoku" to solve.')
        self.sudoku_input.setVisible(True)
        self.solve_sudoku_button.setVisible(True)

    def setup_cricket(self):
        self.result_label.setText('Enter a number between 1 and 6.')
        self.cricket_input.setVisible(True)
        self.cricket_input.returnPressed.connect(self.play_cricket)

    def play_rps(self, user_choice):
        choices = ["rock", "paper", "scissor"]
        computer_choice = random.choice(choices)

        result = self.play_single_player(user_choice, computer_choice)
        self.update_labels(result, computer_choice)
        for i in range(3):
            if choices[i] == user_choice:
                k = i
        if user_choice == computer_choice:
            self.user_score += 0
            result = f'it is a tie'
        elif computer_choice == choices[k-1]:
            self.user_score += 1
            result = f'You Won!'
        else:
            self.comp_score+=1
            result = f'Computer Won!'
        self.check_scores()
        self.update_labels(result,str(computer_choice))

        sender = self.sender()
        self.highlight_button(sender)

    def play_odd_even(self, user_choice):
        computer_number = random.randint(1, 10)
        user_choice = user_choice == 'odd'
        computer_choice = computer_number % 2 == 1

        if user_choice == computer_choice:
            self.user_score += 1
            result = f'Computer chose {computer_number}. You win!'
        else:
            self.comp_score += 1
            result = f'Computer chose {computer_number}. Computer wins!'

        self.check_scores()
        self.update_labels(result, str(computer_number))

    def play_guess_number(self):
        try:
            user_guess = int(self.number_input.text())
            computer_number = random.randint(1, 100)
            
            if user_guess == computer_number:
                self.user_score += 1
                result = f'Correct! The number was {computer_number}. You win!'
            else:
                self.comp_score += 1
                result = f'Wrong! The number was {computer_number}. Computer wins!'

            self.check_scores()
            self.update_labels(result, str(computer_number))
        except ValueError:
            QMessageBox.warning(self, "Invalid Input", "Please enter a valid number between 1 and 100.")

    def play_higher_lower(self):
        try:
            user_guess = self.guess_input.text().strip().lower()
            if user_guess not in ['higher', 'lower']:
                raise ValueError("Invalid guess. Please enter 'higher' or 'lower'.")

            current_number = random.randint(1, 100)
            next_number = random.randint(1, 100)
            computer_choice = 'higher' if next_number > current_number else 'lower'
            
            if user_guess == computer_choice:
                self.user_score += 1
                result = f'The next number was {next_number}. You win!'
            else:
                self.comp_score += 1
                result = f'The next number was {next_number}. Computer wins!'

            self.check_scores()
            self.update_labels(result, str(next_number))
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", str(e))

    def solve_sudoku(self):
        try:
            puzzle = self.sudoku_input.toPlainText().strip().split()
            grid = [list(map(int, puzzle[i * 9:(i + 1) * 9])) for i in range(9)]
            if self.solve_sudoku_grid(grid):
                self.result_label.setText("Sudoku solved!")
                self.sudoku_input.setPlainText('\n'.join([' '.join(map(str, row)) for row in grid]))
            else:
                self.result_label.setText("No solution exists.")
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    def solve_sudoku_grid(self, grid):
        empty = self.find_empty_location(grid)
        if not empty:
            return True
        row, col = empty
        for num in range(1, 10):
            if self.is_safe(grid, row, col, num):
                grid[row][col] = num
                if self.solve_sudoku_grid(grid):
                    return True
                grid[row][col] = 0
        return False

    def find_empty_location(self, grid):
        for row in range(9):
            for col in range(9):
                if grid[row][col] == 0:
                    return (row, col)
        return None

    def is_safe(self, grid, row, col, num):
        for x in range(9):
            if grid[row][x] == num or grid[x][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for r in range(start_row, start_row + 3):
            for c in range(start_col, start_col + 3):
                if grid[r][c] == num:
                    return False
        return True

    def play_cricket(self):
        try:
            user_number = int(self.cricket_input.text().strip())
            if user_number < 1 or user_number > 6:
                raise ValueError("Please enter a number between 1 and 6.")

            computer_number = random.randint(1, 6)
            if user_number == computer_number:
                self.result_label.setText(f"You chose {user_number}. Computer chose {computer_number}. You're out!")
                self.user_score = 0
            else:
                self.user_score += user_number
                self.comp_score += computer_number
                self.result_label.setText(f"You chose {user_number}. Computer chose {computer_number}. Score updated!")

            self.score_label.setText(f'User: {self.user_score} | Computer: {self.comp_score}')
            self.cricket_input.clear()
        except ValueError as e:
            QMessageBox.warning(self, "Invalid Input", str(e))

    def play_single_player(self, user_choice, computer_choice):
        if user_choice == computer_choice:
            return "It's a tie!"
        elif (user_choice == "rock" and computer_choice == "scissor") or \
             (user_choice == "paper" and computer_choice == "rock") or \
             (user_choice == "scissor" and computer_choice == "paper"):
            return "You win!"
        else:
            return "Computer wins!"

    def update_labels(self, result, computer_choice):
        self.result_label.setText(f'Computer chose {computer_choice}. {result}')
        self.score_label.setText(f'User: {self.user_score} | Computer: {self.comp_score}')

    def check_scores(self):
        if self.user_score >= 5:
            self.reset_scores()
            self.result_label.setText("You reached 5 wins! You win the game!")
        elif self.comp_score >= 5:
            self.reset_scores()
            self.result_label.setText("Computer reached 5 wins! Computer wins the game!")

    def reset_scores(self):
        self.user_score = 0
        self.comp_score = 0

    def highlight_button(self, button):
        button.setStyleSheet("background-color: #1abc9c; color: white; font-size: 18px; font-weight: bold;"
                             "border-radius: 8px; padding: 12px; min-width: 140px;"
                             "border: none; margin: 10px;")

    def quit_game(self):
        self.reset_ui()
        self.setWindowTitle('Devopps Minigames')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = RockPaperScissorsGame()
    sys.exit(app.exec_())
