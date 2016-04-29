from PySide import QtGui
from PySide import QtCore

from port import Port
from event import EventMixin


class Block(QtGui.QGraphicsPathItem, EventMixin):
    """A block holds ports that can be connected to."""

    def __init__(self, parent, scene):
        super(Block, self).__init__(parent, scene)
        self.horizontal_margin = 20
        self.vertical_margin = 5
        self.corner_roundness = 5

        self.width = self.horizontal_margin
        self.height = self.vertical_margin

        self.line_color = QtCore.Qt.darkGray
        self.fill_color = QtCore.Qt.lightGray
        self.hover_color = QtCore.Qt.yellow

        self.setup()

    def report(self, event):
        print "something happened:", event.type()

    def setup(self):
        p = QtGui.QPainterPath()
        p.addRoundedRect(-50, -15, 100, 30,
                         self.corner_roundness, self.corner_roundness)
        self.setPath(p)
        self.setFlag(self.ItemIsMovable)
        self.setFlag(self.ItemIsSelectable)

        # self.mouse_pressed.connect(self.report)
        # self.mouse_moved.connect(self.report)
        # self.mouse_released.connect(self.report)

    def add_port(self, name, is_output=False, style="default"):
        port = Port(self, self.scene(), style=style)
        port.name = name
        port.is_output = is_output
        port.block = self

        fm = QtGui.QFontMetrics(port.label.font())
        w = fm.width(name)
        h = fm.height()
        if w > self.width - self.horizontal_margin:
            self.width = w + self.horizontal_margin
        self.height += h

        p = QtGui.QPainterPath()
        p.addRoundedRect(-self.width / 2, -self.height / 2,
                         self.width, self.height,
                         self.corner_roundness, self.corner_roundness)
        self.setPath(p)

        y = -self.height / 2 + self.vertical_margin + port.radius_
        for thing in self.childItems():
            if not isinstance(thing, Port):
                continue
            port_ = thing
            if port_.is_output:
                port_.setPos(self.width / 2 + port_.radius_, y)
            else:
                port_.setPos(-self.width / 2 - port_.radius_, y)
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
            painter.setPen(QtGui.QPen(self.line_color))
            painter.setBrush(self.hover_color)
        else:
            painter.setPen(QtGui.QPen(self.line_color))
            painter.setBrush(self.fill_color)
        painter.drawPath(self.path())

    def clone(self):
        b = Block(None, self.scene())
        for thing in self.childItems():
            if not isinstance(thing, Port):
                continue
            port = thing
            b.add_port(port.name, port.is_output, style=port.style)
        return b

    @property
    def ports(self):
        ports = []
        for thing in self.childItems():
            if isinstance(thing, Port):
                ports.append(thing)
        return ports

    def remove(self):
        for thing in self.childItems():
            thing.remove()
        self.scene().removeItem(self)

    def itemChange(self, change, value):
        return value

    def save(self):
        pass

    def load(self):
        pass
