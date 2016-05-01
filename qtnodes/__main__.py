"""Manual tests."""

from PySide import QtGui

from .knob import InputKnob, OutputKnob
from .header import Header
from .node import Node
from .widget import NodeGraphWidget


class Integer(Node):

    def __init__(self, *args, **kwargs):
        super(Integer, self).__init__(*args, **kwargs)
        self.addHeader(Header(node=self, text="Int"))
        self.addKnob(OutputKnob(labelText="value"))


class Multiply(Node):

    def __init__(self, *args, **kwargs):
        super(Multiply, self).__init__(*args, **kwargs)
        self.addHeader(Header(node=self, text="Multiply"))
        self.addKnob(InputKnob(labelText="x"))
        self.addKnob(InputKnob(labelText="y"))
        self.addKnob(OutputKnob(labelText="value"))


class Output(Node):

    def __init__(self, *args, **kwargs):
        super(Output, self).__init__(*args, **kwargs)
        self.addHeader(Header(node=self, text="Output"))
        self.addKnob(InputKnob(labelText="output"))


class BigNode(Node):

    def __init__(self, *args, **kwargs):
        super(BigNode, self).__init__(*args, **kwargs)
        self.addHeader(Header(node=self, text="BigNode"))
        self.addKnob(InputKnob(labelText="i1"))
        self.addKnob(OutputKnob(labelText="o1"))
        self.addKnob(InputKnob(labelText="i2"))
        self.addKnob(OutputKnob(labelText="o2"))
        self.addKnob(InputKnob(labelText="i3"))
        self.addKnob(OutputKnob(labelText="o3"))
        self.addKnob(InputKnob(labelText="i4"))
        self.addKnob(OutputKnob(labelText="o4"))
        self.addKnob(InputKnob(labelText="i5"))
        self.addKnob(OutputKnob(labelText="o5"))
        self.addKnob(InputKnob(labelText="i6"))
        self.addKnob(OutputKnob(labelText="o6"))
        self.addKnob(InputKnob(labelText="i7"))
        self.addKnob(OutputKnob(labelText="o7"))
        self.addKnob(InputKnob(labelText="i8"))
        self.addKnob(OutputKnob(labelText="o8"))
        self.addKnob(InputKnob(labelText="i9"))
        self.addKnob(OutputKnob(labelText="o9"))


class Directory(Node):

    def __init__(self, *args, **kwargs):
        text = kwargs.pop("text")
        super(Directory, self).__init__(*args, **kwargs)
        self.addHeader(Header(node=self, text=text))
        self.addKnob(InputKnob(labelText="parent"))
        self.addKnob(OutputKnob(labelText="children"))


class File(Node):

    def __init__(self, *args, **kwargs):
        text = kwargs.pop("text")
        super(File, self).__init__(*args, **kwargs)
        self.addHeader(Header(node=self, text=text))
        self.addKnob(InputKnob(labelText="parent"))


def test():
    app = QtGui.QApplication([])

    graph = NodeGraphWidget()
    graph.setGeometry(100, 100, 800, 600)
    graph.show()

    # d1 = Directory(scene=graph.scene, text="root")
    # d2 = Directory(scene=graph.scene, text="opt")
    # d3 = Directory(scene=graph.scene, text="rengo")
    # d4 = Directory(scene=graph.scene, text=".venvs")
    # d5 = Directory(scene=graph.scene, text="rengo")
    # d6 = Directory(scene=graph.scene, text="rengo01")
    # d7 = Directory(scene=graph.scene, text="bin")
    # d8 = File(scene=graph.scene, text="activate")

    # d2.moveBy(100, 0)
    # d3.moveBy(200, 0)
    # d4.moveBy(200, 70)
    # d5.moveBy(300, 70)
    # d6.moveBy(300, 0)
    # d7.moveBy(400, 70)
    # d8.moveBy(500, 70)

    # d1.knob("children").connectTo(d2.knob("parent"))
    # d2.knob("children").connectTo(d3.knob("parent"))
    # d2.knob("children").connectTo(d4.knob("parent"))
    # d4.knob("children").connectTo(d5.knob("parent"))
    # d3.knob("children").connectTo(d6.knob("parent"))
    # d5.knob("children").connectTo(d7.knob("parent"))
    # d7.knob("children").connectTo(d8.knob("parent"))

    nodeInt1 = Integer(scene=graph.scene)
    nodeInt2 = Integer(scene=graph.scene)
    nodeMult = Multiply(scene=graph.scene)
    nodeOut = Output(scene=graph.scene)
    nodeBig = BigNode(scene=graph.scene)

    nodeInt2.moveBy(100, 250)
    nodeMult.moveBy(200, 100)
    nodeBig.moveBy(300, 50)
    nodeOut.moveBy(400, 150)

    nodeInt1.knob("value").connectTo(nodeMult.knob("x"))
    nodeInt2.knob("value").connectTo(nodeMult.knob("y"))

    nodeMult.knob("value").connectTo(nodeBig.knob("i1"))
    nodeMult.knob("value").connectTo(nodeBig.knob("i2"))
    nodeMult.knob("value").connectTo(nodeBig.knob("i3"))
    nodeMult.knob("value").connectTo(nodeBig.knob("i4"))
    nodeMult.knob("value").connectTo(nodeBig.knob("i5"))
    nodeMult.knob("value").connectTo(nodeBig.knob("i6"))
    nodeMult.knob("value").connectTo(nodeBig.knob("i7"))
    nodeMult.knob("value").connectTo(nodeBig.knob("i8"))
    nodeMult.knob("value").connectTo(nodeBig.knob("i9"))

    nodeBig.knob("o1").connectTo(nodeOut.knob("output"))
    nodeBig.knob("o2").connectTo(nodeOut.knob("output"))
    nodeBig.knob("o3").connectTo(nodeOut.knob("output"))
    nodeBig.knob("o4").connectTo(nodeOut.knob("output"))
    nodeBig.knob("o5").connectTo(nodeOut.knob("output"))
    nodeBig.knob("o6").connectTo(nodeOut.knob("output"))
    nodeBig.knob("o7").connectTo(nodeOut.knob("output"))
    nodeBig.knob("o8").connectTo(nodeOut.knob("output"))
    nodeBig.knob("o9").connectTo(nodeOut.knob("output"))

    app.exec_()


if __name__ == '__main__':
    test()


"""
todos

- that should hopefully enable us to use RubberBandDrag together with
  creating edges from a knob
- attach data to nodes and let them modify it
- save/load a graph to/from json

"""