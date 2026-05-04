from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)
from PySide6.QtGui import (
    QIcon
)
from PySide6.QtCore import (
    Qt, Signal
)

class HomeView(QWidget):
    mergeClicked = Signal()
    splitClicked = Signal()
    extractClicked = Signal()
    deleteClicked = Signal()

    def __init__(self):
        super().__init__()

        # creating a layout alingn vertically
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        layout.setContentsMargins(0, 0, 0, 0)

        textTitle = QLabel('Welcome to PDF Modifier!')
        textTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        textTitle.setStyleSheet("font-size: 30px;")

        textSub = QLabel("Select a process to continue.")
        textSub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        textSub.setStyleSheet("font-size: 20px;")

        buttonContainer = QWidget()
        buttonLayout = QHBoxLayout(buttonContainer)
        buttonLayout.setSpacing(5)

        # creating process buttons
        mergeBtn = QPushButton("Merge")
        splitBtn = QPushButton("Split")
        extractBtn = QPushButton("Extract")
        deleteBtn = QPushButton("Delete")

        mergeBtn.clicked.connect(self.mergeClicked.emit)
        splitBtn.clicked.connect(self.splitClicked.emit)
        extractBtn.clicked.connect(self.extractClicked.emit)
        deleteBtn.clicked.connect(self.deleteClicked.emit)

        for btn in [mergeBtn, splitBtn, deleteBtn, extractBtn]:
            btn.setStyleSheet("padding: 10px; min-width: 80px")

        # add buttons in the button layout
        buttonLayout.addWidget(mergeBtn)
        buttonLayout.addWidget(splitBtn)
        buttonLayout.addWidget(extractBtn)
        buttonLayout.addWidget(deleteBtn)

        layout.addStretch()
        layout.addWidget(textTitle)
        layout.addWidget(textSub)
        layout.addWidget(buttonContainer, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()