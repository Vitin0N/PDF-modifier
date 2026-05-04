from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QSizePolicy
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

    def __init__(self, title, subtitle):
        super().__init__()

        self.title = title.lower()

        cfLayout = QVBoxLayout(self)

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
        
        
        
        cfLayout.addStretch()
        cfLayout.addWidget(titleLabel)
        cfLayout.addSpacing(10)
        cfLayout.addWidget(subtitleLabel)
        cfLayout.addSpacing(50)
        cfLayout.addWidget(self.chooseBtn, alignment=Qt.AlignCenter)
        cfLayout.addStretch()

        self.chooseBtn.clicked.connect(self.searchFile)

    def searchFile(self):
        if self.title == 'merge':
            filepaths = chooseFile(self, 'multiple')

        else:
            filepaths = chooseFile(self, 'single')

        if filepaths:
            self.fileSelected.emit(filepaths)
