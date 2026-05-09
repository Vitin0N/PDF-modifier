from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFrame,
    QSizePolicy,
    QPushButton,
    QHBoxLayout,
    QApplication
)
from PySide6.QtGui import QFont, QDrag, QPixmap

from PySide6.QtCore import Qt, Signal, QMimeData, QPoint

class FileCards(QFrame):
    removeRequest = Signal(object)
    def __init__(self, filename, filepath):
        super().__init__()

        # var to filepath
        self.filepath = filepath
        # keep the cursor pointing when over the card
        self.setCursor(Qt.PointingHandCursor)

        # fix the size of the card
        self.setSizePolicy(
            QSizePolicy.Fixed,
            QSizePolicy.Fixed
        )

        # card format
        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedSize(140, 140)
        
        self.setStyleSheet('''
            QFrame {
                border-radius: 10px;
            }

            QFrame:hover {
                background-color: #e5322d;  
            }
        ''')

        # card layout
        cardLayout = QVBoxLayout(self)

        # file icon
        icon = QLabel('📄')

        # size of icon
        iconFont = QFont()
        iconFont.setPixelSize(60)
        icon.setFont(iconFont)

        icon.setAlignment(Qt.AlignCenter)

        # file name
        name = QLabel(filename)
        name.setAlignment(Qt.AlignCenter)

        # set the background color transparent on hover
        icon.setAttribute(Qt.WA_TransparentForMouseEvents)
        name.setAttribute(Qt.WA_TransparentForMouseEvents)

        # remove button
        self.removeBtn = QPushButton("✕", self)
        self.removeBtn.setFixedSize(28, 28)
        self.removeBtn.setStyleSheet('''
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 14px;
                font-weight: bold;
            }
                                     
            QPushButton:hover {
                background-color: white;
                color: #e5322d;
            }
        ''')
        self.removeBtn.move(104, 8)
        self.removeBtn.raise_()
        self.removeBtn.hide()

        # add icon and name to layout
        cardLayout.addStretch()
        cardLayout.addWidget(icon)
        cardLayout.addWidget(name)
        cardLayout.addStretch()

        # buttons commands 
        self.removeBtn.clicked.connect(self.handleRemove)

    # events functions
    def enterEvent(self, event):
        self.removeBtn.show()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.removeBtn.hide()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragStartPos = event.pos()
        
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        
        if (event.pos() - self.dragStartPos).manhattanLength() < QApplication.startDragDistance():
            return
        
        drag = QDrag(self)
        mimeData = QMimeData()

        mimeData.setText(self.filepath)
        drag.setMimeData(mimeData)

        pixmap = self.grab()
        smallerPixmap = pixmap.scaled(
            130, 130,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )

        drag.setPixmap(smallerPixmap)
        drag.setHotSpot(event.pos())

        drag.exec()


    # Command functions
    def handleRemove(self):
        self.removeRequest.emit(self)