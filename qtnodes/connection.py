from PySide import QtGui
from PySide import QtCore


class Connection(QtGui.QGraphicsPathItem):
    """Connects one port to another."""

    def __init__(self, parent, scene):
        super(Connection, self).__init__(parent, scene)

        self._pos1 = None
        self._pos1 = None

        self._port1 = False
        self._port2 = False

        self.line_color = QtCore.Qt.black
        self.hover_color = QtCore.Qt.yellow
        self.thickness = 2

        self.setup()

    def setup(self):
        self.setPen(QtGui.QPen(self.line_color, self.thickness))
        self.setBrush(QtCore.Qt.NoBrush)
        self.setZValue(-1)

    @property
    def port1(self):
        return self._port1

    @port1.setter
    def port1(self, port):
        self._port1 = port
        self._port1.connections.append(self)

    @property
    def port2(self):
        return self._port2

    @port2.setter
    def port2(self, port):
        self._port2 = port
        self._port2.connections.append(self)

    def update_pos_from_ports(self):
        self.pos1 = self.port1.scenePos()
        self.pos2 = self.port2.scenePos()

    def update_path(self):
        p = QtGui.QPainterPath()
        p.moveTo(self.pos1)

        dx = self.pos2.x() - self.pos1.x()
        dy = self.pos2.y() - self.pos1.y()

        ctr1 = QtCore.QPointF(self.pos1.x() + dx * 0.35,
                              self.pos1.y() + dy * 0.1)
        ctr2 = QtCore.QPointF(self.pos1.x() + dx * 0.65,
                              self.pos1.y() + dy * 0.9)
        p.cubicTo(ctr1, ctr2, self.pos2)
        self.setPath(p)

    def remove(self):
        try:
            self.port1.connection.remove(self)
        except (AttributeError, ValueError):
            pass
        try:
            self.port2.connection.remove(self)
        except (AttributeError, ValueError):
            pass
        try:
            self.scene().removeItem(self)
        except AttributeError:
            pass

    def save(self):
        pass

    def load(self):
        pass
