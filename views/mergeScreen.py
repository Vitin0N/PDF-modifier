from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QFrame, QHBoxLayout,
    QGridLayout
)
from PySide6.QtCore import Qt
import os

from interface.fileCard import FileCards
from components._chooseFileScreen import ChooseFileWidget

class MergeScreen(QWidget):
    def __init__(self):
        super().__init__()

        self.cards = []

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
        mainSettingLayout = QHBoxLayout(self.settingStep)

        # main content
        mainSide = QWidget()
        mainSideLayout = QVBoxLayout(mainSide)

        # helper buttons
        topButtons = QHBoxLayout()

        self.backBtn = QPushButton('Back')
        self.addFilesBtn = QPushButton('+')

        topButtons.addWidget(self.backBtn)
        topButtons.addStretch()
        topButtons.addWidget(self.addFilesBtn)

        mainSideLayout.addLayout(topButtons)

        # grid with the file icons
        self.fileFrame = QFrame()
        self.fileFrame.setFrameStyle(QFrame.StyledPanel)

        self.fileLayout = QGridLayout(self.fileFrame)
        self.fileLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        mainSideLayout.addWidget(self.fileFrame)

        # Settings side
        settingSide = QWidget()
        settingLayout = QVBoxLayout(settingSide)

        self.mergeBtn = QPushButton("Merge")
        self.mergeBtn.setMinimumHeight(60)
        
        nome = QLabel('teste de que esta indo para o lugar')
        nome.setWordWrap(True)
        nome.setAlignment(Qt.AlignTop)

        settingLayout.addWidget(nome)
        settingLayout.addStretch()
        settingLayout.addWidget(self.mergeBtn)

        # add to main layout
        mainSettingLayout.addWidget(mainSide, 3)      # Bigger
        mainSettingLayout.addWidget(settingSide, 1)   # Smaller

        # add screen to stack
        self.innerStack.addWidget(self.selectFileStep)
        self.innerStack.addWidget(self.settingStep)

        # save the selected files on this var
        self.selectedFile = []

        # buttons commands
        self.backBtn.clicked.connect(self.backChoosingFile)

    def continueToMergeScreen(self, filepaths):
        self.selectedFile = filepaths

        self.createFileCard(filepaths)

        self.updateCurrentGrid()

        self.innerStack.setCurrentIndex(1)

    def backChoosingFile(self):
        self.innerStack.setCurrentIndex(0)

    # helper functions
    def createFileCard(self, filepaths):
        self.cards.clear()

        for file in filepaths:
            filename = os.path.basename(file)
            filename = filename[:15] + '...' if len(filename) > 15 else filename

            card = FileCards(filename)

            self.cards.append(card)

    def updateCurrentGrid(self):
        width = self.fileFrame.width()

        cardWidth = 140

        # max colluns of fileFrame 
        collumns = max(1, width // cardWidth)

        # remove widget of fileLayout
        while self.fileLayout.count():
            item = self.fileLayout.takeAt(0)

        for index, card in enumerate(self.cards):
            row = index // collumns
            col = index % collumns

            self.fileLayout.addWidget(card, row, col)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.updateCurrentGrid()