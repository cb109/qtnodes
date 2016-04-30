from PySide import QtGui
from PySide import QtCore


FLOW_LEFT_TO_RIGHT = "flow_left_to_right"
FLOW_RIGHT_TO_LEFT = "flow_right_to_left"


class QtNodesError(Exception):
    """Base custom exception."""


class UnknownFlowError(QtNodesError):
    """The flow style can not be recognized."""


def getTextSize(text, painter=None):
    """Return a QSize based on given string.

    If no painter is supplied, the font metrics are based on a default
    QPainter, which may be off depending on the font und text size used.
    """
    if not painter:
        metrics = QtGui.QFontMetrics(QtGui.QFont())
    else:
        metrics = painter.fontMetrics()
    size = metrics.size(QtCore.Qt.TextSingleLine, text)
    return size


class Knob(QtGui.QGraphicsItem):

    def __init__(self, *args, **kwargs):
        super(Knob, self).__init__()
        self.x = kwargs.get("x", 0)
        self.y = kwargs.get("y", 0)
        self.w = kwargs.get("w", 10)
        self.h = kwargs.get("h", 10)
        self.margin = kwargs.get("margin", 5)
        self.flow = kwargs.get("margin", FLOW_LEFT_TO_RIGHT)

        self.labelText = kwargs.get("labelText", "value")
        self.labelColor = kwargs.get("labelColor", QtGui.QColor(10, 10, 10))
        self.fillColor = kwargs.get("fillColor", QtGui.QColor(130, 130, 130))

        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        """Change knob rectange color.

        Store the old color in a new attribute, so it can be restored.
        """
        self._oldFillColor = self.fillColor
        self.fillColor = QtGui.QColor(255, 255, 0)
        super(Knob, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        """Change knob rectange color.

        Retrieve the old color from an attribute to restore it.
        """
        self.fillColor = self._oldFillColor
        super(Knob, self).hoverLeaveEvent(event)

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

        painter.setPen(QtGui.QPen(self.labelColor))

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

        painter.drawText(x, y, self.labelText)


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


class Header(QtGui.QGraphicsItem):

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
        painter.drawRect(bbox)

        # Draw header label.
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


class Node(QtGui.QGraphicsItem):

    def __init__(self):
        super(Node, self).__init__()

        self.header = None

        self.x = 0
        self.y = 0
        self.w = 10
        self.h = 10

        self.margin = 6

        self.fillColor = QtGui.QColor(220, 220, 220)

        # General configuration.
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setCursor(QtCore.Qt.SizeAllCursor)

        self.setAcceptHoverEvents(True)
        self.setAcceptTouchEvents(True)
        self.setAcceptDrops(True)

    def boundingRect(self):
        rect = QtCore.QRect(self.x,
                            self.y,
                            self.w,
                            self.h)
        return rect

    def updateSizeForChildren(self):
        """Adjust width and height as needed for header and knobs."""

        class NoOpHeader(object):
            """Stand-in for when there is no header."""
            h = 0
            text = ""
        header = self.header or NoOpHeader()

        def adjustHeight():
            """Adjust height to fit header and all knobs."""
            knobs = [c for c in self.childItems() if isinstance(c, Knob)]
            knobsHeight = sum([k.h + self.margin for k in knobs])
            heightNeeded = header.h + knobsHeight + self.margin
            self.h = heightNeeded

        def adjustWidth():
            """Adjust width as needed for the widest child item."""
            headerWidth = (self.margin + getTextSize(header.text).width())

            knobs = [c for c in self.childItems() if isinstance(c, Knob)]
            knobWidths = [k.w + self.margin + getTextSize(k.labelText).width()
                          for k in knobs]
            maxWidth = max([headerWidth] + knobWidths)
            self.w = maxWidth + self.margin

        adjustWidth()
        adjustHeight()
        self.update()

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

        bbox = self.boundingRect()
        painter.drawRect(bbox)

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

    # def mouseMoveEvent(self, event):
    #     print("mouseMoveEvent()", event.type(), event)
    #     super(Node, self).mouseMoveEvent(event)

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


class NodeGraphWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(NodeGraphWidget, self).__init__(parent=parent)

        self.scene = QtGui.QGraphicsScene()
        self.view = QtGui.QGraphicsView()
        self.view.setScene(self.scene)

        self.view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.view.setViewportUpdateMode(
            QtGui.QGraphicsView.FullViewportUpdate)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    def addNode(self, node):
        self.scene.addItem(node)


class Multiply(Node):

    def __init__(self):
        super(Multiply, self).__init__()
        self.addHeader(Header(node=self, text="Multiply"))
        self.addKnob(InputKnob(labelText="x"))
        self.addKnob(InputKnob(labelText="y"))
        self.addKnob(OutputKnob(labelText="value"))
        # self.header.fillColor = QtGui.QColor(150, 150, 90)


class Integer(Node):

    def __init__(self):
        super(Integer, self).__init__()
        self.addHeader(Header(node=self, text="Int"))
        self.addKnob(OutputKnob(labelText="value"))
        # self.header.fillColor = QtGui.QColor(90, 150, 90)


class Float(Node):

    def __init__(self):
        super(Float, self).__init__()
        self.addHeader(Header(node=self, text="Float"))
        self.addKnob(OutputKnob(labelText="value"))
        # self.header.fillColor = QtGui.QColor(90, 90, 150)


def test():
    app = QtGui.QApplication([])

    graph = NodeGraphWidget()
    graph.setGeometry(100, 100, 640, 480)
    graph.show()

    graph.addNode(Integer())
    graph.addNode(Float())
    graph.addNode(Multiply())
    # node1 = Node()
    # graph.addNode(node1)
    # node1.addHeader(Header(node=node1, text="Multiply"))
    # node1.addKnob(InputKnob(labelText="x"))
    # node1.addKnob(InputKnob(labelText="y"))
    # node1.addKnob(OutputKnob(labelText="value"))

    app.exec_()


if __name__ == '__main__':
    test()
