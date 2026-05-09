from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QFrame, QHBoxLayout,
    QGridLayout, QScrollArea, QGraphicsBlurEffect, QRadioButton, QButtonGroup
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

from components._chooseFileScreen import ChooseFileWidget
from components.loadingDialog import LoadingDialog
from components.dropGridFrame import DrogGridFrame


class ExtractScreen(QWidget):
    def __init__(self):
        super().__init__()

        mainLayout = QVBoxLayout(self)
        self.innerStack = QStackedWidget()
        mainLayout.addWidget(self.innerStack)

        # choose file screen
        self.selectFileStep = ChooseFileWidget(
            'Extract Pages from PDF',
            'Separate one or a set of pages that can become one or more PDFs!'
        )

        # self.selectFileStep.fileSelected.connect(...) # TODO make the function

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
        # self.pagesFrame.reordered.connect(...) # TODO make the function
        self.pagesFrame.setFrameStyle(QFrame.StyledPanel)

        self.pageLayout = QGridLayout()
        self.pageLayout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

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

        # all pages box information
        allPagesInfo = QWidget()
        allPagesLayout = QVBoxLayout(allPagesInfo)

        allPagesText = QLabel('All pages kakakak')

        allPagesText.setWordWrap(True)
        
        allPagesLayout.addWidget(allPagesText)
        allPagesLayout.addStretch()

        # select pages box information
        selectPageInfo = QWidget()
        selectPageLayout = QVBoxLayout(selectPageInfo)

        selectPageText = QLabel('Select pages akakkakaka')
        selectPageText.setWordWrap(True)

        selectPageLayout.addWidget(selectPageText)
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
        self.innerStack.addWidget(self.settingStep)
        self.innerStack.addWidget(self.selectFileStep)

