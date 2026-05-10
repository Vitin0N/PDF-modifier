from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QProgressBar
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QMovie

from core.currentPath import resourcePath

class LoadingDialog(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAttribute(Qt.WA_StyledBackground, True)

        # make the screen dark and transparent
        self.setStyleSheet('''
            background-color: rgba(0, 0, 0, 160)
        ''')

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setAlignment(Qt.AlignCenter)

        self.title = QLabel()
        self.title.setAlignment(Qt.AlignCenter)

        self.title.setStyleSheet('''
            color: white;
            font-size: 24px;
            font-weight: bold;
            background: transparent;
        ''')

        self.spinner = QLabel()
        self.spinner.setAlignment(Qt.AlignCenter)
        self.spinner.setStyleSheet('background-color: transparent;')

        spinFilepath = resourcePath('assets/spinner.gif')
        self.movie = QMovie(spinFilepath)
        self.movie.setScaledSize(QSize(40, 40))
        self.spinner.setMovie(self.movie)

        self.progressBar = QProgressBar()
        self.progressBar.setFixedWidth(300)

        self.mainLayout.addWidget(self.title)
        self.mainLayout.addSpacing(20)
        self.mainLayout.addWidget(self.spinner)
        self.mainLayout.addWidget(self.progressBar)

        self.hide()

    def showOverlay(self, title='Loading...', mode='spin'):
        self.title.setText(title)

        self.spinner.hide()
        self.progressBar.hide()

        if mode == 'spin':
            self.spinner.show()
            self.movie.start()

        elif mode == 'progress':
            self.progressBar.show()

        self.resize(self.parent().size())

        self.raise_()
        self.show()

    def hideOverlay(self):
        self.movie.stop()
        self.hide()


    def updateProgress(self, value):
        self.progressBar.setValue(value)