import sys
import random
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *

class ChatbotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Rule-Based Chatbot")
        self.setGeometry(100, 100, 600, 400)

        # Set a solid background color
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor(220, 220, 220))
        self.setPalette(palette)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        self.text_display.setFont(QFont("Arial", 12))
        self.text_display.setStyleSheet("background-color: rgba(255, 255, 255, 0.7); border: 1px solid #333;")
        self.layout.addWidget(self.text_display)

        self.input_area = QTextEdit()
        self.input_area.setFont(QFont("Arial", 12))
        self.input_area.setStyleSheet("background-color: rgba(255, 255, 255, 0.7); border: 1px solid #333;")
        self.layout.addWidget(self.input_area)

        self.send_button = QPushButton("Send")
        self.send_button.setFont(QFont("Arial", 12))
        self.send_button.setStyleSheet("background-color: #4CAF50; color: white; border: none;")
        self.send_button.clicked.connect(self.handle_user_input)
        self.layout.addWidget(self.send_button)

        self.central_widget.setLayout(self.layout)

        self.chat_history = []
        self.responses = {
            "hello": "Hi there! How can I assist you?",
            "how are you": "I'm just a chatbot, but I'm here to help!",
            "goodbye": "Goodbye! Have a great day!",
            "age": "I'm just a program, so I don't have an age.",
            "name": "I'm chatbot, your friendly chatbot!",
            "weather": "I'm not connected to the internet, so I can't check the weather.",
            "help": "Sure, I can help with a variety of topics. Just ask me anything!",
            "thank you": "You're welcome!",
            "who are you": "I'm a chatbot created by Waleed Saeed.",
            "tell a joke": "Why did the chicken cross the road? To get to the other side!",
            "favorite color": "I don't have a favorite color, but I like all colors.",
            "tell a fact": "The Eiffel Tower in Paris is made up of 18,038 individual iron parts.",
            "how to learn programming": "To learn programming, start with the basics of a programming language and practice regularly.",
            "favorite food": "I don't eat, but I've heard pizza is quite popular!",
            "tell me a quote": "Here's a famous one: 'The only way to do great work is to love what you do.' - Steve Jobs",
            "tell me a story": "Once upon a time in a faraway land...",
            "math": "Sure, I can help with math problems. What do you need help with?",
            "tell a riddle": "I have keys but open no locks. I have space but no room. You can enter, but you can't go inside. What am I?",
            "programming languages": "There are many programming languages, such as Python, Java, C++, and more. Which one are you interested in?",
            "default": "I'm sorry, I don't understand that. Please ask something else.",
        }

    def handle_user_input(self):
        user_input = self.input_area.toPlainText().strip()
        if user_input:
            self.add_to_chat_history(f"You: {user_input}")
            response = self.get_bot_response(user_input)
            self.add_to_chat_history(f"Chatbot: {response}")
            self.input_area.clear()

    def get_bot_response(self, user_input):
        user_input = user_input.lower()
        for key, value in self.responses.items():
            if key in user_input:
                return value
        return self.responses["default"]

    def add_to_chat_history(self, message):
        self.chat_history.append(message)
        self.text_display.setPlainText("\n".join(self.chat_history))

def main():
    app = QApplication(sys.argv)
    window = ChatbotWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
