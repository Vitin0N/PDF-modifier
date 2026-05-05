from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QStackedWidget
)
from PySide6.QtCore import Qt

from components._chooseFileScreen import ChooseFileWidget

class MergeScreen(QWidget):
    def __init__(self):
        super().__init__()

        mainLayout = QVBoxLayout(self)
        self.innerStack = QStackedWidget()
        mainLayout.addWidget(self.innerStack)

        self.selectFileStep = ChooseFileWidget(
            'Merge PDFs',
            'Merge PDFs in order you want, choose the order of the files to be merged!'
        )

        self.selectFileStep.fileSelected.connect(self.continueToMergeScreen)

        # setting and complete process screen
        self.settingStep = QWidget()
        settingLayout = QVBoxLayout(self.settingStep)

        self.sttgLabel = QLabel("Merge")
        self.backBtn = QPushButton('Back')

        settingLayout.addWidget(self.sttgLabel)
        settingLayout.addWidget(self.backBtn)

        self.backBtn.clicked.connect(self.backChoosingFile)

        # add screen to stack
        self.innerStack.addWidget(self.selectFileStep)
        self.innerStack.addWidget(self.settingStep)

        # save the selected files on this var
        self.selectedFile = []

    def continueToMergeScreen(self, filepaths):
        self.selectedFile = filepaths

        self.innerStack.setCurrentIndex(1)

    def backChoosingFile(self):
        self.innerStack.setCurrentIndex(0)
        