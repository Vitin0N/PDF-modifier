from PySide6.QtCore import QThread, Signal
import time

class ExtractWorker(QThread):
    progress = Signal(int)
    finished = Signal()

    def __init__(self, file, pages):
        super().__init__()
        self.file = file
        self.pages = pages

    def run(self):
        total = len(self.pages)

        for index, file in enumerate(self.pages):
            # simula processamento
            time.sleep(1)

            percent = int(((index + 1) / total) * 100)

            self.progress.emit(percent)

        self.finished.emit()