from PySide6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget, QLabel
)
from PySide6.QtGui import QFont
from PySide6.QtCore import Qt, Signal

class SuccessScreen(QWidget):
    gotoHomeScreen = Signal()

    def __init__(self, process):
        super().__init__()

        sucesLayout = QVBoxLayout(self)

        titleFont = QFont()
        titleFont.setPixelSize(40)
        titleFont.setBold(True)

        successTitle = QLabel(f'{process} completed successfully')
        successTitle.setAlignment(Qt.AlignCenter)
        successTitle.setFont(titleFont)
        successTitle.setWordWrap(True)

        backBtnFont = QFont()
        backBtnFont.setPixelSize(30)
        backBtnFont.setBold(True)

        backToHomeScreenBtn = QPushButton('Home Screen')
        backToHomeScreenBtn.setMinimumSize(300, 150)
        backToHomeScreenBtn.setMaximumWidth(400)
        backToHomeScreenBtn.setFont(backBtnFont)

        sucesLayout.addStretch()
        sucesLayout.addWidget(successTitle)
        sucesLayout.addSpacing(25)
        sucesLayout.addWidget(backToHomeScreenBtn, alignment=Qt.AlignCenter)
        sucesLayout.addStretch()

        backToHomeScreenBtn.clicked.connect(self.gotoHomeScreen.emit)

