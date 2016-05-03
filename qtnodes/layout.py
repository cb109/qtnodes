"""Automatic tree layouting."""
import os
import re

from .node import Node

# Need to have graphviz installed (its bin/ must be on PATH).
import pydot
import appdirs


class Tree(object):
    """A wrapper for each Node, solely for layouting purposes."""

    def __init__(self, node):
        self.node = node
        self.parents = []
        self.children = []

        self.depth = -1
        self.position = 0
        self.w = self.node.w
        self.h = self.node.h


def _getNodesFromScene(scene):
    """Return all Node items of the given QGraphicsScene."""
    nodes = [i for i in scene.items() if isinstance(i, Node)]
    return nodes


def _makeTree(nodes):
    """Return a list of Trees that represent the Node hierarchy."""
    node2tree = {}
    for node in nodes:
        node2tree[node] = Tree(node)

    for node, tree in node2tree.items():
        for knob in node.knobs():
            for edge in knob.edges:
                sourceNode = edge.source.node()
                targetNode = edge.target.node()

                if node == sourceNode:
                    targetTree = node2tree[targetNode]
                    if targetTree not in tree.parents:
                        tree.parents.append(targetTree)

                if node == targetNode:
                    sourceTree = node2tree[sourceNode]
                    if sourceTree not in tree.children:
                        tree.children.append(sourceTree)

    trees = node2tree.values()
    return trees


def autoLayout(scene):
    """Tree layout using graphviz.

    Code based on this example: https://gist.github.com/dbr/1255776
    """
    print("auto layout")

    nodes = _getNodesFromScene(scene)
    if not nodes:
        return

    trees = _makeTree(nodes)

    class Dotter(object):
        """Walk the Tree hierarchy and write it to a .dot file."""

        delim = "_"

        def __init__(self):
            self.graph = pydot.Dot(graph_type="digraph", rankdir="LR")
            self.checked = []
            self.counter = 0

        def nodeToName(self, node):
            # FIXME: Using <classname>_<n-digit-uuid> has a chance
            #   of name clashes which gets higher the more nodes we
            #   have. We should use the full uuid as identifier, but
            #   make sure graphviz does not use it as the node width
            #   when doing its layouting. Right now that would result
            #   in graphs that are very far spaced out.
            return (node.header.text + self.delim + node.uuid[:4])

        def recursiveGrapher(self, tree, level=0):
            self.counter += 1

            if tree in self.checked:
                # Don't redo parts of tree already checked.
                return

            self.checked.append(tree)

            for childTree in tree.children:
                childName = self.nodeToName(childTree.node)
                parentName = self.nodeToName(tree.node)
                edge = pydot.Edge(childName, parentName)
                self.graph.add_edge(edge)
                print ("{0} Recursing into {1}".format(
                       level, childName))
                self.recursiveGrapher(childTree, level=level + 1)

        def save(self, filePath):
            """Writing the graph to file will apply graphviz' layouting."""
            # TODO: We can use 'dot' or 'neato', however 'neato'
            #   currently produces pretty bad results (probably related
            #   to .Dot() settings above, may be worth looking into it.)
            self.graph.write_dot(filePath, prog="dot")

    def assignDotResultToNodes(dotFile, nodes):
        """Read positions from file and apply them."""

        # TODO: Use pydot's pydot_parser.py instead.
        # Extract the node name and its x and y position.
        pattern = r"(?P<name>[\"]{0,1}[a-zA-Z0-9_-]+[\"]{0,1})\s*\[\w+\=(?:\d+(?:\.\d+){0,1})\,\s*pos\=\"(?P<x>\d+(?:\.\d+){0,1})\,(?P<y>\d+(?:\.\d+){0,1})"  # noqa

        with open(dotFile) as f:
            text = f.read()

        name2node = {}
        for node in nodes:
            name = dotter.nodeToName(node)
            name2node[name] = node

        matches = re.findall(pattern, text)
        for name, x, y in matches:
            node = name2node[name]
            node.setPos(float(x), float(y))

    dataDir = os.path.join(appdirs.user_data_dir(), "qtnodes")
    try:
        os.makedirs(dataDir)
    except OSError:
        if not os.path.isdir(dataDir):
            raise
    dotFile = os.path.join(dataDir, "last_layout.dot")
    print("writing layout to", dotFile)

    dotter = Dotter()
    for tree in trees:
        dotter.recursiveGrapher(tree)

    dotter.save(dotFile)
    assignDotResultToNodes(dotFile, nodes)
