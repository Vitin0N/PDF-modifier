from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QFrame, QHBoxLayout,
    QGridLayout, QScrollArea, QGraphicsBlurEffect
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
import os
import time

from ui.widgets.fileCard import FileCards
from components._chooseFileScreen import ChooseFileWidget
from core.chooseFileDialog import chooseFile
from ui.widgets.loadingDialog import LoadingDialog
from core.worker.mergeWorker import MergeWorker
from ui.layouts.dropFileGridFrame import DrogGridFrame

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

        # loading setting
        self.loadingProcess = LoadingDialog(self.settingStep)
        
        # main content
        self.mainSide = QWidget()
        mainSideLayout = QVBoxLayout(self.mainSide)

        # helper buttons
        topButtons = QHBoxLayout()

        self.backBtn = QPushButton('Back')

        # Add file settings
        addFileBtnFont = QFont()
        addFileBtnFont.setPixelSize(12)
        addFileBtnFont.setBold(True)

        self.addFilesBtn = QPushButton('+')
        self.addFilesBtn.setFixedSize(24, 24)
        self.addFilesBtn.setCursor(Qt.PointingHandCursor)
        self.addFilesBtn.setFont(addFileBtnFont)
        self.addFilesBtn.setStyleSheet('''
            QPushButton {
                border: none;
                border-radius: 9px;
                background-color: #e5322d;
                color: white;
                text-align: center;
            }
                                       
            QPushButton:hover {
                background-color: #c92a25;
            }
        ''')

        topButtons.addWidget(self.backBtn)
        topButtons.addStretch()
        topButtons.addWidget(self.addFilesBtn)

        mainSideLayout.addLayout(topButtons)

        # scroll area for files
        self.fileScrollArea = QScrollArea()
        self.fileScrollArea.setWidgetResizable(True)

        # grid with the file icons
        self.fileFrame = DrogGridFrame()
        self.fileFrame.reordered.connect(self.reorderCards)
        self.fileFrame.setFrameStyle(QFrame.StyledPanel)

        self.fileLayout = QGridLayout(self.fileFrame)
        self.fileLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.fileScrollArea.setWidget(self.fileFrame)

        mainSideLayout.addWidget(self.fileScrollArea)

        # Settings side
        self.settingSide = QWidget()
        settingLayout = QVBoxLayout(self.settingSide)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        # text style for merge button
        mergeBtnFont = QFont()
        mergeBtnFont.setPixelSize(30)
        mergeBtnFont.setBold(True)

        self.mergeBtn = QPushButton("Merge PDFs")
        self.mergeBtn.setFont(mergeBtnFont)
        self.mergeBtn.setStyleSheet('''
            QPushButton {
                background-color: #e5322d;
                color: white;
                border: none;
                border-radius: 10px;  
                padding: 10px;
            }
                                    
            QPushButton[blocked="false"]:hover {
                background-color: #c92a25;
            }
                                    
            QPushButton[blocked="true"] {
                background-color: #731916;
                color: #eeeeee;
            }                      
        ''')
        self.mergeBtn.setMinimumHeight(80)

        nameFont = QFont()
        nameFont.setPixelSize(30)
        nameFont.setBold(True)
        
        name = QLabel(f'MERGE')
        
        name.setFont(nameFont)
        name.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        infoContainer = QFrame()
        infoLayout = QVBoxLayout(infoContainer)
        infoContainer.setStyleSheet('''
            QFrame {
                background-color: #def2ff;
                border-radius: 10px;
                padding: 0px 5px;
            }
        ''')

        infoText = QLabel('ℹ️ The merge order will be the order thats appears on the screen, ' \
                            'so the PDFs will me merged based on the order in which you selected them.\n\n' \
                            'You can still change the order by dragging the cards and placing them in the desired position.')
        infoText.setAlignment(Qt.AlignCenter)
        infoText.setStyleSheet('color: black;')
        infoText.setWordWrap(True)

        infoLayout.addWidget(infoText)

        # info text for when don't have enough files
        self.canMergeContainer = QFrame()
        canMergeLayout = QVBoxLayout(self.canMergeContainer)

        canMergeFont = QFont()
        canMergeFont.setBold(True)
        canMergeFont.setPixelSize(10)

        canMergeText = QLabel('You can only merge if there is more than one PDF file.')
        canMergeText.setFont(canMergeFont)
        canMergeText.setAlignment(Qt.AlignCenter)
        canMergeText.setWordWrap(True)

        canMergeLayout.addWidget(canMergeText)
        self.canMergeContainer.hide()

        # add elements in setting layout
        settingLayout.addWidget(name)
        settingLayout.addSpacing(10)
        settingLayout.addWidget(line)
        settingLayout.addWidget(infoContainer)
        settingLayout.addStretch()
        settingLayout.addWidget(self.canMergeContainer)
        settingLayout.addWidget(self.mergeBtn)
        settingLayout.addSpacing(20)

        # add to main layout
        mainSettingLayout.addWidget(self.mainSide, 2)      # Bigger
        mainSettingLayout.addWidget(self.settingSide, 1)   # Smaller

        # add screen to stack
        self.innerStack.addWidget(self.selectFileStep)
        self.innerStack.addWidget(self.settingStep)

        # save the selected files on this var
        self.selectedFile = []

        # buttons commands
        self.backBtn.clicked.connect(self.backChoosingFile)
        self.addFilesBtn.clicked.connect(self.addFiles)
        self.mergeBtn.clicked.connect(self.mergePdfs)

    # screen functions
    def continueToMergeScreen(self, filepaths):
        self.loadingProcess.showOverlay('', mode='spin')
        
        self.innerStack.setCurrentIndex(1)
        QTimer.singleShot(
            0, 
            lambda: self.loadMergeScreen(filepaths)
        )

    def loadMergeScreen(self, filepaths):
        self.selectedFile = filepaths

        self.updateMergeBtnState()
        self.createFileCard(filepaths)

        QTimer.singleShot(0, self.updateCurrentGrid)
        self.loadingProcess.hideOverlay()


    def backChoosingFile(self):
        self.selectedFile.clear()
        self.clearCards()

        self.innerStack.setCurrentIndex(0)

    def resetScreen(self):
        '''
        Reset all main parameters and return to the file selection screen
        '''
        self.selectedFile.clear()
        self.clearCards()
        self.updateMergeBtnState()
        self.innerStack.setCurrentIndex(0)

    # helper functions
    def createFileCard(self, filepaths):
        self.clearCards()

        for file in filepaths:
            filepath = file
            filename = os.path.basename(file)
            filename = filename[:15] + '...' if len(filename) > 15 else filename

            card = FileCards(filename, filepath)
            card.removeRequest.connect(self.removeCard)

            self.cards.append(card)

    def addFiles(self):
        newFilepaths = chooseFile(self, 'multiple')

        self.selectedFile += newFilepaths

        self.createFileCard(self.selectedFile)
        self.updateMergeBtnState()

        self.updateCurrentGrid()

    def removeCard(self, card):
        '''
        Remove the card when clicked on delete file button
        '''
        self.cards.remove(card)
        
        self.selectedFile.remove(card.filepath)
        self.updateMergeBtnState()

        card.deleteLater()

        self.updateCurrentGrid()
    
    def clearCards(self):
        for card in self.cards:
            self.fileLayout.removeWidget(card)
            card.deleteLater()

        self.cards.clear()

    def updateCurrentGrid(self):
        width = self.fileScrollArea.viewport().width()

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
        
        self.loadingProcess.resize(self.settingStep.size())

    def changeMergeBtnState(self, block: bool):
        self.mergeBtn.setProperty('blocked', block)
        
        if block:
            self.mergeBtn.setCursor(Qt.ForbiddenCursor)
            self.canMerge = False
        else:
            self.mergeBtn.setCursor(Qt.PointingHandCursor)
            self.canMerge = True

        # remove the currente style and add it again
        self.mergeBtn.style().unpolish(self.mergeBtn)
        self.mergeBtn.style().polish(self.mergeBtn) 

    def updateMergeBtnState(self):
        hasEnoughFiles = len(self.selectedFile) >= 2

        self.canMerge = hasEnoughFiles

        if hasEnoughFiles:

            self.changeMergeBtnState(False)

            self.canMergeContainer.hide()
        else:
            self.canMergeContainer.show()

            self.changeMergeBtnState(True)

    def reorderCards(self, filepath, newIndex):
        oldIndex = self.selectedFile.index(filepath)

        if oldIndex == newIndex:
            return
        
        reoderFile = self.selectedFile.pop(oldIndex)
        self.selectedFile.insert(newIndex, reoderFile)

        card = self.cards.pop(oldIndex)
        self.cards.insert(newIndex, card)

        self.updateCurrentGrid()

    def mergePdfs(self):
        if not self.canMerge:
            return
        
        # block the button on the processing
        self.changeMergeBtnState(True)

        # set blur effect
        self.mainBlur = QGraphicsBlurEffect()
        self.mainBlur.setBlurRadius(8)
        self.mainSide.setGraphicsEffect(self.mainBlur)

        self.settingBlur = QGraphicsBlurEffect()
        self.settingBlur.setBlurRadius(8)
        self.settingSide.setGraphicsEffect(self.settingBlur)

        # TODO processing merge PDF
        self.loadingProcess.showOverlay('Merging PDFs...', mode='progress')

        self.worker = MergeWorker(self.selectedFile)

        self.worker.progress.connect(
            self.loadingProcess.updateProgress
        )

        self.worker.finished.connect(
            self.finishMerge
        )

        self.worker.start()

    def finishMerge(self):  

        # remove blur effect
        self.mainSide.setGraphicsEffect(None)
        self.settingSide.setGraphicsEffect(None)

        self.loadingProcess.progressBar.setValue(0)

        self.loadingProcess.hideOverlay()

        self.changeMergeBtnState(False)

        print('Terminou')

        self.resetScreen()
        