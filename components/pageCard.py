from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel, QSizePolicy
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, Signal
import fitz  # Importando o PyMuPDF

class PageCard(QFrame):
    clicked = Signal()

    def __init__(self, filepath, pageIndex):
        super().__init__()

        self.filepath = filepath
        self.pageIndex = pageIndex

        self.setCursor(Qt.PointingHandCursor)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.setFrameShape(QFrame.StyledPanel)
        self.setFixedSize(140, 180)

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
        layout.contentsMargins(5, 5, 5, 5)

        # the page image
        self.imgLabel = QLabel()
        self.imgLabel.setAlignment(Qt.AlignCenter)

        # the page index
        self.pageLabel = QLabel(f'{pageIndex + 1}')
        self.pageLabel.setAlignment(Qt.AlignCenter)
        self.pageLabel.setStyleSheet("borde: none; color: #333; font-weight: bold;")

        layout.addWidget(self.imgLabel)
        layout.addWidget(self.pageLabel)

        # call the thumbnail page function
        self.loadThumb()

    def loadThumb(self):
        try:
            doc = fitz.open(self.filepath)

            page = doc.load_page(self.pageIndex)

            # render the page at a lower resolution
            zoomMatriz = fitz.Matrix(0.4, 0.4)

            pix = page.get_pixmap(matrix=zoomMatriz)

            img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)

            pixmap = QPixmap.fromImage(img)
            pixmapResized = pixmap.scaled(120, 140, Qt.KeepAspectRatio, Qt.SmoothTransformation)

            self.imgLabel.setPixmap(pixmapResized)

            doc.close()
        except Exception as e:
            print(f'Error: The thumbnail could not be loaded {e}')
            self.imglabel.setText('Error: Diplay\nError')

    def mousePressEvent(self, event):
        if event.button() == Qt.leftButton:
            self.clicked.emit(self.pageIndex)
        super().mousePressEvent(event)