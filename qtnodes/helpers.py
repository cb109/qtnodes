"""Various helper functions."""

import json

from .qtchooser import QtCore, QtGui, QtWidgets

def readFileContent(filePath):
    """Return the content of the file."""
    with open(filePath) as f:
        return f.read()


def toJson(serialized):
    """Return JSON string from given native Python datatypes."""
    return json.dumps(serialized, indent=4)


def fromJson(jsonString):
    """Return native Python datatypes from JSON string."""
    return json.loads(jsonString)


def getTextSize(text, painter=None):
    """Return a QSize based on given string.

    If no painter is supplied, the font metrics are based on a default
    QPainter, which may be off depending on the font und text size used.
    """
    if not painter:
        metrics = QtGui.QFontMetrics(QtGui.QFont())
    else:
        metrics = painter.fontMetrics()
    size = metrics.size(QtCore.Qt.TextSingleLine, text)
    return size
