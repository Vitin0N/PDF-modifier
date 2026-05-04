from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QStackedWidget
)
from PySide6.QtCore import Qt

class MergeSreen(QWidget):
    def __init__(self):
        super().__init__()

        mainLayout = QVBoxLayout(self)

        