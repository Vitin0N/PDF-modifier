from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget, QLabel
)

from views.homeScreen import HomeView
from views.mergeScreen import MergeScreen
from views.extractScreen import ExtractScreen

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('PDF Modifier')
        self.resize(800, 600)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        mainLayout = QHBoxLayout(centralWidget)

        # Sidebar configuration
        self.sidebar = QWidget()    
        self.sidebar.setFixedWidth(200)

        menuLayout = QVBoxLayout(self.sidebar)
        menuLayout.setContentsMargins(0, 10, 0, 0)

        # Routes buttons
        self.homeBtn = QPushButton('Home')
        self.mergeBtn = QPushButton('Merge PDFs')
        self.splitBtn = QPushButton('Split PDFs')
        self.extractBtn = QPushButton('Extract Pages')
        self.deleteBtn = QPushButton('Delete Pages')

        menuLayout.addWidget(self.homeBtn)
        menuLayout.addSpacing(50)
        menuLayout.addWidget(self.mergeBtn)
        menuLayout.addWidget(self.splitBtn)
        menuLayout.addWidget(self.extractBtn)
        menuLayout.addWidget(self.deleteBtn)
        menuLayout.addStretch()

        # Add stack with the all screens
        self.stackWidget = QStackedWidget()

        # Screens of the processes
        self.homeScreen = HomeView()
        self.mergeScreen = MergeScreen()
        self.extractScreen = ExtractScreen()

        # Add screens to the stack
        self.stackWidget.addWidget(self.homeScreen)
        self.stackWidget.addWidget(self.mergeScreen)
        self.stackWidget.addWidget(self.extractScreen)

        mainLayout.addWidget(self.sidebar)
        mainLayout.addWidget(self.stackWidget)

        # Listener to all buttons
        self.homeBtn.clicked.connect(self.showHomeScreen)
        self.mergeBtn.clicked.connect(self.showMergeScreen)
        self.extractBtn.clicked.connect(self.showExtractScreen)

        # Homescreen buttons listeners
        self.homeScreen.mergeClicked.connect(self.showMergeScreen)
        self.homeScreen.extractClicked.connect(self.showExtractScreen)

    # ==== Buttons Functions ====
    def showHomeScreen(self):
        print('home screen')
        self.stackWidget.setCurrentIndex(0)

    def showMergeScreen(self):
        print('merge srcreen')
        self.mergeScreen.resetScreen()
        
        self.stackWidget.setCurrentIndex(1)
    
    def showExtractScreen(self):
        print("Extract Screen")
        self.stackWidget.setCurrentIndex(2)
