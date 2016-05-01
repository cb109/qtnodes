"""Connections between Knobs."""

from PySide import QtGui
from PySide import QtCore


class Edge(QtGui.QGraphicsPathItem):
    """A connection between two Knobs."""

    def __init__(self):
        super(Edge, self).__init__()

        self.lineColor = QtGui.QColor(10, 10, 10)
        self.thickness = 1

        self.knob1 = None
        self.knob2 = None

        self.pos1 = QtCore.QPointF(0, 0)
        self.pos2 = QtCore.QPointF(0, 0)

        self.curv1 = 0.6
        self.curv3 = 0.4

        self.curv2 = 0.2
        self.curv4 = 0.8

        self.setAcceptHoverEvents(True)

    def mousePressEvent(self, event):
        """Delete Edge if icon is clicked with CTRL pressed."""
        leftmouse = event.button() == QtCore.Qt.MouseButton.LeftButton
        ctrl = event.modifiers() == QtCore.Qt.ControlModifier
        if leftmouse and ctrl:
            self.knob1.removeEdge(self)
            self.knob2.removeEdge(self)
            del self

    def paint(self, painter, option, widget):
        self.setPen(QtGui.QPen(self.lineColor, self.thickness))
        self.setBrush(QtCore.Qt.NoBrush)
        self.setZValue(-1)
        super(Edge, self).paint(painter, option, widget)

    def updatePath(self):
        if self.knob1:
            self.pos1 = self.knob1.mapToScene(
                self.knob1.boundingRect().center())

        if self.knob2:
            self.pos2 = self.knob2.mapToScene(
                self.knob2.boundingRect().center())

        path = QtGui.QPainterPath()
        path.moveTo(self.pos1)

        dx = self.pos2.x() - self.pos1.x()
        dy = self.pos2.y() - self.pos1.y()

        ctrl1 = QtCore.QPointF(self.pos1.x() + dx * self.curv1,
                               self.pos1.y() + dy * self.curv2)
        ctrl2 = QtCore.QPointF(self.pos1.x() + dx * self.curv3,
                               self.pos1.y() + dy * self.curv4)
        path.cubicTo(ctrl1, ctrl2, self.pos2)
        self.setPath(path)
