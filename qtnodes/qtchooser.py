import sys

try:
    import PySide2
    from PySide2 import QtGui, QtWidgets, QtCore
    from PySide2.QtCore import Signal, Slot
    print('Using PySide2 bindings')
except:

    try:
        import PyQt5
        from PyQt5 import QtGui, QtWidgets, QtCore
        from PyQt5.QtCore import pyqtSignal as Signal, pyqtSlot as Slot
        print('Using PyQt5 bindings')
    except:
        raise Exception('No Qt bindings found! Install PySide2 or PyQt5')
