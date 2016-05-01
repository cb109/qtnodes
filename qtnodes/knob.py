"""Knob classes."""

from PySide import QtGui
from PySide import QtCore

from .helpers import getTextSize
from .exceptions import KnobConnectionError, UnknownFlowError
from .edge import Edge

FLOW_LEFT_TO_RIGHT = "flow_left_to_right"
FLOW_RIGHT_TO_LEFT = "flow_right_to_left"


class Knob(QtGui.QGraphicsItem):
    """A Knob is a socket of a Node and can be connected to other Knobs."""

    def __init__(self, *args, **kwargs):
        super(Knob, self).__init__()
        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)
        self.w = kwargs.get("w", 10)
        self.h = kwargs.get("h", 10)
        self.margin = kwargs.get("margin", 5)
        self.flow = kwargs.get("flow", FLOW_LEFT_TO_RIGHT)

        # FIXME: This is basically the unique identifier now.
        #   We could create multiple Knobs with the same though,
        #   which would be a problem during deserialization.
        self.labelText = kwargs.get("labelText", "value")

        self.labelColor = kwargs.get("labelColor", QtGui.QColor(10, 10, 10))
        self.fillColor = kwargs.get("fillColor", QtGui.QColor(130, 130, 130))
        self.highlightColor = kwargs.get("highlightColor",
                                         QtGui.QColor(255, 255, 0))

        # Temp store for Edge currently being created.
        self.newEdge = None

        self.edges = []

        self.setAcceptHoverEvents(True)
        self.setAcceptTouchEvents(True)
        self.setAcceptDrops(True)

    def node(self):
        """This Knob's parent item is the Node it is attached to."""
        return self.parentItem()

    def highlight(self, toggle):
        """Toggle highlight color."""
        if toggle:
            self._oldFillColor = self.fillColor
            self.fillColor = self.highlightColor
        else:
            self.fillColor = self._oldFillColor

    def hoverEnterEvent(self, event):
        """Change Knob rectange color.

        Store the old color in a new attribute, so it can be restored.
        """
        self.highlight(True)
        super(Knob, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        """Change Knob rectange color.

        Retrieve the old color from an attribute to restore it.
        """
        self.highlight(False)
        super(Knob, self).hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        """Handle Edge creation."""
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            print("create edge")

            self.newEdge = Edge()
            self.newEdge.knob1 = self
            self.newEdge.pos2 = event.scenePos()
            self.newEdge.updatePath()

            # Make sure this is removed if the user cancels.
            self.addEdge(self.newEdge)
            return

    def mouseMoveEvent(self, event):
        """Update Edge position when currently creating one."""
        if self.newEdge:
            print("update edge")
            self.newEdge.pos2 = event.scenePos()
            self.newEdge.updatePath()

    def mouseReleaseEvent(self, event):
        """Update Edge position when currently creating one."""
        if event.button() == QtCore.Qt.MouseButton.LeftButton:

            node = self.parentItem()
            scene = node.scene()
            target = scene.itemAt(event.scenePos())
            try:
                if self.newEdge and target:
                    if self.newEdge.knob1 is target:
                        raise KnobConnectionError(
                            "Can't connect a Knob to itself.")

                    if isinstance(target, Knob):
                        if type(self) == type(target):
                            raise KnobConnectionError(
                                "Can't connect Knobs of same type.")

                        newConn = set([self, target])
                        for edge in self.edges:
                            existingConn = set([edge.knob1, edge.knob2])
                            diff = existingConn.difference(newConn)
                            if not diff:
                                raise KnobConnectionError(
                                    "Connection already exists.")
                                return

                        print("finalize edge")
                        target.addEdge(self.newEdge)
                        self.newEdge.knob2 = target
                        self.newEdge.updatePath()
                        self.newEdge = None
                        return

                raise KnobConnectionError(
                    "Edge creation cancelled by user.")
            except KnobConnectionError as err:
                print(err)
                # Abort Edge creation and do some cleanup.
                self.removeEdge(self.newEdge)
                self.newEdge = None

    def boundingRect(self):
        rect = QtCore.QRect(self.x,
                            self.y,
                            self.w,
                            self.h)
        return rect

    def paint(self, painter, option, widget):
        bbox = self.boundingRect()

        # Draw a filled rectangle.
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        painter.setBrush(QtGui.QBrush(self.fillColor))
        painter.drawRect(bbox)

        # Draw a text label next to it. Position depends on the flow.
        textSize = getTextSize(self.labelText, painter=painter)
        if self.flow == FLOW_LEFT_TO_RIGHT:
            x = bbox.right() + self.margin
        elif self.flow == FLOW_RIGHT_TO_LEFT:
            x = bbox.left() - self.margin - textSize.width()
        else:
            raise UnknownFlowError(
                "Flow not recognized: {0}".format(self.flow))
        y = bbox.bottom()

        painter.setPen(QtGui.QPen(self.labelColor))
        painter.drawText(x, y, self.labelText)

    def connectTo(self, knob):
        """Convenience method to connect this to another Knob."""
        if knob is self:
            return

        edge = Edge()
        edge.knob1 = self
        edge.knob2 = knob

        self.addEdge(edge)
        knob.addEdge(edge)

        edge.updatePath()

    def addEdge(self, edge):
        self.edges.append(edge)
        scene = self.scene()
        if edge not in scene.items():
            scene.addItem(edge)

    def removeEdge(self, edge):
        self.edges.remove(edge)
        scene = self.scene()
        if edge in scene.items():
            scene.removeItem(edge)

    def destroy(self):
        """Remove this Knob, its Edges and associations."""
        print("destroy knob:", self)
        edgesToDelete = self.edges[::]  # Avoid shrinking during deletion.
        for edge in edgesToDelete:
            edge.destroy()
        node = self.parentItem()
        if node:
            node.removeKnob(self)

        self.scene().removeItem(self)
        del self


class InputKnob(Knob):

    def __init__(self, *args, **kwargs):
        super(InputKnob, self).__init__(*args, **kwargs)
        self.labelText = kwargs.get("labelText", "input")
        self.fillColor = kwargs.get("fillColor", QtGui.QColor(130, 230, 130))


class OutputKnob(Knob):

    def __init__(self, *args, **kwargs):
        super(OutputKnob, self).__init__(*args, **kwargs)
        self.labelText = kwargs.get("labelText", "output")
        self.fillColor = kwargs.get("fillColor", QtGui.QColor(230, 130, 130))
        self.flow = kwargs.get("flow", FLOW_RIGHT_TO_LEFT)
