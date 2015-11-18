import sys

from PySide import QtGui

from libs.pyside_dynamic import loadUi

from block import Block
from port import Port
from connection import Connection
from editor import Editor


UI_FILE = "mainwindow.ui"


class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.editor = None
        loadUi(UI_FILE, self)

        scene = QtGui.QGraphicsScene()
        self.graphicsView.setScene(scene)
        self.graphicsView.setRenderHint(QtGui.QPainter.Antialiasing)

        # TODO: create test entries here


        self.editor = Editor(self)
        self.editor.install(scene)


def main():
    app = QtGui.QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
