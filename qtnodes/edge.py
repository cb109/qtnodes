"""Connections between Knobs."""

import os

from .qtchooser import QtCore, QtGui, QtWidgets


windows = os.name == "nt"

DELETE_MODIFIER_KEY = QtCore.Qt.AltModifier if windows else QtCore.Qt.ControlModifier


class Edge(QtWidgets.QGraphicsPathItem):
    """A connection between two Knobs."""

    def __init__(self, **kwargs):
        super(Edge, self).__init__(**kwargs)

        self.lineColor = QtGui.QColor(10, 10, 10)
        self.removalColor = QtCore.Qt.red
        self.thickness = 1

        self.source = None  # A Knob.
        self.target = None  # A Knob.

        self.sourcePos = QtCore.QPointF(0, 0)
        self.targetPos = QtCore.QPointF(0, 0)

        self.curv1 = 0.6
        self.curv3 = 0.4

        self.curv2 = 0.2
        self.curv4 = 0.8

        self.setAcceptHoverEvents(True)

    def mousePressEvent(self, event):
        """Delete Edge if icon is clicked with DELETE_MODIFIER_KEY pressed."""
        leftMouse = event.button() == QtCore.Qt.MouseButton.LeftButton
        mod = event.modifiers() == DELETE_MODIFIER_KEY
        if leftMouse and mod:
            self.destroy()

    def updatePath(self):
        """Adjust current shape based on Knobs and curvature settings."""
        if self.source:
            self.sourcePos = self.source.mapToScene(
                self.source.boundingRect().center())

        if self.target:
            self.targetPos = self.target.mapToScene(
                self.target.boundingRect().center())

        path = QtGui.QPainterPath()
        path.moveTo(self.sourcePos)

        dx = self.targetPos.x() - self.sourcePos.x()
        dy = self.targetPos.y() - self.sourcePos.y()

        ctrl1 = QtCore.QPointF(self.sourcePos.x() + dx * self.curv1,
                               self.sourcePos.y() + dy * self.curv2)
        ctrl2 = QtCore.QPointF(self.sourcePos.x() + dx * self.curv3,
                               self.sourcePos.y() + dy * self.curv4)
        path.cubicTo(ctrl1, ctrl2, self.targetPos)
        self.setPath(path)

    def paint(self, painter, option, widget):
        """Paint Edge color depending on modifier key pressed or not."""
        mod = QtGui.QGuiApplication.keyboardModifiers() == DELETE_MODIFIER_KEY
        if mod:
            self.setPen(QtGui.QPen(self.removalColor, self.thickness))
        else:
            self.setPen(QtGui.QPen(self.lineColor, self.thickness))

        # self.setBrush(QtCore.Qt.NoBrush)
        self.setZValue(-1)
        super(Edge, self).paint(painter, option, widget)

    def destroy(self):
        """Remove this Edge and its reference in other objects."""
        print("destroy edge:", self)
        if self.source:
            self.source.removeEdge(self)
        if self.target:
            self.target.removeEdge(self)
        del self
