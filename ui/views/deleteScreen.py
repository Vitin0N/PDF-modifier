from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget, QFrame, QHBoxLayout,
    QGridLayout, QScrollArea, QGraphicsBlurEffect, QLineEdit,QFileDialog   
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont, QPixmap

from components._chooseFileScreen import ChooseFileWidget
from ui.widgets.loadingDialog import LoadingDialog
from ui.layouts.dropPageGridFrame import DrogGridFrame
from ui.widgets.pageCard import PageCard
from core.worker.thumbWorker import ThumbWorker
from core.worker.deleteWorker import DeleteWorker


class DeleteScreen(QWidget):
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
            'Delete Pages from PDF',
            'Select and remove the PDF pages you don\'t need. And get a new file without the deleted pages.'
        )

        self.selectFileStep.fileSelected.connect(self.continueToeleteScreen)

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

        # text style for delete button
        deleteBtnFont = QFont()
        deleteBtnFont.setPixelSize(30)
        deleteBtnFont.setBold(True)

        candeleteFont = QFont()
        candeleteFont.setBold(True)
        candeleteFont.setPixelSize(13)

        self.candeleteText = QLabel('You can only delete if there is more than one page selected file.')
        self.candeleteText.setFont(candeleteFont)
        self.candeleteText.setAlignment(Qt.AlignCenter)
        self.candeleteText.setWordWrap(True)
        self.candeleteText.hide()

        self.deleteBtn = QPushButton("Delete Pages")
        self.deleteBtn.setFont(deleteBtnFont)
        self.deleteBtn.setStyleSheet('''
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
        self.deleteBtn.setMinimumHeight(60)
        self.deleteBtn.clicked.connect(self.deletePages)

        nameFont = QFont()
        nameFont.setPixelSize(30)
        nameFont.setBold(True)

        name = QLabel('Delete Pages') 
        name.setFont(nameFont)
        name.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        # option info text
        # ==== select pages box information =====
        selectPageInfo = QWidget()
        selectPageLayout = QVBoxLayout(selectPageInfo)

        selectPageText = QLabel('delete Mode:')
        selectPageText.setWordWrap(True)

        # input for the selected pages
        self.pageInput = QLineEdit()
        self.pageInput.setPlaceholderText('Example: 1-5,8-10')
        self.pageInput.setMinimumHeight(35)

        self.pageInput.textChanged.connect(self.selectPages)

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

        selectPageLayout.addWidget(selectPageText)
        selectPageLayout.addWidget(self.pageInput)
        selectPageLayout.addSpacing(10)
        selectPageLayout.addWidget(self.selectInfoContainer)
        selectPageLayout.addStretch()

        # add elements in setting layout
        settingLayout.addWidget(name)
        settingLayout.addSpacing(10)
        settingLayout.addWidget(line)
        settingLayout.addWidget(selectPageInfo)
        settingLayout.addStretch()
        settingLayout.addWidget(self.candeleteText)
        settingLayout.addWidget(self.deleteBtn)
        settingLayout.addSpacing(20)

        # add the main and setting canva
        mainSettingLayout.addWidget(self.mainSide, 2)
        mainSettingLayout.addWidget(self.settingSide, 1)

        # add screen to stack
        self.innerStack.addWidget(self.selectFileStep)
        self.innerStack.addWidget(self.settingStep)

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

    def continueToeleteScreen(self, filepath):
        # show loading overlay
        self.loading.showOverlay('', mode='spin')

        # switch to delete screen
        self.innerStack.setCurrentIndex(1)

        # call the load delete screen
        QTimer.singleShot(
            0,
            lambda: self.loaddeleteScreen(filepath)
        )

    def loaddeleteScreen(self, filepath):
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

        self.thumbWorker.start()

    def resetScreen(self):
        # reset all file data
        self.selectFile = ''
        self.filepath = ''
        self.selectedPages.clear()
        self.updateInfoText()
        self.clearPages()
        self.updatePageInput()

        # reset thumbWorker
        if hasattr(self, 'thumbWorker'):
            self.thumbWorker = None

        # restore default UI
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
        # find clicked page card
        for page in self.pages:
            if page.pageIndex == pageIndex:

                # deselect page
                if pageIndex in self.selectedPages:
                    self.selectedPages.remove(pageIndex)
                    page.setSelected(False, 'delete')

                # select page
                else:
                    self.selectedPages.add(pageIndex)
                    page.setSelected(True, 'delete')

                break

        self.updatePageInput()
        self.updateInfoText()
        self.setCanDelete()

    def deselectAllPages(self):
        # clear previous selection
        self.selectedPages.clear()
        
        # deselect every page
        for page in self.pages:
            page.setSelected(False, 'delete')

        self.updatePageInput()
        self.updateInfoText()
        self.setCanDelete()

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
                card.setSelected(True, 'delete')
            elif card.pageIndex in toDeselect:
                card.setSelected(False, 'delete')

        # update info text
        self.updateInfoText()
        self.setCanDelete()


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
    
    def setCanDelete(self):
        if len(self.selectedPages) == 0:
            self.deleteBtn.setCursor(Qt.ForbiddenCursor)
            self.deleteBtn.setProperty('blocked', True)
            self.candeleteText.show()
        else:
            self.deleteBtn.setCursor(Qt.PointingHandCursor)
            self.deleteBtn.setProperty('blocked', False)
            self.candeleteText.hide()

        self.deleteBtn.style().unpolish(self.deleteBtn)
        self.deleteBtn.style().polish(self.deleteBtn) 

    def updateInfoText(self):
        total = len(self.selectedPages)

        self.selectPageInfoText.setText(
            f'ℹ️ Selected pages will be converted to separated PDF files. '
            f'<b>{total} PDFs</b> will be created.'
        )

    def deletePages(self):
        output, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar PDF Mesclado",
            "deleted.pdf",
            "PDF Files (*.pdf)"
        )

        if not output:
            return

        # set blur effect
        self.mainBlur = QGraphicsBlurEffect()
        self.mainBlur.setBlurRadius(8)
        self.mainSide.setGraphicsEffect(self.mainBlur)

        self.settingBlur = QGraphicsBlurEffect()
        self.settingBlur.setBlurRadius(8)
        self.settingSide.setGraphicsEffect(self.settingBlur)
        
        self.loading.showOverlay('Delete Pages...', mode='progress')
        self.worker = DeleteWorker(
            file=self.filepath, 
            selectedPages=self.selectedPages,
            reorderedPages=self.pages,
            output=output
        )

        self.worker.progress.connect(
            self.loading.updateProgress
        )

        self.worker.finished.connect(
            self.finishdelete
        )

        self.worker.start()

    def finishdelete(self):
            # remove blur effect
        self.mainSide.setGraphicsEffect(None)
        self.settingSide.setGraphicsEffect(None)

        self.loading.progressBar.setValue(0)

        self.loading.hideOverlay()

        self.resetScreen()