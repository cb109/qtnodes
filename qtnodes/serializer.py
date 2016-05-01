"""Serialization and deserialization of the graph."""

import os
import json

from .node import Node
from .edge import Edge


def serializeEdge(edge):
    """Return the Edge as native Python datatypes, fit for json.

    Edges only reference Knobs, so we have to store their Node id here
    to be able to correctly associate it once reconstructed.
    """
    return {
        "knob1_nodeId": edge.knob1.node().uuid,
        "knob1_labelText": edge.knob1.labelText,

        "knob2_nodeId": edge.knob2.node().uuid,
        "knob2_labelText": edge.knob2.labelText,
    }


def serializeNode(node):
    """Return the Node as native Python datatypes, fit for json."""
    return {
        "class": node.__class__.__name__,
        "uuid": node.uuid,
        "x": node.scenePos().x(),
        "y": node.scenePos().y(),
    }


def serializeScene(scene):
    """Very naive scene serialization.

    Returns the scene as native Python datatypes, fit for json.

    We only store what Nodes there are, their positions and how they are
    connected by Edges. This should be enough to reconstruct the graph
    by relying on the other default values in each Node class.

    I repeat: If specific node/knob/header settings like flow, colors or
    labels have been changed, that is not (yet) stored here!
    """
    nodes = [i for i in scene.items() if isinstance(i, Node)]
    edges = [i for i in scene.items() if isinstance(i, Edge)]
    data = {
        "nodes": [serializeNode(node) for node in nodes],
        "edges": [serializeEdge(edge) for edge in edges]
    }
    return data


def reconstructScene(graphWidget, sceneData):
    """Rebuild a scene based on the serialized data.

    This reconstructs only type, position and connections right now.
    """
    # Node classes need to be registered beforehand.
    classMap = {}
    for cls in graphWidget.nodeClasses:
        classMap[cls.__name__] = cls

    # Reconstruct Nodes.
    for nodeData in sceneData["nodes"]:
        cls = classMap[nodeData["class"]]

        node = cls()
        node.uuid = nodeData["uuid"]  # Enforce 'original' uuid.
        node.setPos(nodeData["x"], nodeData["y"])

        graphWidget.addNode(node)

    # Reconstruct their connections.
    for edgeData in sceneData["edges"]:
        node1 = graphWidget.getNodeById(edgeData["knob1_nodeId"])
        knob1 = node1.knob(edgeData["knob1_labelText"])

        node2 = graphWidget.getNodeById(edgeData["knob2_nodeId"])
        knob2 = node2.knob(edgeData["knob2_labelText"])

        knob1.connectTo(knob2)


def toJson(serialized):
    """Return JSON string from given native Python datatypes."""
    return json.dumps(serialized, encoding="utf-8", indent=4)


def fromJson(jsonString):
    """Return native Python datatypes from JSON string."""
    return json.loads(jsonString, encoding="utf-8")


def saveSceneToFile(sceneData, jsonFile):
    """Store the serialized scene as .json file."""
    with open(jsonFile, "w") as f:
        f.write(toJson(sceneData) + "\n")


def loadSceneFromFile(jsonFile):
    """Read the serialized scene data from a .json file."""
    with open(jsonFile) as f:
        sceneData = fromJson(f.read())
    return sceneData
