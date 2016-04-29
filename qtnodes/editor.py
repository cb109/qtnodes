from PySide import QtGui
from PySide import QtCore

from port import Port
from connection import Connection
from block import Block


class Editor(QtCore.QObject):
    """The editor handles node events for the installed scene."""

    def __init__(self, parent):
        super(Editor, self).__init__(parent)
        self.conn = None
        self.scene = None

    def install(self, scene):
        scene.installEventFilter(self)
        self.scene = scene

    def itemAt(self, pos):
        items = self.scene.items(
            QtCore.QRectF(pos - QtCore.QPointF(1, 1), QtCore.QSize(3, 3)))
        for item in items:
            if isinstance(item, QtGui.QGraphicsItem):
                return item
        return None

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.GraphicsSceneMousePress:
            btn = event.button()
            if btn == QtCore.Qt.LeftButton:
                item = self.itemAt(event.scenePos())
                try:
                    item.mouse_pressed.emit(event)
                except Exception as err:
                    print err
                if item and isinstance(item, Port):
                    self.conn = Connection(None, self.scene)
                    self.conn.port1 = item
                    self.conn.pos1 = item.scenePos()
                    self.conn.pos2 = event.scenePos()
                    self.conn.update_path()
                    return True
                elif item and isinstance(item, Block):
                    pass
            elif btn == QtCore.Qt.RightButton:
                item = self.itemAt(event.scenePos())
                try:
                    item.mouse_pressed.emit(event)
                except Exception as err:
                    print err
                if item:
                    if isinstance(item, Connection) or isinstance(item, Block):
                        item.remove()

        elif event.type() == QtCore.QEvent.GraphicsSceneMouseMove:
            item = self.itemAt(event.scenePos())
            try:
                item.mouse_moved.emit(event)
            except Exception as err:
                print err
            if self.conn:
                self.conn.pos2 = event.scenePos()
                self.conn.update_path()
                return True

        elif event.type() == QtCore.QEvent.GraphicsSceneMouseRelease:
            item = self.itemAt(event.scenePos())
            try:
                item.mouse_released.emit(event)
            except Exception as err:
                print err
            if self.conn and event.button() == QtCore.Qt.LeftButton:
                if item and isinstance(item, Port):
                    port1 = self.conn.port1
                    port2 = item
                    if (port1.block != port2.block and
                        port1.is_output != port2.is_output and
                            not port1.is_connected(port2)):
                        self.conn.pos2 = port2.scenePos()
                        self.conn.port2 = port2
                        self.conn.update_path()
                        self.conn = None
                        return True
                self.conn.remove()
                self.conn = None
                return True
        return super(Editor, self).eventFilter(obj, event)

    def save(self):
        pass

    def load(self):
        pass
