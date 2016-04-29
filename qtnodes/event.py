from PySide import QtCore


class EventMixin(QtCore.QObject):
    """Hold custom signals that can be emitted by the editor."""

    mouse_pressed = QtCore.Signal(QtCore.QEvent)
    mouse_released = QtCore.Signal(QtCore.QEvent)
    mouse_moved = QtCore.Signal(QtCore.QEvent)

    # created = QtCore.Signal()
    # removed = QtCore.Signal()
    # hovered = QtCore.Signal()

    port_added = QtCore.Signal(QtCore.QEvent)
    port_connected = QtCore.Signal(QtCore.QEvent)
    port_disconnected = QtCore.Signal(QtCore.QEvent)
