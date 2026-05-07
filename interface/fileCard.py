from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFrame
)

from PySide6.QtCore import Qt

class FileCards(QFrame):
    def __init__(self, filename):
        super().__init__()

        # card format
        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedSize(140, 140)

        # card layout
        cardLayout = QVBoxLayout(self)

        # file icon
        icon = QLabel('📄')
        icon.setAlignment(Qt.AlignCenter)

        # file name
        name = QLabel(filename)
        name.setAlignment(Qt.AlignCenter)

        # add icon and name to layout
        cardLayout.addStretch()
        cardLayout.addWidget(icon)
        cardLayout.addWidget(name)
        cardLayout.addStretch()