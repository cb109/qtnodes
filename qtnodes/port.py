from PySide import QtGui
from PySide import QtCore


class Port(QtGui.QGraphicsPathItem):
    """A port is attached to a node and accepts connections."""

    def __init__(self, parent, scene):
        super(Port, self).__init__(parent, scene)
        self.name = "port"

        self.block = None
        self.connections = []
        self.is_output = False
        self.port_flags = []

        self.radius_ = 5
        self.margin = 2

        self.setup()

    def setup(self):
        self._label = QtGui.QGraphicsTextItem(self)
        self._path = QtGui.QPainterPath()
        self._path.addEllipse(-self.radius_, -self.radius_,
                              2 * self.radius_, 2 * self.radius_)
        self.setPath(self._path)
        self.setPen(QtCore.Qt.darkRed)
        self.setBrush(QtCore.Qt.red)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsScenePositionChanges)

    @property
    def name(self):
        return self.name

    @name.setter
    def name(self, name):
        self.name = name
        self._label.setPlainText(name)

    @property
    def is_output(self):
        return self.is_output

    @is_output.setter
    def is_output(self, is_output):
        self.is_output = is_output
        # Adapt label size.
        if is_output:
            self._label.setPos(
                -self.radius_ - self.margin - self.label.boundingRect().width(),
                -self.label.boundingRect().height() / 2)
        else:
            self._label.setPos(self.radius_ + self.margin,
                               self._label.boundingRect().height() / 2)

    #
    # TODO: Handle port flags and change of appearance based of them.
    #

    def is_connected(self, other_port):
        for conn in self.connections:
            if conn.port1 == other_port or conn.port2 == other_port:
                return True
        return False

    def itemChange(self, change, value):
        if change == self.ItemScenePositionHasChanged:
            for conn in self.connections:
                conn.update_pos_from_ports()
                conn.update_path()
        return value
