from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QSizePolicy
)
from PySide6.QtCore import (
    Qt, Signal
)
from PySide6.QtGui import (
    QFont
)

from core.chooseFileDialog import chooseFile

class ChooseFileWidget(QWidget):
    fileSelected = Signal(list)

    # receives the title and subtitle of the current screen
    def __init__(self, title, subtitle):
        super().__init__()

        # vertically aligned layout
        cfLayout = QVBoxLayout(self)

        # font, label and button size settings
        titleFont = QFont()
        titleFont.setPixelSize(30)

        titleLabel = QLabel(f'<h1>{title}</h1>')
        titleLabel.setFont(titleFont)
        titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitleFont = QFont()
        subtitleFont.setPixelSize(18)

        subtitleLabel = QLabel(subtitle)
        subtitleLabel.setFont(subtitleFont)
        subtitleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        btnFont = QFont()
        btnFont.setPointSize(20)

        self.chooseBtn = QPushButton('Choose PDFs files')
        self.chooseBtn.setFont(btnFont)
        self.chooseBtn.setMinimumSize(300, 100)
        self.chooseBtn.setMaximumWidth(500)
        

        # add title, subtitle and choose file button to the layout
        cfLayout.addStretch()
        cfLayout.addWidget(titleLabel)
        cfLayout.addSpacing(10)
        cfLayout.addWidget(subtitleLabel)
        cfLayout.addSpacing(50)
        cfLayout.addWidget(self.chooseBtn, alignment=Qt.AlignCenter)
        cfLayout.addStretch()

        # connect the button to the choose file function
        self.chooseBtn.clicked.connect(lambda: self.searchFile(title))

    def searchFile(self, title):
        if title == 'merge':
            filepaths = chooseFile(self, 'multiple')

        else:
            filepaths = chooseFile(self, 'single')

        if filepaths:
            self.fileSelected.emit(filepaths)
