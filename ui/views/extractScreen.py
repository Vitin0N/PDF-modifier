from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QFrame, QHBoxLayout,
    QGridLayout, QScrollArea, QGraphicsBlurEffect, QButtonGroup, QLineEdit, QCheckBox,
    QFileDialog
)
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QFont, QPixmap

from components._chooseFileScreen import ChooseFileWidget
from ui.widgets.loadingDialog import LoadingDialog
from ui.layouts.dropPageGridFrame import DrogGridFrame
from ui.widgets.pageCard import PageCard
from core.worker.thumbWorker import ThumbWorker
from core.worker.extractWorker import ExtractWorker
from components.successScreen import SuccessScreen

class ExtractScreen(QWidget):
    returnToHome = Signal()
    
    def __init__(self):
        super().__init__()

        # initial var
        self.selectFile = ''
        self.pages = []
        self.selectedPages = set()
        self.currentCollumns = 0

        # timer to resize
        self.resizeTimer = QTimer()
        self.resizeTimer.setSingleShot(True)
        self.resizeTimer.timeout.connect(self.updateCurrentGrid)

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

        # Success Screen Step
        self.successScreen = SuccessScreen("Extract")

        # loading for setting Step
        self.loading = LoadingDialog(self.settingStep)

        self.mainSide = QWidget()
        mainSideLayout = QVBoxLayout(self.mainSide)

        # tobar button
        topButtons = QHBoxLayout()

        self.backButton = QPushButton('Back')
        self.backButton.clicked.connect(self.backToChooseFileScreen)

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

        canExtractFont = QFont()
        canExtractFont.setBold(True)
        canExtractFont.setPixelSize(13)

        self.canExtractText = QLabel('You can only extract if there is more than one page selected file.')
        self.canExtractText.setFont(canExtractFont)
        self.canExtractText.setAlignment(Qt.AlignCenter)
        self.canExtractText.setWordWrap(True)
        self.canExtractText.hide()

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
        self.extractBtn.clicked.connect(self.extractPages)

        nameFont = QFont()
        nameFont.setPixelSize(30)
        nameFont.setBold(True)

        name = QLabel('Extract Pages') 
        name.setFont(nameFont)
        name.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        # options tab
        optionLabel = QLabel('Extract mode:')

        optionTabLayout = QHBoxLayout()

        self.allPagesBtn = QPushButton('Extract all pages')
        self.allPagesBtn.setCheckable(True)
        self.allPagesBtn.setCursor(Qt.PointingHandCursor)
        self.allPagesBtn.setMinimumHeight(50)
        self.allPagesBtn.setChecked(True)

        self.allPagesBtn.clicked.connect(self.selectAllPages)

        selectPageBtn = QPushButton('Select pages')
        selectPageBtn.setCheckable(True)
        selectPageBtn.setCursor(Qt.PointingHandCursor)
        selectPageBtn.setMinimumHeight(50)

        selectPageBtn.clicked.connect(self.enableSelectMode)

        optionGroup = QButtonGroup(self)
        optionGroup.setExclusive(True)
        optionGroup.addButton(self.allPagesBtn)
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

        self.allPagesBtn.setStyleSheet(style)
        selectPageBtn.setStyleSheet(style)

        optionTabLayout.addWidget(self.allPagesBtn)
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

        self.allPagesInfoText = QLabel()
        self.allPagesInfoText.setWordWrap(True)
        self.allPagesInfoText.setStyleSheet('color: black;')
        self.allPagesInfoText.setAlignment(Qt.AlignCenter)

        allPagesInfoLayout.addWidget(self.allPagesInfoText)
        
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

        self.pageInput.textChanged.connect(self.selectPages)

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

        self.selectPageInfoText = QLabel()
        self.selectPageInfoText.setWordWrap(True)
        self.selectPageInfoText.setStyleSheet('color: black;')
        self.selectPageInfoText.setAlignment(Qt.AlignCenter)

        selectInfoLayout.addWidget(self.selectPageInfoText)

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

        self.allPagesBtn.clicked.connect(
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
        settingLayout.addWidget(self.canExtractText)
        settingLayout.addWidget(self.extractBtn)
        settingLayout.addSpacing(20)

        # add the main and setting canva
        mainSettingLayout.addWidget(self.mainSide, 2)
        mainSettingLayout.addWidget(self.settingSide, 1)

        # add screen to stack
        self.innerStack.addWidget(self.selectFileStep)
        self.innerStack.addWidget(self.settingStep)
        self.innerStack.addWidget(self.successScreen)

        self.successScreen.gotoHomeScreen.connect(self.handleGoHome)


    # ===== Funtions =====
    def backToChooseFileScreen(self):
        # stop thumbnail redering thread
        if hasattr(self, 'thumbWorker') and self.thumbWorker.isRunning():
            self.thumbWorker.quit()
            self.thumbWorker.wait()

        # reset all screen component and page card
        self.resetScreen()
        self.clearPages()

        # change stack to choose file screen
        self.innerStack.setCurrentIndex(0)

    def continueToExtractScreen(self, filepath):
        # show loading overlay
        self.loading.showOverlay('', mode='spin')

        # switch to extract screen
        self.innerStack.setCurrentIndex(1)

        # call the load extract screen
        QTimer.singleShot(
            0,
            lambda: self.loadExtractScreen(filepath)
        )

    def loadExtractScreen(self, filepath):
        # store the filepath
        self.selectFile = filepath

        # if exist clear the old pages
        self.clearPages()
        self.filepath = "".join(filepath)

        # create worker thread for thumbnail rendering
        self.thumbWorker = ThumbWorker(self.filepath)

        # add pages whenever a page is rendered
        self.thumbWorker.pageRendered.connect(self.addPageCard)

        # hide loading overlay
        self.thumbWorker.finished.connect(self.loading.hideOverlay)
        self.thumbWorker.finished.connect(self.selectAllPages)

        self.thumbWorker.start()

    def resetScreen(self):
        # reset all file data
        self.selectFile = ''
        self.filepath = ''
        self.selectedPages.clear()
        self.clearPages()

        # reset thumbWorker
        if hasattr(self, 'thumbWorker'):
            self.thumbWorker = None

        # restore default UI
        self.allPagesBtn.setChecked(True)
        self.settingStack.setCurrentIndex(0)
        self.innerStack.setCurrentIndex(0)

    def addPageCard(self, pageIndex, qimage):
        pixmap = QPixmap.fromImage(qimage)

        # create page cards
        card = PageCard(pageIndex, pixmap)

        card.clicked.connect(self.togglePageSelection)

        self.pages.append(card)

        # otimization: if the col dont change only add a card in a correct pos
        if self.currentCollumns > 0:
            index = len(self.pages) - 1
            row = index // self.currentCollumns
            col = index % self.currentCollumns
            self.pageLayout.addWidget(card, row, col)
        else:
            self.updateCurrentGrid()

    def togglePageSelection(self, pageIndex):
        # ignore click if the current screen is extract all
        if self.settingStack.currentIndex() == 0:
            return
        
        # find clicked page card
        for page in self.pages:
            if page.pageIndex == pageIndex:

                # deselect page
                if pageIndex in self.selectedPages:
                    self.selectedPages.remove(pageIndex)
                    page.setSelected(False, 'extract')

                # select page
                else:
                    self.selectedPages.add(pageIndex)
                    page.setSelected(True, 'extract')

                break

        self.updatePageInput()
        self.updateInfoText()
        self.setCanExtract()

    def selectAllPages(self):
        # clear previous selection
        self.selectedPages.clear()

        # select every page
        for page in self.pages:
            page.setSelected(True, 'extract')
            self.selectedPages.add(page.pageIndex)

        self.updatePageInput()
        self.updateInfoText()
        self.setCanExtract()

    def deselectAllPages(self):
        # clear previous selection
        self.selectedPages.clear()
        
        # deselect every page
        for page in self.pages:
            page.setSelected(False, 'extract')

        self.updatePageInput()
        self.updateInfoText()
        self.setCanExtract()

    def updatePageInput(self):
        # clear input if nothing selected
        if not self.selectedPages:
            self.pageInput.clear()
            return
        
        # sort selected pages
        selected = sorted(self.selectedPages)

        finalText = ''
        start = selected[0]
        end = selected[0]
        result = []
        for i in range(1, len(selected)):
            current = selected[i]

            if current == end + 1:
                end = current
            else:
                if start == end:
                    result.append(str(start+1))
                else:
                    result.append(f'{start+1}-{end+1}')
            
                start = current
                end = current

        # add final range
        if start == end:
            result.append(f'{start+1}')
        else:
            result.append(f'{start+1}-{end+1}')

        # create final text
        finalText = ','.join(result)

        
        self.pageInput.setText(finalText)

    def enableSelectMode(self):
        # deselect all pages initially 
        self.deselectAllPages()
        
        # switch to select pages
        self.settingStack.setCurrentIndex(1)

        # refresh card selection
        for card in self.pages:
            card.setSelected(card.pageIndex in self.selectedPages, 'delete')

    def selectPages(self, text):
        # if input is empty deselect every thing
        if not text.strip():
            self.selectedPages.clear()

            self.deselectAllPages()
            return
        
        newSelect = set()
        try:
            textList = text.split(',')
            for elem in textList:
                elem = elem.strip()
                if '-' in elem:
                    start, end = elem.split('-')

                    for i in range(int(start), int(end)+1):
                        newSelect.add(i-1)

                else:
                    newSelect.add(int(elem)-1)
        # ignore invalid input
        except:
            return
        
        # calcule selection changes
        toSelect = newSelect-self.selectedPages
        toDeselect = self.selectedPages-newSelect

        # save new selection
        self.selectedPages = newSelect
        
        for card in self.pages:
            if card.pageIndex in toSelect:
                card.setSelected(True, 'extract')
            elif card.pageIndex in toDeselect:
                card.setSelected(False, 'extract')

        # update info text
        self.updateInfoText()
        self.setCanExtract()

    def updateCurrentGrid(self, force=False):
        # igonore if the pages exist
        if not self.pages:
            return
        
        # get visible width of scroll area
        width = self.filePageFrame.viewport().width()
        cardWidth = 170

        collunms = max(1, width // cardWidth)

        # skip rebuild if colluns dont change
        if collunms == self.currentCollumns and not force:
            return
        
        self.currentCollumns = collunms

        # disable repaint update temporally
        self.pagesFrame.setUpdatesEnabled(False)

        # remove all widgets from layout
        while self.pageLayout.count():
            item = self.pageLayout.takeAt(0)

        # reinsert card in positions
        for index, card in enumerate(self.pages):
            row = index // collunms
            col = index % collunms
            self.pageLayout.addWidget(card, row, col)

        # re-enable repaint
        self.pagesFrame.setUpdatesEnabled(True)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        # add delay grid
        self.resizeTimer.start(100)

    def clearPages(self):
        for page in self.pages:
            # remove all widget
            self.pageLayout.removeWidget(page)
            page.deleteLater()
        
        # clear intenal page list
        self.pages.clear()

    def reoderCards(self, index, newIndex):
        oldIndex = -1

        # find the draged card
        for i, card in enumerate(self.pages):
            if card.pageIndex == index:
                oldIndex = i
                break

        # ignore invalid or identical index
        if oldIndex == newIndex or oldIndex == -1:
            return
        
        # move the card in list
        reoderPage = self.pages.pop(oldIndex)
        self.pages.insert(newIndex, reoderPage)

        # force the update grid
        self.updateCurrentGrid(force=True)

    def toggleSelectInfo(self, checked):
        if checked:
            self.selectInfoContainer.hide()
        else:
            self.selectInfoContainer.show()
    
    def setCanExtract(self):
        if len(self.selectedPages) == 0:
            self.extractBtn.setCursor(Qt.ForbiddenCursor)
            self.extractBtn.setProperty('blocked', True)
            self.canExtractText.show()
        else:
            self.extractBtn.setCursor(Qt.PointingHandCursor)
            self.extractBtn.setProperty('blocked', False)
            self.canExtractText.hide()

        self.extractBtn.style().unpolish(self.extractBtn)
        self.extractBtn.style().polish(self.extractBtn) 


    def updateInfoText(self):
        total = len(self.selectedPages)

        self.selectPageInfoText.setText(
            f'ℹ️ Selected pages will be converted to separated PDF files. '
            f'<b>{total} PDFs</b> will be created.'
        )

        self.allPagesInfoText.setText(
            f'ℹ️ Selected pages will be converted to separated PDF files. '
            f'<b>{total} PDFs</b> will be created.'
        )

    def extractPages(self):

        if self.extractToOne.isChecked():
            # get where the filepath will be saved 
            output, _ = QFileDialog.getSaveFileName(
                self,
                "Salvar PDF Mesclado",
                "extract.pdf",
                "PDF Files (*.pdf)"
            )

            if not output:
                return
        else:
            output = QFileDialog.getExistingDirectory(
                self,
                'Choose folder'
            )

        # set blur effect
        self.mainBlur = QGraphicsBlurEffect()
        self.mainBlur.setBlurRadius(8)
        self.mainSide.setGraphicsEffect(self.mainBlur)

        self.settingBlur = QGraphicsBlurEffect()
        self.settingBlur.setBlurRadius(8)
        self.settingSide.setGraphicsEffect(self.settingBlur)

        self.loading.showOverlay('Extract Pages...', mode='progress')
        self.worker = ExtractWorker(
            file=self.filepath, 
            selectedPages=self.selectedPages, 
            reoderPages=self.pages,
            output=output, 
            mode=self.extractToOne.isChecked()
        )

        self.worker.progress.connect(
            self.loading.updateProgress
        )

        self.worker.finished.connect(
            self.finishExtract
        )

        self.worker.start()

    def finishExtract(self):
            # remove blur effect
        self.mainSide.setGraphicsEffect(None)
        self.settingSide.setGraphicsEffect(None)

        self.loading.progressBar.setValue(0)

        self.loading.hideOverlay()

        self.resetScreen()

        self.innerStack.setCurrentIndex(2)

    def handleGoHome(self):
        self.returnToHome.emit()
