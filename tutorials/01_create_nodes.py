# Tutorial 01 — Creating nodes with `jvisu.core.node`
#
# Run this script inside Visual-Environment's Python environment
# (the VE Python console / macro runner), where `VistaDb` is provided.
# Make sure the SDK root (the folder containing `jvisu/`) is on
# sys.path, e.g. run from the SDK folder or add it to PYTHONPATH in VE.
#
# What you will learn:
#   1. How to get the current model and build a `node` helper object.
#   2. How to create nodes (auto id and explicit id).
#   3. How to read a node's id and coordinates back.
#   4. How to create a node between two existing nodes.
#
# All calls used here are taken from jvisu/core/node.py (see docs/node.md).

import VistaDb
from jvisu.core.node import node

# ----------------------------------------------------------------------
# 1. Get the current model and build the helper
# ----------------------------------------------------------------------
# VistaDb.GetCurrentModel() returns the model open in VE right now.
# Every jvisu class takes that model object in its constructor.
vista_model = VistaDb.GetCurrentModel()

nodes = node(vista_model)

# ----------------------------------------------------------------------
# 2. Create four corner nodes of a 10 x 10 square (z = 0)
# ----------------------------------------------------------------------
# node.create(cx, cy, cz, nid=None, show=False) creates one node and
# returns the created node object (a FeNodeClass VistaObject).
# With nid omitted, VE assigns a fresh unique id.
n1 = nodes.create(0.0, 0.0, 0.0)
n2 = nodes.create(10.0, 0.0, 0.0)
n3 = nodes.create(10.0, 10.0, 0.0)
n4 = nodes.create(0.0, 10.0, 0.0)

# The numeric id of a node object comes from VistaDb.GetId().
print("created nodes:", [VistaDb.GetId(n) for n in (n1, n2, n3, n4)])

# ----------------------------------------------------------------------
# 3. Create a node with an explicit id
# ----------------------------------------------------------------------
# Pass nid to choose the id yourself. If that id already exists,
# create() prints "Node number already exists" and returns None.
n5 = nodes.create(5.0, 5.0, 0.0, nid=10001)
print("explicit-id node:", VistaDb.GetId(n5))

# ----------------------------------------------------------------------
# 4. Read coordinates back
# ----------------------------------------------------------------------
# get_coordinate() accepts either a node object or an integer id and
# returns an (x, y, z) tuple.
print("n1 coordinates:", nodes.get_coordinate(n1))
print("n5 coordinates:", nodes.get_coordinate(10001))

# get_object() turns an id back into the node object.
n1_again = nodes.get_object(VistaDb.GetId(n1))
print("same object:", n1_again == n1)

# ----------------------------------------------------------------------
# 5. Create a node halfway between two existing nodes
# ----------------------------------------------------------------------
# between_2nodes(N1, N2) creates the midpoint node and returns it.
# get_mid_2nodes(N1, N2) only computes the midpoint (x, y, z) without
# creating anything.
mid_xyz = nodes.get_mid_2nodes(n1, n3)
print("midpoint of n1-n3:", mid_xyz)

mid_node = nodes.between_2nodes(n1, n3)
print("midpoint node id:", VistaDb.GetId(mid_node),
      "at", nodes.get_coordinate(mid_node))

print("Tutorial 01 done.")
