"""Node header."""

from PySide import QtGui
from PySide import QtCore

from .helpers import getTextSize


class Header(QtGui.QGraphicsItem):
    """A Header is a child of a Node and gives it a title.

    Its width resizes automatically to match the Node's width.
    """
    def __init__(self, node, text, h=20,
                 fillColor=QtGui.QColor(90, 90, 90),
                 textColor=QtGui.QColor(240, 240, 240)):
        super(Header, self).__init__()
        self.node = node
        self.text = text
        self.h = h
        self.fillColor = fillColor
        self.textColor = textColor

    def boundingRect(self):
        nodebox = self.node.boundingRect()
        rect = QtCore.QRect(self.x(),
                            self.y(),
                            nodebox.width(),
                            self.h)
        return rect

    def paint(self, painter, option, widget):
        # Draw background rectangle.
        bbox = self.boundingRect()

        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        painter.setBrush(self.fillColor)
        painter.drawRoundedRect(bbox,
                                self.node.roundness,
                                self.node.roundness)

        # Draw header label.
        if self.node.isSelected():
            painter.setPen(QtGui.QPen(QtGui.QColor(255, 255, 0)))
        else:
            painter.setPen(QtGui.QPen(self.textColor))

        # # centered text
        # textSize = getTextSize(painter, self.text)
        # painter.drawText(self.x() + (self.node.w - textSize.width()) / 2,
        #                  self.y() + (self.h + textSize.height() / 2) / 2,
        #                  self.text)

        # left aligned text
        textSize = getTextSize(self.text, painter=painter)
        painter.drawText(self.x() + self.node.margin,
                         self.y() + (self.h + textSize.height() / 2) / 2,
                         self.text)

    def destroy(self):
        """Remove this object from the scene and delete it."""
        print("destroy header:", self)
        scene = self.node.scene()
        scene.removeItem(self)
        del self
