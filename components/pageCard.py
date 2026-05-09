from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QSizePolicy
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, Signal
import fitz  # Importando o PyMuPDF

class PageCard(QFrame):
    clicked = Signal(int)

    def __init__(self, pageIndex, pixmap):
        super().__init__()

        self.pageIndex = pageIndex

        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedSize(170, 210)

        self.setStyleSheet('''
            QFrame {
                border-radius: 10px;
                border: 2px solid #ccc;
            }
            QFrame:hover {
                border: 2px solid #e5322d;
            }
        ''')

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)

        # the page image
        self.imgLabel = QLabel()
        self.imgLabel.setAlignment(Qt.AlignCenter)

        pixmapResized = pixmap.scaled(120, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.imgLabel.setPixmap(pixmapResized)

        # the page index
        self.pageLabel = QLabel(f'{pageIndex + 1}')
        self.pageLabel.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.imgLabel)
        layout.addWidget(self.pageLabel)


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.pageIndex)
        super().mousePressEvent(event)