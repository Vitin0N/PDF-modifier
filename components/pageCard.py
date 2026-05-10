from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QSizePolicy, QApplication
from PySide6.QtGui import QDrag, QFont
from PySide6.QtCore import Qt, Signal, QMimeData, QTimer

class PageCard(QFrame):
    clicked = Signal(int)

    def __init__(self, pageIndex, pixmap):
        super().__init__()

        self.pageIndex = pageIndex
        self.selected = False
        self.startPos = None

        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedSize(170, 210)

        self.setStyleSheet('''
            QFrame {
                border-radius: 10px;
                border: none;
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
        self.imgLabel.setStyleSheet('''
            QLabel {
                border: none;
            }
        ''')

        pixmapResized = pixmap.scaled(120, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.imgLabel.setPixmap(pixmapResized)

        # the page index
        indexFont = QFont()
        indexFont.setPixelSize(15)
        indexFont.setBold(True)

        self.pageLabel = QLabel(f'{pageIndex + 1}')
        self.pageLabel.setAlignment(Qt.AlignCenter)
        self.pageLabel.setFont(indexFont)
        self.pageLabel.setStyleSheet('''
            QLabel {
                background-color: #404040;
                border: none;
                max-height: 30px;
            }
        ''')

        self.checkLabel = QLabel('✓', self)
        self.checkLabel.setFixedSize(24, 24)
        self.checkLabel.setAlignment(Qt.AlignCenter)
        self.checkLabel.setStyleSheet('''
            QLabel {
            background-color: #22c55e;
            color: white;
            border-radius: 12px;
            font-weight: bold;
                                      }
        ''')

        self.checkLabel.hide()

        layout.addWidget(self.imgLabel)
        layout.addWidget(self.pageLabel)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPos = event.pos()

            self.clicked.emit(self.pageIndex)

        super().mousePressEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        self.checkLabel.move(
            self.width() - 30,
            6
        )

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        
        if not self.startPos:
            return
        
        distance = (event.pos() - self.startPos).manhattanLength()

        if distance < QApplication.startDragDistance():
            return
        
        drag = QDrag(self)
        mimeData = QMimeData()

        mimeData.setText(str(self.pageIndex))
        drag.setMimeData(mimeData)

        

        drag.setPixmap(self.grab().scaled(
            100,
            120, 
            Qt.KeepAspectRatio,
            Qt.FastTransformation
            )
        )
        drag.setHotSpot(event.pos())
        
        drag.exec()

    def setSelected(self, value):
        self.selected = value
        self.checkLabel.setVisible(value)
        self.updateStyle()

    def updateStyle(self):
        borderColor = '#22c55e' if self.selected else 'transparent'

        self.setStyleSheet(f'''
        QFrame {{
            border-radius: 14px;
            border: 2px solid {borderColor};
        }}

        QLabel {{
            border: none;
            background: transparent;
        }}
    ''')