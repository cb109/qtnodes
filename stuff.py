from PySide import QtGui
from PySide import QtCore


# class Knob(QtGui.QGraphicsItem):

#     def __init__(self, parent=None, scene=None):
#         super(Knob, self).__init__(parent=parent, scene=scene)

#         self.w = 100
#         self.h = 100


class Node(QtGui.QGraphicsItem):

    def __init__(self, parent=None, scene=None):
        super(Node, self).__init__(parent=parent, scene=scene)

        self.x = -10
        self.y = -10
        self.w = 100
        self.h = 100

        self.xRadius = 0
        self.yRadius = 0

        self.headerHeight = 22

        self.knobWidth = 10
        self.knobHeight = 10

        self.brushColor = QtGui.QColor(220, 220, 220)
        self.brush = QtGui.QBrush(self.brushColor)

        self.penWidth = 1
        self.penColor = QtGui.QColor(100, 100, 100)
        # self.pen = QtGui.QPen(self.penColor)
        self.pen = QtGui.QPen(QtCore.Qt.NoPen)
        self.pen.setWidth(self.penWidth)

        # General configuration.
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setCursor(QtCore.Qt.SizeAllCursor)

        self.setAcceptHoverEvents(True)
        self.setAcceptTouchEvents(True)

    def boundingRect(self):
        return QtCore.QRectF(self.x - self.penWidth / 2,
                             self.y - self.penWidth / 2,
                             self.w + self.penWidth,
                             self.h + self.penWidth)

    def paint(self, painter, option, widget):
        painter.setBrush(self.brush)
        painter.setPen(self.pen)

        # general stuff
        bbox = self.boundingRect()
        outwards = 2
        margin = 5

        # body
        painter.drawRoundedRect(self.x,
                                self.y,
                                self.w,
                                self.h,
                                self.xRadius,
                                self.yRadius)

        # header
        brush = QtGui.QBrush(QtGui.QColor(90, 90, 90))
        painter.setBrush(brush)
        painter.drawRoundedRect(self.x,
                                self.y,
                                self.w,
                                self.headerHeight,
                                self.xRadius,
                                self.yRadius)

        # header text
        pen = QtGui.QPen(QtGui.QColor(240, 240, 240))
        painter.setPen(pen)
        painter.drawText(self.x + margin,
                         self.y + self.headerHeight - margin,
                         "my_node")

        # input knob
        inputKnobPosX = bbox.left() - outwards
        inputKnobPosY = bbox.center().y() - self.headerHeight
        inputKnobRect = QtCore.QRect(inputKnobPosX,
                                     inputKnobPosY,
                                     self.knobWidth,
                                     self.knobHeight)

        pen = QtGui.QPen(QtCore.Qt.NoPen)
        brush = QtGui.QBrush(QtGui.QColor(150, 250, 150))
        painter.setBrush(brush)
        painter.setPen(pen)
        painter.drawRoundedRect(inputKnobRect,
                                self.xRadius,
                                self.yRadius)

        # input knob text
        font = painter.font()
        font.setPixelSize(11)
        painter.setFont(font)

        brush = QtGui.QBrush(QtGui.QColor(10, 10, 10))
        pen = QtGui.QPen(brush, 1)
        painter.setPen(pen)

        painter.drawText(inputKnobPosX + margin + self.knobWidth,
                         inputKnobPosY + self.knobHeight,
                         "input")

        # output knob
        outputKnobPosX = bbox.right() - self.knobWidth + outwards
        outputKnobPosY = bbox.bottom() - self.headerHeight
        outputKnobRect = QtCore.QRect(outputKnobPosX,
                                      outputKnobPosY,
                                      self.knobWidth,
                                      self.knobHeight)

        pen = QtGui.QPen(QtCore.Qt.NoPen)
        brush = QtGui.QBrush(QtGui.QColor(250, 150, 150))
        painter.setBrush(brush)
        painter.setPen(pen)
        painter.drawRoundedRect(outputKnobRect,
                                self.xRadius,
                                self.yRadius)
        # painter.drawEllipse(outputKnobRect)

        # output knob text
        font = painter.font()
        font.setPixelSize(11)
        painter.setFont(font)

        brush = QtGui.QBrush(QtGui.QColor(10, 10, 10))
        pen = QtGui.QPen(brush, 1)
        painter.setPen(pen)

        size = painter.fontMetrics().size(QtCore.Qt.TextSingleLine, "output")
        outputKnobTextWidth = size.width()

        painter.drawText(
            outputKnobPosX - margin - outputKnobTextWidth,
            outputKnobPosY + self.knobHeight,
            "output")

    # def sceneEvent(self, event):
    #     print("sceneEvent()", event.type(), event)
    #     super(Node, self).sceneEvent(event)

    # def sceneEventFilter(self, watched, event):
    #     print("sceneEventFilter()", watched, event.type(), event)
    #     super(Node, self).sceneEventFilter(watched, event)

    def contextMenuEvent(self, event):
        print("contextMenuEvent()", event.type(), event)
        super(Node, self).contextMenuEvent(event)

    def focusInEvent(self, event):
        print("focusInEvent()", event.type(), event)
        super(Node, self).focusInEvent(event)

    def focusOutEvent(self, event):
        print("focusOutEvent()", event.type(), event)
        super(Node, self).focusOutEvent(event)

    def hoverEnterEvent(self, event):
        print("hoverEnterEvent()", event.type(), event)
        super(Node, self).hoverEnterEvent(event)

    def hoverMoveEvent(self, event):
        print("hoverMoveEvent()", event.type(), event)
        super(Node, self).hoverMoveEvent(event)

    def hoverLeaveEvent(self, event):
        print("hoverLeaveEvent()", event.type(), event)
        super(Node, self).hoverLeaveEvent(event)

    def inputMethodEvent(self, event):
        print("inputMethodEvent()", event.type(), event)
        super(Node, self).inputMethodEvent(event)

    def keyPressEvent(self, event):
        print("keyPressEvent()", event.type(), event)
        super(Node, self).keyPressEvent(event)

    def keyReleaseEvent(self, event):
        print("keyReleaseEvent()", event.type(), event)
        super(Node, self).keyReleaseEvent(event)

    def mousePressEvent(self, event):
        print("mousePressEvent()", event.type(), event)
        super(Node, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        print("mouseMoveEvent()", event.type(), event)
        super(Node, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        print("mouseReleaseEvent()", event.type(), event)
        super(Node, self).mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        print("mouseDoubleClickEvent()", event.type(), event)
        super(Node, self).mouseDoubleClickEvent(event)


class NodeGraphWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(NodeGraphWidget, self).__init__(parent=parent)

        self.scene = QtGui.QGraphicsScene()
        self.view = QtGui.QGraphicsView()
        self.view.setScene(self.scene)

        self.view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.view.setViewportUpdateMode(
            QtGui.QGraphicsView.BoundingRectViewportUpdate)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    def addNode(self, node):
        self.scene.addItem(node)


app = QtGui.QApplication([])

graph = NodeGraphWidget()
graph.setGeometry(100, 100, 640, 480)
graph.show()

node1 = Node(scene=graph.scene)
node2 = Node()
graph.addNode(node2)

app.exec_()
