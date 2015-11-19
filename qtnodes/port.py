from PySide import QtGui
from PySide import QtCore


class Port(QtGui.QGraphicsPathItem):
    """A port is attached to a node and accepts connections."""

    def __init__(self, parent, scene, style="default"):
        super(Port, self).__init__(parent, scene)
        self._name = "port"
        self._is_output = False

        self.style = style  # 'default', 'italic', 'bold'
        self.block = None
        self.connections = []

        self.radius_ = 5
        self.margin = 2

        self.setup()

    def setup(self):
        self._label = QtGui.QGraphicsTextItem(self)
        self._path = QtGui.QPainterPath()
        self._path.addEllipse(-self.radius_, -self.radius_,
                              2 * self.radius_, 2 * self.radius_)
        self.setPath(self._path)
        self.setPen(QtGui.QPen(QtCore.Qt.darkRed))
        self.setBrush(QtCore.Qt.red)
        self.setFlag(QtGui.QGraphicsItem.ItemSendsScenePositionChanges)

        if self.style == "default":
            return
        font = self.scene().font()
        if self.style == "italic":
            font.setItalic(True)
        elif self.style == "bold":
            font.setBold(True)
        self._label.setFont(font)
        self.setPath(QtGui.QPainterPath())

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        self._label.setPlainText(name)

    @property
    def is_output(self):
        return self._is_output

    @is_output.setter
    def is_output(self, is_output):
        self._is_output = is_output
        # Adapt label size.
        if is_output:
            self._label.setPos(
                -self.radius_ - self.margin - self._label.boundingRect().width(),
                -self._label.boundingRect().height() / 2)
        else:
            self._label.setPos(self.radius_ + self.margin,
                               -self._label.boundingRect().height() / 2)

    def is_connected(self, other_port):
        for conn in self.connections:
            if conn.port1 == other_port or conn.port2 == other_port:
                return True
        return False

    def remove(self):
        for conn in self.connections:
            conn.remove()
        try:
            self.scene().removeItem(self)
        except AttributeError:
            pass

    def itemChange(self, change, value):
        if change == self.ItemScenePositionHasChanged:
            for conn in self.connections:
                try:
                    conn.update_pos_from_ports()
                    conn.update_path()
                except AttributeError:
                    self.connections.remove(conn)
        return value
