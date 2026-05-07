from PySide6.QtWidgets import QFileDialog

def chooseFile(parent, mode='single'):

    if mode == 'single':
        filename, _ = QFileDialog.getOpenFileName(
            parent,
            'Choose a PDF file',    # Window title
            '',                     # Home directory (NULL)
            'PDF Files (*.pdf)'     # filter of PDFs files
        )
    
    elif mode == 'multiple':
        filename, _ = QFileDialog.getOpenFileNames(
            parent,
            'Choose a PDF file',    # Window title
            '',                     # Home directory (NULL)
            'PDF Files (*.pdf)'     # filter of PDFs files
        )
    
    if filename:
        return filename