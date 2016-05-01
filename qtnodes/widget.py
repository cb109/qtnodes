"""Editor widget."""

from PySide import QtGui

from .view import GridView


class NodeGraphWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(NodeGraphWidget, self).__init__(parent=parent)

        self.scene = QtGui.QGraphicsScene()
        self.view = GridView()
        self.view.setScene(self.scene)

        self.view.setRenderHint(QtGui.QPainter.Antialiasing)
        self.view.setViewportUpdateMode(
            QtGui.QGraphicsView.FullViewportUpdate)

        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

    def addNode(self, node):
        if node not in self.scene.items():
            self.scene.addItem(node)
