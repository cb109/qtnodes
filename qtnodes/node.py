"""Node classes."""

from PySide import QtGui
from PySide import QtCore

from .helpers import getTextSize
from .knob import Knob, InputKnob, OutputKnob


class Node(QtGui.QGraphicsItem):

    def __init__(self, scene=None):
        super(Node, self).__init__(scene=scene)

        self.header = None

        self.x = 0
        self.y = 0
        self.w = 10
        self.h = 10

        self.margin = 6
        self.roundness = 0

        self.fillColor = QtGui.QColor(220, 220, 220)

        # General configuration.
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable)
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)

        self.setCursor(QtCore.Qt.SizeAllCursor)

        self.setAcceptHoverEvents(True)
        self.setAcceptTouchEvents(True)
        self.setAcceptDrops(True)

    def knob(self, name):
        """Return matching Knob by name, None otherwise."""
        for child in self.childItems():
            if isinstance(child, Knob):
                if child.labelText == name:
                    return child
        return None

    def boundingRect(self):
        rect = QtCore.QRect(self.x,
                            self.y,
                            self.w,
                            self.header.h)
        return rect

    def updateSizeForChildren(self):
        """Adjust width and height as needed for header and knobs."""

        def adjustHeight():
            """Adjust height to fit header and all knobs."""
            knobs = [c for c in self.childItems() if isinstance(c, Knob)]
            knobsHeight = sum([k.h + self.margin for k in knobs])
            heightNeeded = self.header.h + knobsHeight + self.margin
            self.h = heightNeeded

        def adjustWidth():
            """Adjust width as needed for the widest child item."""
            headerWidth = (self.margin + getTextSize(self.header.text).width())

            knobs = [c for c in self.childItems() if isinstance(c, Knob)]
            knobWidths = [k.w + self.margin + getTextSize(k.labelText).width()
                          for k in knobs]
            maxWidth = max([headerWidth] + knobWidths)
            self.w = maxWidth + self.margin

        adjustWidth()
        adjustHeight()

    def addHeader(self, header):
        self.header = header
        header.setPos(self.pos())
        header.setParentItem(self)
        self.updateSizeForChildren()

    def addKnob(self, knob):
        children = [c for c in self.childItems()]
        yOffset = sum([c.h + self.margin for c in children])
        xOffset = self.margin / 2

        knob.setParentItem(self)
        knob.margin = self.margin
        self.updateSizeForChildren()

        bbox = self.boundingRect()
        if isinstance(knob, OutputKnob):
            knob.setPos(bbox.right() - knob.w + xOffset, yOffset)
        elif isinstance(knob, InputKnob):
            knob.setPos(bbox.left() - xOffset, yOffset)

    def paint(self, painter, option, widget):
        painter.setBrush(QtGui.QBrush(self.fillColor))
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))

        # The bounding box is only as high as the header (we do this
        # to limit the area that is move-enabled). Acommodate for that.
        bbox = self.boundingRect()
        painter.drawRoundedRect(self.x,
                                self.y,
                                bbox.width(),
                                self.h,
                                self.roundness,
                                self.roundness)

    # def sceneEvent(self, event):
    #     print("sceneEvent()", event.type(), event)
    #     super(Node, self).sceneEvent(event)

    # def sceneEventFilter(self, watched, event):
    #     print("sceneEventFilter()", watched, event.type(), event)
    #     super(Node, self).sceneEventFilter(watched, event)

    # def contextMenuEvent(self, event):
    #     print("contextMenuEvent()", event.type(), event)
    #     super(Node, self).contextMenuEvent(event)

    # def focusInEvent(self, event):
    #     print("focusInEvent()", event.type(), event)
    #     super(Node, self).focusInEvent(event)

    # def focusOutEvent(self, event):
    #     print("focusOutEvent()", event.type(), event)
    #     super(Node, self).focusOutEvent(event)

    # def hoverEnterEvent(self, event):
    #     print("hoverEnterEvent()", event.type(), event)
    #     super(Node, self).hoverEnterEvent(event)

    # def hoverMoveEvent(self, event):
    #     print("hoverMoveEvent()", event.type(), event)
    #     super(Node, self).hoverMoveEvent(event)

    # def hoverLeaveEvent(self, event):
    #     print("hoverLeaveEvent()", event.type(), event)
    #     super(Node, self).hoverLeaveEvent(event)

    # def inputMethodEvent(self, event):
    #     print("inputMethodEvent()", event.type(), event)
    #     super(Node, self).inputMethodEvent(event)

    # def keyPressEvent(self, event):
    #     print("keyPressEvent()", event.type(), event)
    #     super(Node, self).keyPressEvent(event)

    # def keyReleaseEvent(self, event):
    #     print("keyReleaseEvent()", event.type(), event)
    #     super(Node, self).keyReleaseEvent(event)

    # def mousePressEvent(self, event):
    #     print("mousePressEvent()", event.type(), event)
    #     super(Node, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Update selected item's (and children's) positions as needed.

        We cannot just update our own childItems, since we are using
        RubberBandDrag, and that woudl lead to otherwise e.g. Edges
        visually lose their connection until an attached Node is moved
        individually.
        """
        items = self.scene().selectedItems()
        for item in items:
            knobs = [c for c in item.childItems() if isinstance(c, Knob)]
            for knob in knobs:
                for edge in knob.edges:
                    edge.updatePath()
        super(Node, self).mouseMoveEvent(event)

    # def mouseReleaseEvent(self, event):
    #     print("mouseReleaseEvent()", event.type(), event)
    #     super(Node, self).mouseReleaseEvent(event)

    # def mouseDoubleClickEvent(self, event):
    #     print("mouseDoubleClickEvent()", event.type(), event)
    #     super(Node, self).mouseDoubleClickEvent(event)

    # def wheelEvent(self, event):
    #     print("wheelEvent()", event.type(), event)
    #     super(Node, self).wheelEvent(event)

    # def dragEnterEvent(self, event):
    #     print("dragEnterEvent()", event.type(), event)
    #     super(Node, self).dragEnterEvent(event)

    # def dragMoveEvent(self, event):
    #     print("dragMoveEvent()", event.type(), event)
    #     super(Node, self).dragMoveEvent(event)

    # def dragLeaveEvent(self, event):
    #     print("dragLeaveEvent()", event.type(), event)
    #     super(Node, self).dragLeaveEvent(event)

    # def dropEvent(self, event):
    #     print("dropEvent()", event.type(), event)
    #     super(Node, self).dropEvent(event)
