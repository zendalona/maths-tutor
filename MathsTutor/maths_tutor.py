import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QSizePolicy, QPushButton
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QMovie

import random

def parse_question_expression(expression):
    operands = expression.split("+")  
    numbers = []
    for operand in operands:
        if ":" in operand:  
            start, end = map(int, operand.split(":"))
            numbers.append(str(random.randint(start, end)))
        elif "," in operand: 
            options = list(map(int, operand.split(",")))
            numbers.append(str(random.choice(options)))
        elif ";" in operand:  
            multiplier, range_expression = operand.split(";")
            start, end = map(int, range_expression.split(":"))
            selected_number = random.randint(start, end)
            result = int(multiplier) * selected_number
            numbers.append(str(result))
        else:  
            numbers.append(operand)
    return "+".join(numbers)

def load_question_file(file_path):
    questions = []
    with open(file_path, "r") as file:
        for line in file:
            question_data = line.strip().split("===")
            question_expression = parse_question_expression(question_data[0].strip())
            time_allotted = int(question_data[1].strip())
            bell_needed = int(question_data[2].strip())
            questions.append((question_expression, time_allotted, bell_needed))
    return questions

class MathsTutorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Maths Tutor")
        self.questions = load_question_file("../lessons/add_easy.txt")  
        self.current_question_index = -1
        self.create_ui()

    def create_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.label = QLabel("Welcome! Press Enter to start.")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter) 
        font = self.label.font()
        font.setPointSize(50)  
        self.label.setFont(font)
        layout.addWidget(self.label)

        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Enter your answer")
        self.entry.setAlignment(Qt.AlignmentFlag.AlignCenter)  
        self.entry.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Minimum)  
        self.entry.setFont(font)
        layout.addWidget(self.entry)

        self.gif_label = QLabel()
        layout.addWidget(self.gif_label, alignment=Qt.AlignmentFlag.AlignCenter)  
        self.quit_button = QPushButton("Quit")
        self.quit_button.clicked.connect(self.close)
        layout.addWidget(self.quit_button)

        self.toggle_button = QPushButton("Toggle Contrast")
        self.toggle_button.clicked.connect(self.toggle_contrast)
        layout.addWidget(self.toggle_button)

        self.entry.returnPressed.connect(self.check_answer)  

        self.setCentralWidget(central_widget)
        
        self.next_question()

    def next_question(self):
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            question_expression, self.time_allotted, self.bell_needed = self.questions[self.current_question_index]
            display_text = f"{question_expression}"
            self.label.setText(display_text)
            self.entry.clear()
            self.entry.setFocus()
            self.update_gif("../images/question-1.gif") 
        else:
            self.label.setText("No more questions!")
            self.update_gif("../images/finished-1.gif") 


    def check_answer(self):
        if self.current_question_index < len(self.questions):
            user_answer = self.entry.text()
            correct_answer = eval(self.questions[self.current_question_index][0])
            if user_answer == str(correct_answer):
                self.label.setText("Excellent!")
                QTimer.singleShot(1000, self.next_question)
                self.update_gif("../images/excellent-1.gif")  
            else:
                self.update_gif("../images/wrong-anwser-1.gif")
                self.label.setText("Sorry! Let's try again")
                QTimer.singleShot(1000, self.show_question)


    def show_question(self):
        question_expression, _, _ = self.questions[self.current_question_index]
        display_text = f"{question_expression}"
        self.label.setText(display_text)
        self.entry.clear()
        self.entry.setFocus()
        self.update_gif("../images/question-1.gif")

    def toggle_contrast(self):
        if self.styleSheet() == "":
            self.setStyleSheet("QWidget { color: white; background-color: black; }")
        else:
            self.setStyleSheet("")

    def update_gif(self, gif_name):
        movie = QMovie(f"../images/{gif_name}")
        self.gif_label.setMovie(movie)
        movie.start()
        
    # def setup_audio(self):
    #     self.player = QMediaPlayer()
    #     content = QUrl.fromLocalFile("../sounds/backgroundmusic.ogg")
    #     self.player.source()
    #     self.player.play()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MathsTutorApp()
    window.show()
    sys.exit(app.exec())