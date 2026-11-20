# Tutorial 03 — Creating parts with `jvisu.core.part`
#
# Run this script inside Visual-Environment's Python environment
# (the VE Python console / macro runner), where `VistaDb` is provided.
# Make sure the SDK root (the folder containing `jvisu/`) is on
# sys.path, e.g. run from the SDK folder or add it to PYTHONPATH in VE.
#
# What you will learn:
#   1. How to create a material and get its id.
#   2. How to create a shell part with a thickness and a material.
#   3. How to read and change a part's thickness and material.
#   4. How the other part creators (solid, null) differ.
#
# IMPORTANT: unlike node.create() / element.create_*(), which return
# the created OBJECT, part.create_*() return the new part ID (an int).
# All calls used here are taken from jvisu/core/part.py and
# jvisu/core/material.py (see docs/part.md).
#
# NOTE: part.__init__() takes a snapshot of the part list (id -> name)
# at construction time. Parts created AFTER you build the `part`
# helper do not appear in parts.part_list / parts.id_list / parts.name_list.
# Rebuild the helper (part(vista_model)) or use thickness_list() /
# get_part_object_list() when you need a fresh list.

import VistaDb
from jvisu.core.node import node
from jvisu.core.elem import element
from jvisu.core.part import part
from jvisu.core.material import material

# ----------------------------------------------------------------------
# 1. Model and helpers
# ----------------------------------------------------------------------
vista_model = VistaDb.GetCurrentModel()

nodes = node(vista_model)
elems = element(vista_model)
parts = part(vista_model)
mats = material(vista_model)

# ----------------------------------------------------------------------
# 2. Create a material first (parts reference materials by id)
# ----------------------------------------------------------------------
# material.create_mat1(name, mid, rho, e_value, nu) creates a VPS
# material type 1 (elastic-plastic isotropic) and returns the material
# OBJECT. Defaults: rho=7.8e-6, e_value=210, nu=0.3, yield stress 1e30.
# The numeric id comes from VistaDb.GetId(), as with nodes.
mat_obj = mats.create_mat1(name="TUTORIAL_STEEL", rho=7.8e-6,
                           e_value=210, nu=0.3)
mid = VistaDb.GetId(mat_obj)
print("material id:", mid, "name:", mats.get_name(mid))

# ----------------------------------------------------------------------
# 3. Create a shell part with thickness and material
# ----------------------------------------------------------------------
# create_shell_part(pid, thickness, mid, pname, NINT, HCONT)
#   pid       : part id you want, or None for an auto id
#   thickness : shell thickness (sets ShellThickness1)
#   mid       : material id to assign (may be None)
#   pname     : part name (default "PID_<id>")
#   NINT      : through-thickness integration points (default 5)
#   HCONT     : optional (contact) thickness
# Returns the new part ID (int).
pid = parts.create_shell_part(thickness=1.2, mid=mid,
                              pname="TUTORIAL_SHELL")
print("shell part id:", pid)

# ----------------------------------------------------------------------
# 4. Read the part back and verify
# ----------------------------------------------------------------------
print("part name:", parts.get_name(pid))
print("thickness:", parts.get_thickness(pid))   # 1.2
print("material id:", parts.get_material(pid))  # same mid as above
print("section type:", parts.get_type(pid))     # 3 = SHELL (see ATYPE)

# thickness_list() returns {part_id: [name, thickness]} for ALL parts.
print("all parts:", parts.thickness_list())

# ----------------------------------------------------------------------
# 5. Change the thickness afterwards
# ----------------------------------------------------------------------
parts.set_thickness(pid, 2.0)
print("thickness after set_thickness:", parts.get_thickness(pid))

# modify() changes material / thickness / NINT / HCONT in one call.
parts.modify(pid, thickness=1.5)
print("thickness after modify:", parts.get_thickness(pid))

# ----------------------------------------------------------------------
# 6. Put some elements in the part (so it is not empty)
# ----------------------------------------------------------------------
n1 = nodes.create(0.0, 0.0, 0.0)
n2 = nodes.create(10.0, 0.0, 0.0)
n3 = nodes.create(10.0, 10.0, 0.0)
n4 = nodes.create(0.0, 10.0, 0.0)
quad = elems.create_quad([n1, n2, n3, n4], pid)
print("quad in part:", VistaDb.GetId(quad),
      "-> part", elems.get_partid(quad))

# ----------------------------------------------------------------------
# 7. The other part creators (same pid/pname pattern, different section)
# ----------------------------------------------------------------------
# Solid part (3D elements). Same return: the new part id.
pid_solid = parts.create_solid_part(mid=mid, pname="TUTORIAL_SOLID")
print("solid part id:", pid_solid,
      "type:", parts.get_type(pid_solid))       # 5 = SOLID

# Null part (no section property at all — a placeholder / collector).
pid_null = parts.create_null_part(pname="TUTORIAL_NULL")
print("null part id:", pid_null)

print("Tutorial 03 done.")
