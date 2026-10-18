from PySide6.QtWidgets import QWidget, QVBoxLayout
from gui.widgets.message_area import MessageArea
from gui.widgets.input_bar import InputBar


class ChatWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.messages = MessageArea()
        self.input_bar = InputBar()

        layout.addWidget(self.messages, 1)
        layout.addWidget(self.input_bar)

        self.input = self.input_bar.input
        self.send_button = self.input_bar.send_button
        self.voice_button = self.input_bar.voice_button

    def add_user_message(self, text):
        self.messages.add_user_message(text)

    def add_ai_message(self, text):
        self.messages.add_ai_message(text)

    def clear_chat(self):
        self.messages.clear()
