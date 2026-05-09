from PySide6.QtWidgets import (
    QFrame,
)
from PySide6.QtCore import Signal

class DrogGridFrame(QFrame):
    # sinal that analyses which file were moved and their positions
    reordered = Signal(str, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        filepath = event.mimeData().text()
        pos = event.position().toPoint()

        newIndex = -1
        for i in range(self.layout().count()):
            widget = self.layout().itemAt(i).widget()
            
            # check if the position is within a card
            if widget.geometry().contains(pos):
                newIndex = i
                break

        # if the index change, we change the card's index
        if newIndex != -1:
            self.reordered.emit(filepath, newIndex)
            event.acceptProposedAction()