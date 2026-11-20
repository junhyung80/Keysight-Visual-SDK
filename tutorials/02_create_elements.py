# Tutorial 02 — Creating elements with `jvisu.core.element`
#
# Run this script inside Visual-Environment's Python environment
# (the VE Python console / macro runner), where `VistaDb` is provided.
# Make sure the SDK root (the folder containing `jvisu/`) is on
# sys.path, e.g. run from the SDK folder or add it to PYTHONPATH in VE.
#
# What you will learn:
#   1. How to create tria and quad shell elements from nodes.
#   2. How to read an element's node list, normal and area back.
#   3. How to find which part an element belongs to.
#
# Elements always belong to a part, so this tutorial first creates a
# shell part (see Tutorial 03 for the full part story).
# All calls used here are taken from jvisu/core/elem.py (see
# docs/element.md). `create_bar` is intentionally NOT used here: the
# shipped implementation references a module-level global `vista_model`
# (elem.py:779-794), so it fails unless that global happens to exist.
# See NOTES.md.

import VistaDb
from jvisu.core.node import node
from jvisu.core.elem import element
from jvisu.core.part import part

# ----------------------------------------------------------------------
# 1. Model, helpers, and a shell part to hold the elements
# ----------------------------------------------------------------------
vista_model = VistaDb.GetCurrentModel()

nodes = node(vista_model)
elems = element(vista_model)
parts = part(vista_model)

# create_shell_part() returns the new part ID (an int, not an object).
pid = parts.create_shell_part(thickness=1.0, pname="TUTORIAL_SHELL")
print("shell part id:", pid)

# ----------------------------------------------------------------------
# 2. Create the nodes first
# ----------------------------------------------------------------------
# A quad needs 4 nodes, a tria needs 3. The node objects returned by
# node.create() can be passed straight into the element creators.
n1 = nodes.create(0.0, 0.0, 0.0)
n2 = nodes.create(10.0, 0.0, 0.0)
n3 = nodes.create(10.0, 10.0, 0.0)
n4 = nodes.create(0.0, 10.0, 0.0)
n5 = nodes.create(20.0, 0.0, 0.0)
n6 = nodes.create(20.0, 10.0, 0.0)

# ----------------------------------------------------------------------
# 3. Create a quad and a tria
# ----------------------------------------------------------------------
# create_quad(node_obj_list, pid, show=False) builds a 4-node shell
# element. It sorts the four nodes counter-clockwise by itself, so the
# order you pass them in does not matter.
# create_tria(node_obj_list, pid, show=False) builds a 3-node shell
# element. NOTE: unlike create_quad it does not sort the nodes, and the
# node list passes through a set internally, so the winding (and hence
# the normal direction) of a tria is not guaranteed — check it with
# get_normal() if the normal matters to you.
quad = elems.create_quad([n1, n2, n3, n4], pid)
tria = elems.create_tria([n2, n5, n6], pid)
# A second tria sharing the quad's edge, to complete the 20 x 10 plate.
tria2 = elems.create_tria([n2, n6, n3], pid)

print("quad id:", VistaDb.GetId(quad))
print("tria ids:", VistaDb.GetId(tria), VistaDb.GetId(tria2))

# ----------------------------------------------------------------------
# 4. Read element data back
# ----------------------------------------------------------------------
# get_nodelist() accepts an element object or an element id and returns
# the node ids (ints) of the element, in the order stored in VE.
print("quad node ids:", elems.get_nodelist(quad))
print("tria node ids:", elems.get_nodelist(VistaDb.GetId(tria)))

# get_normal() returns the element normal as a numpy array [x, y, z].
print("quad normal:", elems.get_normal(quad))

# get_area() takes the element OBJECT (not an id) and returns its area.
# The quad is 10 x 10, so the area is 100.
print("quad area:", elems.get_area(quad))
print("tria area:", elems.get_area(tria))

# get_partid() returns the id of the part the element belongs to.
print("quad part id:", elems.get_partid(quad))

# get_object() turns an element id back into the element object.
quad_again = elems.get_object(VistaDb.GetId(quad))
print("same object:", quad_again == quad)

print("Tutorial 02 done.")
