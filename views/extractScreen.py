from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QFrame, QHBoxLayout,
    QGridLayout, QScrollArea, QGraphicsBlurEffect, QButtonGroup, QLineEdit, QCheckBox
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QPixmap

from components._chooseFileScreen import ChooseFileWidget
from components.loadingDialog import LoadingDialog
from components.dropPageGridFrame import DrogGridFrame
from components.pageCard import PageCard
from core.thumbWorker import ThumbWorker


class ExtractScreen(QWidget):
    def __init__(self):
        super().__init__()

        # initial var
        self.selectFile = ''
        self.pages = []

        # screen construction
        mainLayout = QVBoxLayout(self)
        self.innerStack = QStackedWidget()
        mainLayout.addWidget(self.innerStack)

        # choose file screen
        self.selectFileStep = ChooseFileWidget(
            'Extract Pages from PDF',
            'Separate one or a set of pages that can become one or more PDFs!'
        )

        self.selectFileStep.fileSelected.connect(self.continueToExtractScreen)

        # setting and complete process screen
        self.settingStep = QWidget()
        mainSettingLayout = QHBoxLayout(self.settingStep)

        # loading for setting Step
        self.loading = LoadingDialog(self.settingStep)

        self.mainSide = QWidget()
        mainSideLayout = QVBoxLayout(self.mainSide)

        # tobar button
        topButtons = QHBoxLayout()

        self.backButton = QPushButton('Back')

        topButtons.addWidget(self.backButton)
        topButtons.addStretch()

        mainSideLayout.addLayout(topButtons)

        # scroll area for PDF's pages
        self.filePageFrame = QScrollArea()
        self.filePageFrame.setWidgetResizable(True)

        self.pagesFrame = DrogGridFrame()
        self.pagesFrame.reordered.connect(self.reoderCards) 
        self.pagesFrame.setFrameStyle(QFrame.StyledPanel)

        self.pageLayout = QGridLayout()
        self.pageLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.pagesFrame.setLayout(self.pageLayout)

        self.filePageFrame.setWidget(self.pagesFrame)

        mainSideLayout.addWidget(self.filePageFrame)

        # setting side
        self.settingSide = QWidget()
        settingLayout = QVBoxLayout(self.settingSide)

        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)

        # text style for extract button
        extractBtnFont = QFont()
        extractBtnFont.setPixelSize(30)
        extractBtnFont.setBold(True)

        self.extractBtn = QPushButton("Extract Pages")
        self.extractBtn.setFont(extractBtnFont)
        self.extractBtn.setStyleSheet('''
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
        self.extractBtn.setMinimumHeight(60)

        nameFont = QFont()
        nameFont.setPixelSize(30)
        nameFont.setBold(True)

        name = QLabel('Extract Pages') 
        name.setFont(nameFont)
        name.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        # options tab
        optionLabel = QLabel('Extract mode:')

        optionTabLayout = QHBoxLayout()

        allPagesBtn = QPushButton('Extract all pages')
        allPagesBtn.setCheckable(True)
        allPagesBtn.setCursor(Qt.PointingHandCursor)
        allPagesBtn.setMinimumHeight(50)
        allPagesBtn.setChecked(True)

        selectPageBtn = QPushButton('Select pages')
        selectPageBtn.setCheckable(True)
        selectPageBtn.setCursor(Qt.PointingHandCursor)
        selectPageBtn.setMinimumHeight(50)

        optionGroup = QButtonGroup(self)
        optionGroup.setExclusive(True)
        optionGroup.addButton(allPagesBtn)
        optionGroup.addButton(selectPageBtn)

        style = '''
            QPushButton {
                background-color: #2b2b2b;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }

            QPushButton:hover {
                border: 2px solid #e5322d;
                color: #e5322d;
            }

            QPushButton:checked {
                background-color: #e5322d;
            }

            QPushButton:checked:hover {
                background-color: #C72B27;
                color: white;
                border: none;
            }
        '''

        allPagesBtn.setStyleSheet(style)
        selectPageBtn.setStyleSheet(style)

        optionTabLayout.addWidget(allPagesBtn)
        optionTabLayout.addWidget(selectPageBtn)

        # option info text
        self.settingStack = QStackedWidget()

        # ===== all pages box information =====
        allPagesInfo = QWidget()
        allPagesLayout = QVBoxLayout(allPagesInfo)

        allPagesText = QLabel('Extract all pages:')
        allPagesText.setWordWrap(True)

        # all page info text
        self.allPagesInfoContainer = QFrame()
        allPagesInfoLayout = QVBoxLayout(self.allPagesInfoContainer)
        self.allPagesInfoContainer.setStyleSheet('''
            QFrame {
                background-color: #def2ff;
                border-radius: 10px;
                padding: 0px 5px;
            }
        ''')

        allPagesInfoText = QLabel('ℹ️Selected pages will be convert to separated PDFs files.')
        allPagesInfoText.setWordWrap(True)
        allPagesInfoText.setStyleSheet('color: black;')
        allPagesInfoText.setAlignment(Qt.AlignCenter)

        allPagesInfoLayout.addWidget(allPagesInfoText)
        
        allPagesLayout.addWidget(allPagesText)
        allPagesLayout.addSpacing(30)
        allPagesLayout.addWidget(self.allPagesInfoContainer)
        allPagesLayout.addStretch()

        # ==== select pages box information =====
        selectPageInfo = QWidget()
        selectPageLayout = QVBoxLayout(selectPageInfo)

        selectPageText = QLabel('Extract Mode:')
        selectPageText.setWordWrap(True)

        # input for the selected pages
        self.pageInput = QLineEdit()
        self.pageInput.setPlaceholderText('Example: 1-5,8-10')
        self.pageInput.setMinimumHeight(35)

        # extract to one pdf chebok
        self.extractToOne = QCheckBox('Merge extract pages into one PDF!')

        # select page info text
        self.selectInfoContainer = QFrame()
        selectInfoLayout = QVBoxLayout(self.selectInfoContainer)
        self.selectInfoContainer.setStyleSheet('''
            QFrame {
                background-color: #def2ff;
                border-radius: 10px;
                padding: 0px 5px;
            }
        ''')

        selectPageInfoText = QLabel('ℹ️Selected pages will be convert to separated PDFs files.')
        selectPageInfoText.setWordWrap(True)
        selectPageInfoText.setStyleSheet('color: black;')
        selectPageInfoText.setAlignment(Qt.AlignCenter)

        selectInfoLayout.addWidget(selectPageInfoText)

        self.extractToOne.toggled.connect(
            self.toggleSelectInfo
        )

        selectPageLayout.addWidget(selectPageText)
        selectPageLayout.addWidget(self.pageInput)
        selectPageLayout.addWidget(self.extractToOne)
        selectPageLayout.addSpacing(10)
        selectPageLayout.addWidget(self.selectInfoContainer)
        selectPageLayout.addStretch()

        self.settingStack.addWidget(allPagesInfo)
        self.settingStack.addWidget(selectPageInfo)

        allPagesBtn.clicked.connect(
            lambda: self.settingStack.setCurrentIndex(0)
        )
        
        selectPageBtn.clicked.connect(
            lambda: self.settingStack.setCurrentIndex(1)
        )

        # add elements in setting layout
        settingLayout.addWidget(name)
        settingLayout.addSpacing(10)
        settingLayout.addWidget(line)
        settingLayout.addWidget(optionLabel)
        settingLayout.addLayout(optionTabLayout)
        settingLayout.addWidget(self.settingStack)
        settingLayout.addStretch()
        settingLayout.addWidget(self.extractBtn)
        settingLayout.addSpacing(20)

        # add the main and setting canva
        mainSettingLayout.addWidget(self.mainSide, 2)
        mainSettingLayout.addWidget(self.settingSide, 1)

        # add screen to stack
        self.innerStack.addWidget(self.selectFileStep)
        self.innerStack.addWidget(self.settingStep)

    def continueToExtractScreen(self, filepath):
        self.loading.showOverlay('', mode='spin')

        self.innerStack.setCurrentIndex(1)
        QTimer.singleShot(
            0,
            lambda: self.loadExtractScreen(filepath)
        )

    def loadExtractScreen(self, filepath):
        self.selectFile = filepath

        # TODO criar as paginas e fazer o updategrid
        self.clearPages()
        self.filepath = "".join(filepath)

        self.thumbWoker = ThumbWorker(self.filepath)
        self.thumbWoker.pageRendered.connect(self.addPageCard)
        self.thumbWoker.finished.connect(self.loading.hideOverlay)

        self.thumbWoker.start()

    def resetScreen(self):
        self.selectFile = ''
        self.filepath = ''
        self.clearPages()
        self.innerStack.setCurrentIndex(0)

    def addPageCard(self, pageIndex, qimage):
        pixmap = QPixmap.fromImage(qimage)
        card = PageCard(pageIndex, pixmap)

        self.pages.append(card)

        self.updateCurrentGrid()

    def updateCurrentGrid(self):
        if not self.pages:
            return
        
        width = self.filePageFrame.viewport().width()
        cardWidth = 170

        collunms = max(1, width // cardWidth)

        while self.pageLayout.count():
            item = self.pageLayout.takeAt(0)

        for index, card in enumerate(self.pages):
            row = index // collunms
            col = index % collunms
            self.pageLayout.addWidget(card, row, col)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.updateCurrentGrid()

    def clearPages(self):
        for page in self.pages:
            self.pageLayout.removeWidget(page)
            page.deleteLater()
        
        self.pages.clear()

    def reoderCards(self, index, newIndex):
        oldIndex = -1

        for i, card in enumerate(self.pages):
            if card.pageIndex == index:
                oldIndex = i
                break


        if oldIndex == newIndex or oldIndex == -1:
            return
        
        reoderPage = self.pages.pop(oldIndex)
        self.pages.insert(newIndex, reoderPage)

        self.updateCurrentGrid()

    def toggleSelectInfo(self, checked):
        if checked:
            self.selectInfoContainer.hide()
        else:
            self.selectInfoContainer.show()
            