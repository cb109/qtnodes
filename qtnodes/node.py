"""Node classes."""

import uuid

from PySide import QtGui
from PySide import QtCore

from .helpers import getTextSize
from .knob import Knob, InputKnob, OutputKnob


class Node(QtGui.QGraphicsItem):
    """A Node is a container for a header and 0-n Knobs.

    It can be created, removed and modified by the user in the UI.
    """
    def __init__(self, **kwargs):
        super(Node, self).__init__(**kwargs)

        # This unique id is useful for serialization/reconstruction.
        self.uuid = str(uuid.uuid4())

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

    def knobs(self):
        """Return a list of childItems that are Knob objects."""
        knobs = []
        for child in self.childItems():
            if isinstance(child, Knob):
                knobs.append(child)
        return knobs

    def knob(self, name):
        """Return matching Knob by name, None otherwise."""
        for knob in self.knobs():
            if knob.labelText == name:
                return knob
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

    def removeKnob(self, knob):
        """Remove the Knob reference to this node and resize."""
        knob.setParentItem(None)
        self.updateSizeForChildren()

    def paint(self, painter, option, widget):
        painter.setBrush(QtGui.QBrush(self.fillColor))
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))

        # The bounding box is only as high as the header (we do this
        # to limit the area that is move-enabled). Accommodate for that.
        bbox = self.boundingRect()
        painter.drawRoundedRect(self.x,
                                self.y,
                                bbox.width(),
                                self.h,
                                self.roundness,
                                self.roundness)

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

    def destroy(self):
        """Remove this Node, its Header, Knobs and connected Edges."""
        print("destroy node:", self)
        self.header.destroy()
        knobs = [c for c in self.childItems() if isinstance(c, Knob)]
        for knob in knobs:
            knob.destroy()

        scene = self.scene()
        scene.removeItem(self)
        del self
