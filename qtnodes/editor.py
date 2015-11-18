from PySide import QtGui
from PySide import QtCore

from port import Port
from connection import Connection
from block import Block


class Editor(QtCore.QObject):

    def __init__(self, parent):
        super(Editor, self).__init__(parent)
        self.conn = False
        self.scene = None

    def install(self, scene):
        scene.installEventFilter(self)
        self.scene = scene

    def itemAt(self, pos):
        items = self.scene.items(
            QtGui.QRectF(pos - QtGui.QPointF(1, 1), QtGui.QSize(3, 3)))
        for item in items:
            if isinstance(item, QtGui.QGraphicsItems):
                return item
        return None

    def eventFilter(self, obj, event):
        me = QtGui.QGraphicsSceneMouseEvent(event.type())
        if event.type == QtCore.QEvent.GraphicsSceneMousePress:
            btn = me.button()
            if btn == QtCore.QEvent.LeftButton:
                item = self.itemAt(me.scenePos())
                if isinstance(item, Port):
                    self.conn = Connection(None, self.scene)
                    self.conn.port1 = item
                    self.conn.pos1 = item.scenePos()
                    self.conn.pos2 = me.scenePos()
                    self.conn.update_path()
                    return True
                if isinstance(item, Block):
                    pass
            elif btn == QtCore.QEvent.RightButton:
                item = self.itemAt(me.scenePos())
                if isinstance(item, Connection) or isinstance(item, Block):
                    del item
        elif event.type == QtCore.QEvent.GraphicsSceneMouseMove:
            if self.conn:
                self.conn.pos2 = me.scenePos()
                self.conn.update_path()
                return True
        elif event.type == QtCore.QEvent.GraphicsSceneMouseRelease:
            if self.conn and me.button() == QtCore.QEvent.LeftButton:
                item = self.itemAt(me.scenePos())
                if isinstance(item, Port):
                    port1 = self.conn.port1
                    port2 = item
                    if (port1.block != port2.block and
                        port1.is_output != port2.is_output and not
                            port1.is_connected(port2)):
                        self.conn.pos2 = port2.scenePos()
                        self.conn.port2 = port2
                        self.conn.update_path()
                        self.conn = None
                        return True

            self.conn = None
            return True
        return super(Editor, self).eventFilter(obj, event)

    def save(self):
        pass

    def load(self):
        pass
