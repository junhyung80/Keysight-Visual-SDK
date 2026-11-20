# `jvisu.core.node` — the `node` class

Source: `jvisu/core/node.py` (818 lines). Wraps the `FeNodeClass` objects of
the model open in Visual-Environment.

## Construction

```python
import VistaDb
from jvisu.core.node import node

vista_model = VistaDb.GetCurrentModel()
nodes = node(vista_model)
```

`node(model)` stores the model and immediately calls `get_bounding_box()`
(`node.py:13-15`), which scans all nodes in the model and sets
`self.xmin / xmax / ymin / ymax / zmin / zmax` (all `None` on an empty
model). Every method below operates on `self.model`.

## Ids vs. objects

Most methods accept **either** an integer node id **or** a node object
(`FeNodeClass` VistaObject), and many accept a list of either. The
private resolver `node.__get(NID)` (`node.py:54`) is what makes this
work:

- `int` → `VistaDb.ModelGetNodeFromID(model, id)`
- node object → id via `VistaDb.GetId()`, then looked up again
- `VgPoint3` point object → used directly as the "object"
- anything else → prints `NID TYPE ERROR`, returns `(None, None)`

The helpers in `jvisu/core/check.py` decide what counts as what:
`checkNodeClass` (`check.py:4`, `VistaObject` whose class is
`FeNodeClass`), `checkPointClass` (`check.py:180`, a `VgPoint3`),
`checkInteger` (`check.py:194`).

## Methods

| Method | Signature | Description | Source |
|---|---|---|---|
| `__init__` | `node(model=None)` | Store the model; compute the bounding box. | `node.py:13` |
| `create` | `create(cx, cy, cz, nid=None, show=False)` | Create one node; returns the new node object (see below). | `node.py:255` |
| `get_object` | `get_object(NID)` | Node object for an id (or the object itself). `None` if missing. | `node.py:166` |
| `get_coordinate` | `get_coordinate(NID)` | `(x, y, z)` tuple for an id or object. `None` if missing. | `node.py:174` |
| `get_point_object` | `get_point_object(NID)` | The `VgPoint3` point of a node. `None` if missing. | `node.py:158` |
| `get_nodes_from_element` | `get_nodes_from_element(elist)` | Node objects of one element (id/object) or a list of them. Order is not guaranteed (built from a set). | `node.py:184` |
| `get_nodes_from_part` | `get_nodes_from_part(plist)` | Node objects of one part (id/object) or a list of them. `None` when the part list is empty. | `node.py:221` |
| `copy` | `copy(obj)` | Copy node(s) via VHostManager Copy/Paste; returns the new node objects. Pass a list. | `node.py:85` |
| `delete` | `delete(obj)` | Delete node(s) by id, object, or list. | `node.py:99` |
| `list_check` | `list_check(mylist)` | Normalize id / object / list input to a list of node objects. | `node.py:107` |
| `locate` | `locate(nid)` | Select the node(s) in the VE Explorer (Locate). | `node.py:128` |
| `show` | `show(nid)` | Show the node(s) in the viewer. | `node.py:139` |
| `hide` | `hide(nid)` | Hide the node(s) in the viewer. | `node.py:149` |
| `cnode_to_node` | `cnode_to_node(NID)` | Convert a constraint node to a regular node (VCmd `ConvertCnodetoNode`). | `node.py:18` |
| `node_to_cnode` | `node_to_cnode(NID)` | Convert a regular node to a constraint node (VCmd `ConvertNodetoCnode`). | `node.py:36` |
| `on_curve` | `on_curve(curve_obj, num=2)` | Create `num` nodes on a curve object (or list of curves); returns the new node objects. | `node.py:284` |
| `between_2nodes` | `between_2nodes(N1, N2)` | Create the midpoint node of two nodes; returns it. | `node.py:317` |
| `get_mid_2nodes` | `get_mid_2nodes(N1, N2)` | Midpoint `(x, y, z)` of two nodes, without creating anything. | `node.py:331` |
| `pair_list` | `pair_list(nlist1, nlist2, tol=0.5)` | For each id in `nlist1`, the nearest node in `nlist2` within `tol`; returns `[[id, nearest_obj], ...]`. | `node.py:342` |
| `get_boundary_nodes` | `get_boundary_nodes(elem_obj)` | Boundary nodes of the given element(s). | `node.py:351` |
| `drop_nodes_on_curve` | `drop_nodes_on_curve(node_obj, curve_obj)` | Move node(s) onto curve(s) along the target normal. | `node.py:356` |
| `projection_on_plane_normal` | `projection_on_plane_normal(node_list, plane_x, plane_y, plane_z, d_constant)` | Project node(s) onto a plane along the plane normal, then refresh the display. | `node.py:371` |
| `projection_on_plane_vector` | `projection_on_plane_vector(node_list, plane_x, plane_y, plane_z, d_constant, vect_n1, vect_n2)` | Project node(s) onto a plane along a user vector (defined by two node objects). | `node.py:392` |
| `get_nearest_node` | `get_nearest_node(nodes, chkpoint)` | Node object nearest to `chkpoint`. Returns `(None, None)` on empty input (see NOTES.md). | `node.py:422` |
| `sort_nodes_by_distance` | `sort_nodes_by_distance(nlist, base)` | Greedily order nodes by nearest-neighbour distance from `base`. Mutates the input list. | `node.py:441` |
| `delete_free_node` | `delete_free_node()` | Delete unattached (loose) nodes via the VE `UnAttachedElements` command. | `node.py:455` |
| `coincident_nodes` | `coincident_nodes(node_obj_list, base_parts, move_parts)` | Snap `move_parts` nodes onto coincident `base_parts` nodes (KD-tree). See warning below. | `node.py:463` |
| `all_coordinate_list` | `all_coordinate_list()` | `[[x, y, z], ...]` for every node in the model. | `node.py:490` |
| `get_bounding_box` | `get_bounding_box()` | Sets `self.xmin/xmax/...`; returns `(xmin, xmax, ymin, ymax, zmin, zmax)`, or `False` on an empty model. | `node.py:496` |
| `get_bbox_corner_nodes` | `get_bbox_corner_nodes(tol=1e-6)` | The 8 nodes closest to the bounding-box corners. | `node.py:516` |
| `node_refresh` | `node_refresh()` | Refresh the display of all parts (`UpdateDisplayOfGivenParts` + `ModelDraw`). | `node.py:554` |
| `node_coordinate_modify` | `node_coordinate_modify(node_id_list, final_point_list)` | Set node coordinates from `VgPoint3` objects or `(x, y, z)` tuples, then refresh. | `node.py:559` |
| `get_nodes_by_user_box` | `get_nodes_by_user_box(cog, pid_list, vector, length, depth=5.0, shape="box")` | **BROKEN as shipped** — see warning below. Intended: node ids inside a box/cylinder section volume. | `node.py:571` |

