"""Run this in 3ds Max:

    python.executeFile @"thisfile.py"

"""

import sys
sys.path.insert(0, r"C:\dev\qtnodes")


import MaxPlus

from qtnodes import (Header, Node, InputKnob,
                     OutputKnob, NodeGraphWidget)


class MaxObject(Node):

    def __init__(self, name):
        super(MaxObject, self).__init__()
        self.addHeader(Header(node=self, text=name))
        self.addKnob(InputKnob(labelText="children"))
        self.addKnob(OutputKnob(labelText="parent"))


def createObject(graph, node, parent=None):
    obj = MaxObject(node.Name)
    graph.addNode(obj)
    if parent:
        obj.knob("parent").connectTo(parent.knob("children"))

    for c in node.Children:
        createObject(graph, c, parent=obj)


if __name__ == '__main__':
    graph = NodeGraphWidget()
    graph.registerNodeClass(MaxObject)

    rootNode = MaxPlus.Core.GetRootNode()
    createObject(graph, rootNode)

    graph.show()


