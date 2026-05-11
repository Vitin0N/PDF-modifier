from PySide6.QtCore import QThread, Signal
import time
import pypdf
import os

MAX_SIZE_MERGED_FILE_GB = 1.5
MAX_MERGED_FILE_PAGES = 3000

class MergeWorker(QThread):
    progress = Signal(int)
    finished = Signal()

    def __init__(self, files, outputPath):
        super().__init__()
        self.files = files
        self.outputPath = outputPath

        self.currentBytesSize = 0
        self.currentPages = 0

        self.currentBytesExceedAccept = False
        self.currentPagesExceedAccept = False
        self.canMerge = True

    def getTotalFileSize(self):
         gbSize = self.currentBytesSize / (pow(1024, 3)) # convert to gigabytes 

         if gbSize > MAX_SIZE_MERGED_FILE_GB:
              self.canMerge = False

    def getTotalPages(self):
         if self.currentPages > MAX_MERGED_FILE_PAGES:
              self.canMerge = False
         

    def run(self):
        total = len(self.files)
        writer = pypdf.PdfWriter()

        try:
            for index, file in enumerate(self.files):

                readFile = pypdf.PdfReader(file)
                self.currentBytesSize += os.path.getsize(file)
                self.currentPages += len(readFile.pages)

                if not (self.currentBytesExceedAccept and self.currentPagesExceedAccept):
                     self.getTotalFileSize()
                     self.getTotalPages()

                     if not self.canMerge:
                          # TODO Start a conversation saying that it's over and ask if the person wants to continue.
                          print('passou nas paginas ou no tamanho')
                          return

                writer.append(readFile)
                percent = int(((index + 1) / total) * 80)
                self.progress.emit(percent) 

            self.progress.emit(85)
            
            with open(self.outputPath, 'wb') as output:
                writer.write(output)
            
            self.progress.emit(100)
        
        except Exception as e:
                print("deu erro no arquivo: ", e)

        print(f'Total pages: {self.currentPages}\nTotal MB merged file: {self.currentBytesSize / pow(1024, 2)}\n')

        self.finished.emit()