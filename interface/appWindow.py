from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget, QLabel
)

from views.homeScreen import HomeView

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PDF Modifier')
        self.resize(800, 600)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        mainLayout = QHBoxLayout(centralWidget)

        self.sidebar = QWidget()    
        self.sidebar.setFixedWidth(200)

        menuLayout = QVBoxLayout(self.sidebar)
        menuLayout.setContentsMargins(0, 10, 0, 0)

        self.homeBtn = QPushButton('Home')
        self.mergeBtn = QPushButton('Merge PDFs')
        self.extractBtn = QPushButton('Extract Pages')

        menuLayout.addWidget(self.homeBtn)
        menuLayout.addSpacing(50)
        menuLayout.addWidget(self.mergeBtn)
        menuLayout.addWidget(self.extractBtn)
        menuLayout.addStretch()

        self.stackWidget = QStackedWidget()

        self.homeScreen = HomeView()
        self.mergeScreen = QWidget()

        self.stackWidget.addWidget(self.homeScreen)
        self.stackWidget.addWidget(self.mergeScreen)

        mainLayout.addWidget(self.sidebar)
        mainLayout.addWidget(self.stackWidget)

        self.homeBtn.clicked.connect(self.showHomeScreen)
        self.mergeBtn.clicked.connect(self.showMergeScreen)
        self.extractBtn.clicked.connect(self.showExtractScreen)

        self.homeScreen.mergeClicked.connect(self.showMergeScreen)
        self.homeScreen.extractClicked.connect(self.showExtractScreen)

    def showHomeScreen(self):
        print('home screen')
        self.stackWidget.setCurrentIndex(0)

    def showMergeScreen(self):
        print('merge srcreen')
        self.stackWidget.setCurrentIndex(1)
    
    def showExtractScreen(self):
        print("Extract Screen")
