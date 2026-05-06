from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QFrame, QHBoxLayout,
    QGridLayout
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
        mainSettingLayout = QHBoxLayout(self.settingStep)

        # main content
        mainSide = QWidget()
        mainSideLayout = QVBoxLayout(mainSide)

        # helper buttons
        topButtons = QHBoxLayout()

        self.backBtn = QPushButton('Back')
        self.addFilesBtn = QPushButton('+')

        topButtons.addWidget(self.backBtn)
        topButtons.addWidget(self.addFilesBtn)

        mainSideLayout.addLayout(topButtons)

        # grid with the file icons
        self.fileFrame = QFrame()
        self.fileFrame.setFrameStyle(QFrame.StyledPanel)

        self.fileLayout = QGridLayout(self.fileFrame)

        mainSideLayout.addWidget(self.fileFrame)

        # Settings side
        settingSide = QWidget()
        settingLayout = QVBoxLayout(settingSide)

        self.mergeBtn = QPushButton("Merge")
        self.mergeBtn.setMinimumHeight(60)
        
        nome = QLabel('teste de que esta indo para o lugar correto')

        settingLayout.addWidget(nome)
        settingLayout.addWidget(self.mergeBtn)
        settingLayout.addStretch()


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

        self.innerStack.setCurrentIndex(1)

    def backChoosingFile(self):
        self.innerStack.setCurrentIndex(0)
        