from PySide6.QtCore import QThread, Signal
import pypdf


class DeleteWorker(QThread):
    progress = Signal(int)
    finished = Signal()

    def __init__(self, file, selectedPages, reorderedPages, output):
        super().__init__()
        self.file = file
        self.pages = reorderedPages
        self.selectedPages = selectedPages
        self.output = output

    def run(self):
        total = len(self.selectedPages)
        
        if not total:
            self.finished.emit()
            return

        reader = pypdf.PdfReader(self.file)
        writer = pypdf.PdfWriter()

        for index, _ in enumerate(self.pages):
            try:
                if index not in self.selectedPages:
                    writer.add_page(reader.pages[index])
            except Exception as e:
                print(e)
                
            percent = int(((index + 1) / total) * 90)

            self.progress.emit(percent)

        self.progress.emit(95)
        with open(self.output, 'wb') as output:
            writer.write(output)

        self.progress.emit(100)

        self.finished.emit()
