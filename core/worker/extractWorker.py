from PySide6.QtCore import QThread, Signal
import pypdf
from pathlib import Path


class ExtractWorker(QThread):
    progress = Signal(int)
    finished = Signal()

    def __init__(self, file, pages, output, mode):
        super().__init__()
        self.file = file
        self.pages = pages
        self.output = output
        self.modeExtractToOne = mode

    def run(self):
        total = len(self.pages)
        
        if not total:
            self.finished.emit()
            return

        reader = pypdf.PdfReader(self.file)

        if self.modeExtractToOne:
            writer = pypdf.PdfWriter()
            for index, pageIndex in enumerate(self.pages):
                try:
                    writer.add_page(reader.pages[pageIndex])
                except Exception as e:
                    print(e)
                    
                percent = int(((index + 1) / total) * 90)

                self.progress.emit(percent)

            self.progress.emit(95)
            with open(self.output, 'wb') as output:
                writer.write(output)

        else:
            originalPath = Path(self.file)

            folder = Path(self.output)

            basename = originalPath.stem

            for index, pageIndex in enumerate(self.pages):
                writer = pypdf.PdfWriter()
                writer.add_page(reader.pages[pageIndex])
                try:
                    newFilename = folder / f'{basename}_{pageIndex+1}.pdf'
                    with open(newFilename, 'wb') as output:
                        writer.write(output)

                    percent = int(((index + 1) / total) * 95)

                    self.progress.emit(percent)

                except Exception as e:
                    print(e)


        self.progress.emit(100)

        self.finished.emit()
