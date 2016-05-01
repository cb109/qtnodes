"""Knob classes."""

from PySide import QtGui
from PySide import QtCore

from .helpers import getTextSize
from .exceptions import KnobConnectionError, UnknownFlowError
from .edge import Edge


# Currently only affects Knob label placement.
FLOW_LEFT_TO_RIGHT = "flow_left_to_right"
FLOW_RIGHT_TO_LEFT = "flow_right_to_left"


class Knob(QtGui.QGraphicsItem):
    """A Knob is a socket of a Node and can be connected to other Knobs."""

    def __init__(self, **kwargs):
        super(Knob, self).__init__(**kwargs)
        self.x = 0
        self.y = 0
        self.w = 10
        self.h = 10
        self.margin = 5
        self.flow = FLOW_LEFT_TO_RIGHT

        # FIXME: This is basically the unique identifier now.
        #   We could create multiple Knobs with the same though,
        #   which would be a problem during deserialization.
        self.labelText = "value"

        self.labelColor = QtGui.QColor(10, 10, 10)
        self.fillColor = QtGui.QColor(130, 130, 130)
        self.highlightColor = QtGui.QColor(255, 255, 0)

        # Temp store for Edge currently being created.
        self.newEdge = None

        self.edges = []

        self.setAcceptHoverEvents(True)

    def node(self):
        """This Knob's parent item is the Node it is attached to."""
        return self.parentItem()

    def connectTo(self, knob):
        """Convenience method to connect this to another Knob."""
        if knob is self:
            return

        edge = Edge()
        edge.source = self
        edge.target = knob

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

    def boundingRect(self):
        rect = QtCore.QRect(self.x,
                            self.y,
                            self.w,
                            self.h)
        return rect

    def highlight(self, toggle):
        """Toggle highlight color."""
        if toggle:
            self._oldFillColor = self.fillColor
            self.fillColor = self.highlightColor
        else:
            self.fillColor = self._oldFillColor

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
            self.newEdge.source = self
            self.newEdge.targetPos = event.scenePos()
            self.newEdge.updatePath()

            # Make sure this is removed if the user cancels.
            self.addEdge(self.newEdge)
            return

    def mouseMoveEvent(self, event):
        """Update Edge position when currently creating one."""
        if self.newEdge:
            print("update edge")
            self.newEdge.targetPos = event.scenePos()
            self.newEdge.updatePath()

    def mouseReleaseEvent(self, event):
        """Update Edge position when currently creating one.

        These currently implements some constraints regarding the Knob
        connection logic, for which we should probably have a more
        flexible approach.
        """
        if event.button() == QtCore.Qt.MouseButton.LeftButton:

            node = self.parentItem()
            scene = node.scene()
            target = scene.itemAt(event.scenePos())

            try:
                if self.newEdge and target:

                    if self.newEdge.source is target:
                        raise KnobConnectionError(
                            "Can't connect a Knob to itself.")

                    if isinstance(target, Knob):
                        if type(self) == type(target):
                            raise KnobConnectionError(
                                "Can't connect Knobs of same type.")

                        newConn = set([self, target])
                        for edge in self.edges:
                            existingConn = set([edge.source, edge.target])
                            diff = existingConn.difference(newConn)
                            if not diff:
                                raise KnobConnectionError(
                                    "Connection already exists.")
                                return

                        print("finish edge")
                        target.addEdge(self.newEdge)
                        self.newEdge.target = target
                        self.newEdge.updatePath()
                        self.finalizeEdge(self.newEdge)
                        self.newEdge = None
                        return

                raise KnobConnectionError(
                    "Edge creation cancelled by user.")

            except KnobConnectionError as err:
                print(err)
                # Abort Edge creation and do some cleanup.
                self.removeEdge(self.newEdge)
                self.newEdge = None

    def finalizeEdge(self, edge):
        """This intentionally is a NoOp on the Knob baseclass.

        It is meant for subclass Knobs to implement special behaviour
        that needs to be considered when connecting two Knobs.
        """
        pass

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


def ensureEdgeDirection(edge):
    """Make sure the Edge direction is as described below.

       .source --> .target
    OutputKnob --> InputKnob

    Which basically translates to:

    'Node with OutputKnob is the child of the Node with the InputKnob.''

    This may seem the exact opposite way as expected, but makes sense
    when seen as a hierarchy: A Node which output depends on some other
    Node's input can be seen as a *child* of the other Node. We need
    that information to build a directed graph.

    We assume here that there always is an InputKnob and an OutputKnob
    in the given Edge, just their order may be wrong. Since the
    serialization relies on that order, it is enforced here.
    """
    print("ensure edge direction")
    if isinstance(edge.target, OutputKnob):
        assert isinstance(edge.source, InputKnob)
        actualTarget = edge.source
        edge.source = edge.target
        edge.target = actualTarget
    else:
        assert isinstance(edge.source, OutputKnob)
        assert isinstance(edge.target, InputKnob)

    print("src:", edge.source.__class__.__name__,
          "trg:", edge.target.__class__.__name__)


class InputKnob(Knob):

    def __init__(self, *args, **kwargs):
        super(InputKnob, self).__init__(*args, **kwargs)
        self.labelText = kwargs.get("labelText", "input")
        self.fillColor = kwargs.get("fillColor", QtGui.QColor(130, 230, 130))

    def finalizeEdge(self, edge):
        ensureEdgeDirection(edge)


class OutputKnob(Knob):

    def __init__(self, *args, **kwargs):
        super(OutputKnob, self).__init__(*args, **kwargs)
        self.labelText = kwargs.get("labelText", "output")
        self.fillColor = kwargs.get("fillColor", QtGui.QColor(230, 130, 130))
        self.flow = kwargs.get("flow", FLOW_RIGHT_TO_LEFT)

    def finalizeEdge(self, edge):
        ensureEdgeDirection(edge)
