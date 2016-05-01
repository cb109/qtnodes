"""Tree layouting algorithm.

This is very hacky and horribly inefficient right now, but it really
helps experimenting with the tool.
"""
from collections import defaultdict

from .node import Node


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


def makeTree(nodes):
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


def assignDepth(tree, currentDepth=0):
    """Depth tells us how deep in a hierarchy a Node belongs."""
    # Make sure to only assign this once, otherwise it may be
    # overwritten for Nodes that theoretically can be seen as being in
    # more than one hierarchy level. Keep the first (and such, lowest).
    if tree.depth == -1:
        tree.depth = currentDepth

    currentDepth += 1
    for child in tree.children:
        assignDepth(child, currentDepth=currentDepth)


def autoLayout(scene):
    """Do a basic hierarchical tree layout of the scene."""
    print("auto layout")
    nodes = [i for i in scene.items() if isinstance(i, Node)]
    if not nodes:
        return

    trees = makeTree(nodes)

    # Arrange hierarchical levels on x-axis.
    withoutParents = [t for t in trees if not t.parents]
    for tree in withoutParents:
        assignDepth(tree, currentDepth=0)

    xMargin = 50
    maxWidth = max([tree.node.w for tree in trees])
    for tree in trees:
        x = tree.depth * (-maxWidth - xMargin)
        print(tree.depth, x, maxWidth)
        tree.node.setPos(x, tree.node.pos().y())

    # Arrange Nodes within each level on the y-axis.
    depth2nodes = defaultdict(list)
    for tree in trees:
        depth2nodes[tree.depth].append(tree.node)

    # We start at the deepest level, at the leafs.
    yMargin = 20
    for depth in reversed(sorted(depth2nodes)):
        nodes = depth2nodes[depth]

        firstNode = nodes[0]  # Anchor node.
        firstNode.setPos(firstNode.pos().x(), 0)

        for i, node in enumerate(nodes):
            predecessor = nodes[i - 1] if i > 0 else None
            if predecessor:
                yOffset = i * (predecessor.h + yMargin)
            else:
                yOffset = i * yMargin
            node.setPos(node.pos().x(),
                        firstNode.pos().y() + yOffset)