## How `create()` works (`node.py:255-282`)

```python
node_obj = nodes.create(0.0, 0.0, 0.0)            # auto id
node_obj = nodes.create(5.0, 5.0, 0.0, nid=10001)  # explicit id
```

1. With `nid` given, the code first checks whether that id already
   exists (`VistaDb.ModelGetObjectFromId`). If it does, it raises
   `Node number already exists`; the exception is caught, printed, and
   `create()` returns `None`.
2. Otherwise (or with `nid` omitted) it takes a fresh id from
   `VistaDb.ModelGetUniqueId(model, "FeNodeClass", 0)` and creates the
   node with `VistaDb.ModelCreateNode(model, NID, cx, cy, cz)`.
3. It calls `VToolKit.UpdateRanges(model, 1, [create_node])` so VE
   refreshes its ranges, shows the node if `show=True`, and returns
   the created node object.

The numeric id of the returned object is `VistaDb.GetId(node_obj)`.

## Caveats (verified from the source)

- **`get_nodes_by_user_box` is broken as shipped.** Its body
  references `nodes_list`, a name that does not exist in that scope
  (`node.py:781`; the local variable is `node_obj_list`), so calling
  it raises `NameError`. Its docstring (a full box/cylinder
  specification with examples) still describes the intended behaviour.
  Do not use it until that line is fixed. See NOTES.md.
- **`coincident_nodes` uses a module-level global** `vista_model`
  (`node.py:465-466`) instead of `self.model`. It only works if a
  global named `vista_model` happens to exist in the calling scope.
- **`get_nearest_node` has an inconsistent return**: `(None, None)` on
  empty input, but a single node object on success (`node.py:422-440`).
- **`sort_nodes_by_distance` mutates its input list** (it pops items
  while sorting, `node.py:441-453`).
- **`copy` / `on_curve` depend on VE's `visualenv` package**
  (`from visualenv.dbs.model.FindNewObjects import FindNewObjects`,
  imported lazily inside the methods). That module is provided by VE,
  not by this SDK.
- `node.create()` returns `None` (and prints the error) on failure
  instead of raising.
