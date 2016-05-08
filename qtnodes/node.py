"""Node classes."""

import uuid

from PySide import QtGui
from PySide import QtCore

from .helpers import getTextSize
from .knob import Knob, InputKnob, OutputKnob
from .exceptions import DuplicateKnobNameError


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

    def knobs(self, cls=None):
        """Return a list of childItems that are Knob objects.

        If the optional `cls` is specified, return only Knobs of that class.
        This is useful e.g. to get all InputKnobs or OutputKnobs.
        """
        knobs = []
        for child in self.childItems():
            if isinstance(child, Knob):
                knobs.append(child)

        if cls:
            knobs = filter(knobs, lambda k: k.__class__ is cls)

        return knobs

    def knob(self, name):
        """Return matching Knob by its name, None otherwise."""
        for knob in self.knobs():
            if knob.name == name:
                return knob
        return None

    def boundingRect(self):
        """Return the bounding box of the Node, limited in height to its Header.

        This is so that the drag & drop sensitive area for the Node is only
        active when hovering its Header, as otherwise there would be conflicts
        with the hover events for the Node's Knobs.
        """
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
            knobWidths = [k.w + self.margin + getTextSize(k.displayName).width()
                          for k in knobs]
            maxWidth = max([headerWidth] + knobWidths)
            self.w = maxWidth + self.margin

        adjustWidth()
        adjustHeight()

    def addHeader(self, header):
        """Assign the given header and adjust the Node's size for it."""
        self.header = header
        header.setPos(self.pos())
        header.setParentItem(self)
        self.updateSizeForChildren()

    def addKnob(self, knob):
        """Add the given Knob to this Node.

        A Knob must have a unique name, meaning there can be no duplicates within 
        a Node (the displayNames are not constrained though).

        Assign ourselves as the Knob's parent item (which also will put it onto
        the current scene, if not yet done) and adjust or size for it.

        The position of the Knob is set relative to this Node and depends on it
        either being an Input- or OutputKnob.
        """
        knobNames = [k.name for k in self.knobs()]
        if knob.name in knobNames:
            raise DuplicateKnobNameError(
                "Knob names must be unique, but {0} already exists."
                .format(knob.name))

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
        """Draw the Node's container rectangle."""
        painter.setBrush(QtGui.QBrush(self.fillColor))
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))

        # The bounding box is only as high as the header (we do this
        # to limit the area that is drag-enabled). Accommodate for that.
        bbox = self.boundingRect()
        painter.drawRoundedRect(self.x,
                                self.y,
                                bbox.width(),
                                self.h,
                                self.roundness,
                                self.roundness)

    def mouseMoveEvent(self, event):
        """Update selected item's (and children's) positions as needed.

        We assume here that only Nodes can be selected.

        We cannot just update our own childItems, since we are using
        RubberBandDrag, and that would lead to otherwise e.g. Edges
        visually lose their connection until an attached Node is moved
        individually.
        """
        nodes = self.scene().selectedItems()
        for node in nodes:
            for knob in node.knobs():
                for edge in knob.edges:
                    edge.updatePath()
        super(Node, self).mouseMoveEvent(event)

    def destroy(self):
        """Remove this Node, its Header, Knobs and connected Edges."""
        print("destroy node:", self)
        self.header.destroy()
        for knob in self.knobs():
            knob.destroy()

        scene = self.scene()
        scene.removeItem(self)
        del self
