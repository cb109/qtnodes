"""Serialization and deserialization of the graph."""

import uuid
import re

from .node import Node
from .edge import Edge
from .helpers import fromJson, toJson, readFileContent
from .exceptions import UnregisteredNodeClassError


def serializeEdge(edge):
    """Return the Edge as native Python datatypes, fit for json.

    Edges only reference Knobs, so we have to store their Node id here
    to be able to correctly associate it once reconstructed.
    """
    return {
        "source_nodeId": edge.source.node().uuid,
        "source_name": edge.source.name,

        "target_nodeId": edge.target.node().uuid,
        "target_name": edge.target.name,
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
        try:
            cls = classMap[nodeData["class"]]
        except KeyError as err:
            raise UnregisteredNodeClassError(err)

        node = cls()
        node.uuid = nodeData["uuid"]  # Enforce 'original' uuid.
        node.setPos(nodeData["x"], nodeData["y"])

        graphWidget.addNode(node)

    # Reconstruct their connections.
    for edgeData in sceneData["edges"]:
        sourceNode = graphWidget.getNodeById(edgeData["source_nodeId"])
        sourceKnob = sourceNode.knob(edgeData["source_name"])

        targetNode = graphWidget.getNodeById(edgeData["target_nodeId"])
        targetKnob = targetNode.knob(edgeData["target_name"])

        sourceKnob.connectTo(targetKnob)


def saveSceneToFile(sceneData, jsonFile):
    """Store the serialized scene as .json file."""
    with open(jsonFile, "w") as f:
        f.write(toJson(sceneData) + "\n")


def _renewUUIDs(jsonString):
    """Renew uuids in given text, by doing complete string replacements
    with newly generated uuids.

    Return the resulting text.
    """
    RE_UUID = r"(?P<uuid>\w{8}-\w{4}-\w{4}-\w{4}-\w{12})"
    matches = re.findall(RE_UUID, jsonString)
    uuids = list(set(matches))
    for original in uuids:
        replacement = str(uuid.uuid4())
        jsonString = jsonString.replace(original, replacement)
    return jsonString


def loadSceneFromFile(jsonFile, refreshIds=False):
    """Read the serialized scene data from a .json file.

    refreshIds: If True, ensures all uuids are renewed (on a text
        basis), meaning they will not overwrite existing scene content.
        This can be used to 'merge' a file into an existing scene.
    """
    text = readFileContent(jsonFile)
    if refreshIds:
        text = _renewUUIDs(text)
    sceneData = fromJson(text)
    return sceneData


def mergeSceneFromFile(jsonFile):
    """Like loading, but with new uuids, so it can be merged."""
    return loadSceneFromFile(jsonFile, refreshIds=True)
