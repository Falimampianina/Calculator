from functools import partial

from PySide6 import QtCore
from PySide6.QtGui import QIcon, QShortcut, QKeySequence
from PySide6.QtWidgets import QWidget, QGridLayout, QLineEdit, QPushButton, QSizePolicy


class Calculator(QWidget):
    BUTTONS = {
        "c": (1, 0, 1, 2),
        "/": (1, 3, 1, 1),
        "7": (2, 0, 1, 1),
        "8": (2, 1, 1, 1),
        "9": (2, 2, 1, 1),
        "4": (3, 0, 1, 1),
        "5": (3, 1, 1, 1),
        "6": (3, 2, 1, 1),
        "1": (4, 0, 1, 1),
        "2": (4, 1, 1, 1),
        "3": (4, 2, 1, 1),
        "x": (2, 3, 1, 1),
        "-": (3, 3, 1, 1),
        "+": (4, 3, 1, 1),
        "0": (5, 0, 1, 2),
        ".": (5, 2, 1, 1),
        "=": (5, 3, 1, 1)
    }

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setWindowIcon(QIcon("images/calc.png"))
        self.setStyleSheet("""
            background-color: rgb(20, 20, 20);
            color: rgb(220, 220, 220);
            font-size: 18px;
        """)

        self.main_layout = QGridLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.le_result = QLineEdit()
        self.le_result.setPlaceholderText("0")
        self.le_result.setReadOnly(True)
        self.le_result.setAlignment(QtCore.Qt.AlignRight)
        self.le_result.setMinimumHeight(50)
        self.le_result.setStyleSheet("""
            border: none;
            border-bottom: 2px solid rgb(30, 30, 30);
            padding: 0 8px;
            font-size: 24px;
            font-weight: bold
        """)
        self.main_layout.addWidget(self.le_result, 0, 0, 1, 4)
        self.buttons = dict()
        for button_text, button_position in Calculator.BUTTONS.items():
            button = QPushButton(button_text)
            button.setMinimumSize(50, 50)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            self.main_layout.addWidget(button, *button_position)
            button.setStyleSheet(f"""
                QPushButton {{
                                  border: none;
                                  font-weight: bold;
                                  background-color: {'#1e1e2d' if button_text in ("+", "-", "x", "/") else 'none'};      
                }}
                QPushButton:pressed {{
                                  background-color: #f31d58;  
                }}            
            """)
            self.buttons[button_text] = button

        self.buttons["c"].clicked.connect(self.le_result.clear)

        for key, button in self.buttons.items():
            if key not in ("c", "="):
                button.clicked.connect(partial(self.button_clicked, key))

        self.buttons["="].clicked.connect(self.compute)
        self.buttons["="].setStyleSheet("""
                background-color: rgb(120, 120, 120);
                border: none;
        """)

        self.connect_keyboard_shortcuts()

    def button_clicked(self, text):
        if text in ("+", "-", "x", "/"):
            if len(self.le_result.text()) == 0:
                return
            elif self.le_result.text()[-1] in ("+", "-", "x", "/"):
                return
        self.le_result.setText(self.le_result.text() + text)

    def compute(self):
        try:
            result = eval(self.le_result.text().replace("x", "*"))
            self.le_result.setText(str(result))
        except SyntaxError:
            return
        except ZeroDivisionError:
            return

    def delete_last_character(self):
        self.le_result.setText(self.le_result.text()[:len(self.le_result.text()) - 1])

    def connect_keyboard_shortcuts(self):
        for button_text, button in self.buttons.items():
            QShortcut(QKeySequence(button_text), self, button.clicked.emit)
        QShortcut(QKeySequence(QtCore.Qt.Key_Return), self, self.compute)
        QShortcut(QKeySequence(QtCore.Qt.Key_Backspace), self, self.delete_last_character)
