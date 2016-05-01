qtnodes
~~~~~~~

Node-graph visualization and editing with PySide.

Very WIP right now, the goal is to have a bunch of premade components that make it easy to implement a node graph to store and modify arbitrary data.

Usage
-----

To start a small demo:

    $ python -m qtnodes

Scene
=====

- **Pan the viewport**: Hold the middle mousebutton and drag.
- **Zoom the viewport**: Use the mouse wheel.
- **Hold scene state:** Rightclick > Scene > Hold
- **Fetch scene state:** Rightclick > Scene > Fetch

Nodes
=====

- **Select a node**: Leftclick its header.
- **Select multiple nodes**: Leftclick and drag a rectangle over the nodes, release to select.
- **Create a node**: Rightclick > Nodes, choose a node type.
- **Move a node**: Leftclick and drag its header.
- **Delete a node**: Select it then press ``DELETE``.
- **Create a connection**: Hover over a knob, then leftclick and drag to another knob. You can only connect inputs to outputs and vice versa.
- **Remove a connection**: Hold ``ALT``, the connections turn red, click one to remove it.

Credits
-------

This started as a port of the original Qt/C++ tool ``qnodeseditor`` by Stanislaw Adaszewski, see:
http://algoholic.eu/qnodeseditor-qt-nodesports-based-data-processing-flow-editor/

Additional sources and inspirations:

- http://austinjbaker.com/node-editor-prototype
- http://nukengine.com/blog/category/all/qt-node-editor/
- http://blog.interfacevision.com/design/design-visual-progarmming-languages-snapshots/
- https://github.com/Tillsten/qt-dataflow