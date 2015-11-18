from PySide import QtGui
from PySide import QtCore

from port import Port


class Block(QtGui.QGraphicsPathItem):
    """A block holds ports that can be connected to."""

    def __init__(self, parent, scene):
        super(Block, self).__init__(parent, scene)
        self.horizontal_margin = 20
        self.vertical_margin = 5

        self.width = self.horizontal_margin
        self.height = self.vertical_margin

        self.setup()

    def setup(self):
        p = QtGui.QPainterPath()
        p.addRoundedRect(-50, -15, 100, 30, 5, 5)
        self.setPath(p)

        self.setPen(QtGui.QPen(QtCore.Qt.darkGreen))
        self.setBrush(QtCore.Qt.green)
        self.setFlag(self.ItemIsMovable)
        self.setFlag(self.ItemIsSelectable)

    def add_port(self, name, is_output, flags=None):
        if not flags:
            flags = []
        port = Port(self, self.scene())
        port.name = name
        port.is_output = is_output
        port.block = self
        port.flags = flags

        fm = QtGui.QFontMetrics(self.scene().font())
        w = fm.width(name)
        h = fm.height()
        if w > self.width - self.horizontal_margin:
            self.width = w + self.horizontal_margin
        self.height += h

        p = QtGui.QPainterPath()
        p.addRoundedRect(-self.width / 2, -self.height / 2,
                         self.width, self.height, 5, 5)
        self.setPath(p)

        y = -self.height / 2 + self.vertical_margin + port.radius_
        for thing in self.childItems():
            if not isinstance(thing, Port):
                continue
            port_ = thing
            if port_.is_output:
                port_.setPos(self.width / 2 + port.radius_, y)
            else:
                port.setPos(-self.width / 2 - port.radius_, y)
            y += h
        return port

    def add_input_port(self, name):
        self.add_port(name, False)

    def add_output_port(self, name):
        self.add_port(name, True)

    def add_input_ports(self, names):
        for name in names:
            self.add_port(name, False)

    def add_output_ports(self, names):
        for name in names:
            self.add_port(name, True)

    def paint(self, painter, option, widget):
        if self.isSelected():
            painter.setPen(QtGui.QPen(QtCore.Qt.darkYellow))
            painter.setBrush(QtCore.Qt.yellow)
        else:
            painter.setPen(QtGui.QPen(QtCore.Qt.darkGreen))
            painter.setBrush(QtCore.Qt.green)
        painter.drawPath(self.path())

    def clone(self):
        b = Block(None, self.scene())
        for thing in self.childItems():
            if not isinstance(thing, Port):
                continue
            port = thing
            b.add_port(port.name, port.is_output, port.flags)
        return b

    @property
    def ports(self):
        ports = []
        for thing in self.childItems():
            if isinstance(thing, Port):
                ports.append(thing)
        return ports

    def itemChange(self, change, value):
        return value

    def save(self):
        pass

    def load(self):
        pass
