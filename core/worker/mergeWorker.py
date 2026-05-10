from PySide6.QtCore import QThread, Signal
import time

class MergeWorker(QThread):
    progress = Signal(int)
    finished = Signal()

    def __init__(self, files):
        super().__init__()
        self.files = files

    def run(self):
        total = len(self.files)

        for index, file in enumerate(self.files):
            # simula processamento
            time.sleep(1)

            percent = int(((index + 1) / total) * 100)

            self.progress.emit(percent)

        self.finished.emit()