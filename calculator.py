import sys

from PySide6.QtWidgets import QApplication
from calculator_gui import Calculator

app = QApplication(sys.argv)
window = Calculator()
window.show()
app.exec()
