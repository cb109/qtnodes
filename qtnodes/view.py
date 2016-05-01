"""Custom QGraphicsView."""

from PySide import QtGui
from PySide import QtCore


CURRENT_ZOOM = 1.0


class GridView(QtGui.QGraphicsView):
    """This view will draw a grid in its background."""

    def __init__(self, *args, **kwargs):
        super(GridView, self).__init__(*args, **kwargs)

        self.fillColor = QtGui.QColor(250, 250, 250)
        self.lineColor = QtGui.QColor(230, 230, 230)

        self.xStep = 20
        self.yStep = 20

        self.panningMult = 2.0 * CURRENT_ZOOM
        self.panning = False
        self.zoomStep = 1.1

        # Since we implement custom panning, we don't need the scrollbars.
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        # self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)

    def mousePressEvent(self, event):
        """Initiate custom panning using middle mouse button."""
        if event.button() == QtCore.Qt.MiddleButton:
            self.setDragMode(QtGui.QGraphicsView.NoDrag)
            self.panning = True
            self.prevPos = event.pos()
            self.setCursor(QtCore.Qt.SizeAllCursor)
        elif event.button() == QtCore.Qt.LeftButton:
            self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        super(GridView, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.panning:
            delta = (self.mapToScene(event.pos()) * self.panningMult -
                     self.mapToScene(self.prevPos) * self.panningMult) * -1.0
            center = QtCore.QPoint(self.viewport().width() / 2 + delta.x(),
                                   self.viewport().height() / 2 + delta.y())
            newCenter = self.mapToScene(center)
            self.centerOn(newCenter)
            self.prevPos = event.pos()
            return
        super(GridView, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.panning:
            self.panning = False
            self.setCursor(QtCore.Qt.ArrowCursor)
        super(GridView, self).mouseReleaseEvent(event)

    def wheelEvent(self, event):
        positive = event.delta() >= 0
        zoom = self.zoomStep if positive else 1.0 / self.zoomStep
        self.scale(zoom, zoom)

        # Assuming we always scale x and y proportionally, expose the
        # current horizontal scaling factor so other items can use it.
        global CURRENT_ZOOM
        CURRENT_ZOOM = self.transform().m11()

        super(GridView, self).wheelEvent(event)

    def drawBackground(self, painter, rect):
        painter.setBrush(QtGui.QBrush(self.fillColor))
        painter.setPen(QtGui.QPen(self.lineColor))

        top = rect.top()
        bottom = rect.bottom()
        left = rect.left()
        right = rect.right()

        lines = []

        currentXPos = left
        while currentXPos <= right:
            line = QtCore.QLine(currentXPos, top, currentXPos, bottom)
            lines.append(line)
            currentXPos += self.xStep

        currentYPos = top
        while currentYPos <= bottom:
            line = QtCore.QLine(left, currentYPos, right, currentYPos)
            lines.append(line)
            currentYPos += self.yStep

        painter.drawRect(rect)
        painter.drawLines(lines)
