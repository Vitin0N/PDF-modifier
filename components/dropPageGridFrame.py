from PySide6.QtWidgets import QFrame
from PySide6.QtCore import Signal
from PySide6.QtGui import QPainter, QPen, QColor

class DrogGridFrame(QFrame):
    # sinal that analyses which file were moved and their positions
    reordered = Signal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

        # indicates the index where the card will be droped
        self.indexIndicator = -1

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dragMoveEvent(self, event):
        if not event.mimeData().hasText():
            return
        
        pos = event.position().toPoint()
        pageIndex = int(event.mimeData().text())
        originalIndex = -1
        newIndex = -1
        count = self.layout().count()

        # search the original index of card
        for i in range(count):
            widget = self.layout().itemAt(i).widget()
            if widget.pageIndex == pageIndex:
                originalIndex = i
                break

        # check if the mouse is over the card
        for i in range(count):
            widget = self.layout().itemAt(i).widget()
            if widget and widget.geometry().contains(pos):
                newIndex = i
                break
        
        if newIndex == -1:
            newIndex = originalIndex

        newIndex = min(newIndex, count)

        if self.indexIndicator != newIndex:
            self.indexIndicator = newIndex
            self.update() # to paintEvent

        event.acceptProposedAction()

    def dragLeaveEvent(self, event):
        self.indexIndicator = -1
        self.update() # delete the line


    def dropEvent(self, event):
        pageIndex = int(event.mimeData().text()
)
        if self.indexIndicator != -1:
            maxIndex = max(0, self.layout().count() - 1)
            finalIndex = min(self.indexIndicator, maxIndex)

            self.reordered.emit(pageIndex, finalIndex)

        self.indexIndicator = -1
        self.update()
        event.acceptProposedAction()

    def paintEvent(self, event):
        super().paintEvent(event)

        if self.indexIndicator >= 0:
            count = self.layout().count()

            painter = QPainter(self)
            pen = QPen(QColor("#e5322d"))

            pen.setWidth(4)
            painter.setPen(pen)

            # draw a top line in the card
            if self.indexIndicator < count:
                widget = self.layout().itemAt(self.indexIndicator).widget() 
                rect = widget.geometry()
                painter.drawLine(rect.topLeft(), rect.topRight())

            painter.end()