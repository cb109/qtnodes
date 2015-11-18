from PySide import QtGui
from PySide import QtCore


class Connection(QtGui.QGraphicsPathItem):
    """Connects one port to another."""

    def __init__(self, parent, scene):
        super(Connection, self).__init__(parent, scene)

        self.pos1 = None
        self.pos1 = None

        self.port1 = False
        self.port2 = False

        self.setup()

    def setup(self):
        self.setPen(QtCore.Qt.black, 2)
        self.setBrush(QtCore.Qt.NoBrush)
        self.setZValue(-1)

    @property
    def port1(self):
        return self.port1

    @port1.setter
    def port1(self, port):
        self.port1 = port
        self.port1.connections.append(self)

    @property
    def port2(self):
        return self.port2

    @port2.setter
    def port2(self, port):
        self.port2 = port
        self.port2.connections.append(self)

    def update_pos_from_ports(self):
        self.pos1 = self.port1.scenePos()
        self.pos2 = self.port2.scenePos()

    def update_path(self):
        p = QtGui.QPainerPath()
        p.moveTo(self.pos1)

        dx = self.pos2.x() - self.pos1.x()
        dy = self.pos2.y() - self.pos1.y()

        ctr1 = QtGui.QPointF(self.pos1.x() + dx * 0.25,
                             self.pos.y() + dy * 0.1)
        ctr2 = QtGui.QPointF(self.pos1.x() + dx * 0.75,
                             self.pos.y() + dy * 0.9)
        p.cubicTo(ctr1, ctr2, self.pos2)
        self.setPath(p)

    def save(self):
        pass

    def load(self):
        pass
