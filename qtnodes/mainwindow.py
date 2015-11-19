import os
import sys
import random

from PySide import QtGui

from libs.pyside_dynamic import loadUi

from block import Block
from editor import Editor


UI_FILE = os.path.join(os.path.dirname(__file__), "mainwindow.ui")


class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.editor = None
        loadUi(UI_FILE, self)

        scene = QtGui.QGraphicsScene()
        self.graphicsView.setScene(scene)
        self.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing)

        b = Block(None, scene)

        b.add_port("Operator 1", style="bold")
        b.add_port("Magic inside", style="italic")

        b.add_input_port("input 1")
        b.add_input_port("input 2")
        b.add_input_port("input 3")
        b.add_output_port("output 1")
        b.add_output_port("output 2")
        b.add_output_port("output 3")

        b = b.clone()
        b.setPos(150, 150)

        self.editor = Editor(self)
        self.editor.install(scene)

        self.setup_signals()

    def setup_signals(self):
        action = QtGui.QAction("Add Block", self)
        action.triggered.connect(self.add_block)
        self.toolBar.addAction(action)

    def add_block(self):
        b = Block(None, self.graphicsView.scene())
        names = ["Vin", "Voutsadfasdf", "Imin", "Imax",
                 "mul", "add", "sub", "div", "Conv", "FFT"]
        for i in range(0, random.randint(1, 4)):
            name = random.choice(names)
            b.add_port(name, random.randint(0, 1))
            b.setPos(self.graphicsView.sceneRect().center().toPoint())


def main():
    app = QtGui.QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
