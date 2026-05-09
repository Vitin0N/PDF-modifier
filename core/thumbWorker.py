import fitz
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage

class ThumbWorker(QThread):
    pageRendered = Signal(int, QImage)

    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath

    def run(self):
        try:
            doc = fitz.open(self.filepath)
            totalPages = len(doc)

            for pageIndex in range(totalPages):
                page = doc.load_page(pageIndex)

                zoomMatrix = fitz.Matrix(0.4, 0.4)
                pix = page.get_pixmap(matrix=zoomMatrix)

                img = QImage(pix.samples, pix.width, pix.height, pix.stride, QImage.Format_RGB888)

                self.pageRendered.emit(pageIndex, img)

            doc.close()
        except Exception as e:
            print(f'Error: The thumbnail could not be loaded {e}')