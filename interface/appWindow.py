from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QPushButton, QStackedWidget
)

from ui.views.homeScreen import HomeView
from ui.views.mergeScreen import MergeScreen
from ui.views.extractScreen import ExtractScreen
from ui.views.deleteScreen import DeleteScreen

class AppWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.sidebarCompress = False

        self.setWindowTitle('PDF Modifier')
        self.resize(800, 600)

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)

        mainLayout = QHBoxLayout(centralWidget)

        # Sidebar configuration
        self.sidebarExpandedWidth = 200
        self.sidebarCollapsedWidth = 90

        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(self.sidebarExpandedWidth)

        menuLayout = QVBoxLayout(self.sidebar)
        menuLayout.setContentsMargins(5, 10, 5, 10)

        # ===== Top bar in menu Layout =====
        topLayout = QHBoxLayout()
        topLayout.addStretch()

        self.compressSidebarBtn = QPushButton("⇚")
        self.compressSidebarBtn.setFixedSize(32, 32)

        self.compressSidebarBtn.setStyleSheet("""
            QPushButton {
                background-color: #e5322d;
                color: white;
                border: none;
                border-radius: 16px;
                font-size: 16px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #C42B27;
            }
        """)
        self.compressSidebarBtn.clicked.connect(self.compressSideBar)

        topLayout.addWidget(self.compressSidebarBtn)


        # ===== Route buttons =====
        self.homeBtn = QPushButton()
        self.mergeBtn = QPushButton()
        # self.splitBtn = QPushButton()
        self.extractBtn = QPushButton()
        self.deleteBtn = QPushButton()

        self.setRoutesBtnText()

        menuLayout.addLayout(topLayout)
        menuLayout.addSpacing(20)
        menuLayout.addWidget(self.homeBtn)
        menuLayout.addSpacing(50)
        menuLayout.addWidget(self.mergeBtn)
        # menuLayout.addWidget(self.splitBtn)
        menuLayout.addWidget(self.extractBtn)
        menuLayout.addWidget(self.deleteBtn)
        menuLayout.addStretch()

        # Add stack with the all screens
        self.stackWidget = QStackedWidget()

        # Screens of the processes
        self.homeScreen = HomeView()
        self.mergeScreen = MergeScreen()
        self.extractScreen = ExtractScreen()
        self.deleteScreen = DeleteScreen()

        # Add screens to the stack
        self.stackWidget.addWidget(self.homeScreen)
        self.stackWidget.addWidget(self.mergeScreen)
        self.stackWidget.addWidget(self.extractScreen)
        self.stackWidget.addWidget(self.deleteScreen)

        mainLayout.addWidget(self.sidebar)
        mainLayout.addWidget(self.stackWidget)

        # Listener to all buttons
        self.homeBtn.clicked.connect(self.showHomeScreen)
        self.mergeBtn.clicked.connect(self.showMergeScreen)
        self.extractBtn.clicked.connect(self.showExtractScreen)
        self.deleteBtn.clicked.connect(self.showDeleteScreen)

        # Homescreen buttons listeners
        self.homeScreen.mergeClicked.connect(self.showMergeScreen)
        self.homeScreen.extractClicked.connect(self.showExtractScreen)
        self.homeScreen.deleteClicked.connect(self.showDeleteScreen)

        # Merge Screen buttons listeners
        self.mergeScreen.returnToHome.connect(self.showHomeScreen)
        self.extractScreen.returnToHome.connect(self.showHomeScreen)
        self.deleteScreen.returnToHome.connect(self.showHomeScreen)

    # ==== Buttons Functions ====
    def showHomeScreen(self):
        self.sidebar.setMinimumWidth(200)
        self.sidebar.setMaximumWidth(200)

        self.stackWidget.setCurrentIndex(0)

    def showMergeScreen(self):
        self.mergeScreen.resetScreen()
        self.compressSideBar(forceCompress=True)

        
        self.stackWidget.setCurrentIndex(1)
    
    def showExtractScreen(self):
        self.extractScreen.resetScreen()
        self.compressSideBar(forceCompress=True)

        self.stackWidget.setCurrentIndex(2)

    def showDeleteScreen(self):
        self.deleteScreen.resetScreen()

        self.stackWidget.setCurrentIndex(3)


    def compressSideBar(self, forceCompress=False):

        if self.sidebarCompress and not forceCompress:
            self.sidebarCompress = False
            self.setRoutesBtnText()

            self.sidebar.setFixedWidth(self.sidebarExpandedWidth)
            self.compressSidebarBtn.setText("⇚")

        elif not self.sidebarCompress:
            self.sidebarCompress = True
            self.setRoutesBtnText()

            self.sidebar.setFixedWidth(self.sidebarCollapsedWidth)
            self.compressSidebarBtn.setText("⇛")

    def setRoutesBtnText(self):
        if not self.sidebarCompress:
            self.homeBtn.setText('Home')
            self.mergeBtn.setText('Merge PDFs')
            # self.splitBtn.setText('Split PDFs')
            self.extractBtn.setText('Extract Pages')
            self.deleteBtn.setText('Delete Pages')
        else:
            self.homeBtn.setText('Home')
            self.mergeBtn.setText('Merge')
            # self.splitBtn.setText('Split PDFs')
            self.extractBtn.setText('Extract')
            self.deleteBtn.setText('Delete')
        
