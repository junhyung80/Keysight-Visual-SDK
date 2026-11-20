# `jvisu.core.element` — the `element` class

Source: `jvisu/core/elem.py` (937 lines). The module file is `elem.py`;
the class is `element` — import it as
`from jvisu.core.elem import element`. It wraps the `FeElementClass`
objects of the model open in Visual-Environment.


## Construction

```python
import VistaDb
from jvisu.core.elem import element

vista_model = VistaDb.GetCurrentModel()
elems = element(vista_model)
```

`element(model)` stores the model and also builds `self._part`, a
`jvisu.core.part.part` helper for the same model (`elem.py:12-14`),
which `change_pid()` uses to resolve part ids.

## Ids vs. objects

As with `node`, most methods accept an integer element id, an element
object, or a list of either. The private resolver `element.__get(EID)`
(`elem.py:16`) returns the object unchanged when it already is one
(`checkElementClass`, `check.py:11` — a `VistaObject` that is a
subclass of `FeElementClass`), or looks it up by id with
`VistaDb.ModelGetObjectFromId`. `list_check()` (`elem.py:516`) does
the same normalization for lists.

`node_obj_list_check()` (`elem.py:663`) accepts node objects or integer
node ids and returns a list of node objects. Note it builds a **set**
first, so the input order is **not** preserved.

## Methods

| Method | Signature | Description | Source |
|---|---|---|---|
| `__init__` | `element(model=None)` | Store the model; build the internal `part` helper. | `elem.py:12` |
| `create_tria` | `create_tria(node_obj_list, pid, show=False)` | Create a 3-node shell element; returns the element object. | `elem.py:697` |
| `create_quad` | `create_quad(node_obj_list, pid, show=False)` | Create a 4-node shell element (nodes auto-sorted CCW); returns the element object. | `elem.py:683` |
| `create_tetra` | `create_tetra(node_obj_list, pid, show=False)` | Create a 4-node solid (tetra) element via `VMeshMdlr.CreateTetra`; returns the element object. | `elem.py:637` |
| `create_hexa` | `create_hexa(node_obj_list, pid, show=False)` | Create an 8-node solid (hexa) element via `VMeshMdlr.CreateHexa`; returns the element object. | `elem.py:645` |
| `create_penta` | `create_penta(node_obj_list, pid, show=False)` | Create a 6-node solid (penta/wedge) element via `VMeshMdlr.CreatePenta`; returns the element object. | `elem.py:675` |
| `create_bar` | `create_bar(node_obj1, node_obj2, pid)` | **Do not use as shipped** — see warning below. Intended: 2-node bar/beam element. | `elem.py:707` |
| `get_object` | `get_object(EID)` | Element object for an id (or the object itself). | `elem.py:46` |
| `get_partid` | `get_partid(EID)` | Part id of an element. | `elem.py:51` |
| `get_normal` | `get_normal(EID)` | Element normal as a numpy array `[x, y, z]`. | `elem.py:60` |
| `get_nodelist` | `get_nodelist(EID)` | Node ids (ints) of an element. | `elem.py:67` |
| `get_nodelist_of_elements` | `get_nodelist_of_elements(EID)` | Deduplicated node ids of one element (id/object) or a list of them. | `elem.py:296` |
| `get_area` | `get_area(elem_obj)` | Area of a shell element object (quad split into two trias). | `elem.py:84` |
| `get_tria_area` | `get_tria_area(n1, n2, n3)` | Area of a triangle from three `VgPoint3` points. | `elem.py:75` |
| `get_projected_area` | `get_projected_area(elem_obj, axis)` | Area of a shell element projected on a direction `axis`. | `elem.py:123` |
| `get_tria_projected_area` | `get_tria_projected_area(n1, n2, n3, axis)` | Projected area of a triangle from three points. | `elem.py:107` |
| `get_lengths_list` | `get_lengths_list(obj_list)` | Longest edge length per element (numpy array). | `elem.py:163` |
| `get_areas_list` | `get_areas_list(obj_list)` | Area per element (numpy array; tria/quad only). | `elem.py:215` |
| `get_longest_length` | `get_longest_length(elem_obj)` | Longest edge of one element. | `elem.py:287` |
| `get_shortest_length` | `get_shortest_length(elem_obj)` | Shortest edge of one element. | `elem.py:291` |
| `get_volume` | `get_volume(EID)` | Volume of one (solid) element. | `elem.py:332` |
| `get_volume_list` | `get_volume_list(EID)` | Volumes of a list of elements. | `elem.py:337` |
| `cog` | `cog(EID)` | Centre of gravity `[x, y, z]` of one element. | `elem.py:457` |
| `get_elements_cog` | `get_elements_cog(EID)` | **Broken as shipped** — see warning below. | `elem.py:342` |
| `get_cog_array` | `get_cog_array(elist, decimals=5)` | `(eid_list, elem_list, coordinate_array)` of element centres. | `elem.py:723` |
| `get_coordinate_array` | `get_coordinate_array(elist, decimals=5)` | `(nid_list, coordinate_array)` of all nodes of the elements. | `elem.py:763` |
| `get_element_from_part` | `get_element_from_part(plist)` | Element objects of one part (id/object) or a list of parts. | `elem.py:419` |
| `get_element_by_node` | `get_element_by_node(nlist)` | Element **ids** (ints) attached to node(s). `None` when none. | `elem.py:466` |
| `change_pid` | `change_pid(EID, PID)` | Move element(s) to another part. | `elem.py:385` |
| `copy` | `copy(obj)` | Copy quad/tria element(s); the copies are moved to a **new** part; returns the new elements. | `elem.py:358` |
| `delete` | `delete(obj)` | Delete element(s) by object or list. | `elem.py:378` |
| `list_check` | `list_check(mylist)` | Normalize id / object / list input to a list of element objects. | `elem.py:516` |
| `locate` | `locate(eid)` | Select the element(s) in the VE Explorer (Locate). | `elem.py:537` |
| `show` | `show(eid)` | Show the element(s) in the viewer. | `elem.py:546` |
| `hide` | `hide(eid)` | Hide the element(s) in the viewer. | `elem.py:556` |
| `smooth` | `smooth(elem_obj, fix_node=None)` | Quality smoothing (`QualEnhClass`, 10 iterations, feature-line angle 15). | `elem.py:565` |
| `get_boundary_nodes` | `get_boundary_nodes(elem_obj)` | Boundary nodes of the given element(s). | `elem.py:588` |
| `sort_quad_nodes` | `sort_quad_nodes(node_obj_list)` | Sort 4 node objects counter-clockwise around their centroid; returns the sorted node objects. | `elem.py:593` |
| `reverse_split` | `reverse_split(elem_obj1, elem_obj2)` | **Broken as shipped** — see warning below. Intended: flip the shared diagonal of two trias. | `elem.py:251` |
| `get_group` | `get_group(elist)` | Connected element groups (needs the `group_elements` module — not in this SDK, see NOTES.md). | `elem.py:808` |
| `get_group_old` | `get_group_old(elist)` | Connected element groups, pure-Python BFS over shared nodes. | `elem.py:822` |
| `get_quad_internal_angle` | `get_quad_internal_angle(elem_obj)` | Internal angles of a quad (warns and returns `None` otherwise). | `elem.py:866` |
| `get_tria_internal_angle` | `get_tria_internal_angle(elem_obj)` | Internal angles of a tria (warns and returns `None` otherwise). | `elem.py:875` |
| `get_displayed_entities_list` | `get_displayed_entities_list()` | Visible element objects (or `False` when none). | `elem.py:884` |
| `get_displayed_nodes_list` | `get_displayed_nodes_list()` | Node objects of the visible elements (or `False`). | `elem.py:896` |
| `get_displayed_entities_bounding_box` | `get_displayed_entities_bounding_box()` | `[xmin, xmax, ymin, ymax, zmin, zmax]` of the visible elements (or `False`). | `elem.py:915` |

## How the `create_*` methods work

**Shell elements** (`create_tria`, `create_quad`) call
`VistaDb.ModelCreateShellElement(model, n_nodes, node_list, eid,
etype_num, pid)` with a type code from `jvisu/config/type_dict.py:12`
(`ELEMENT_TYPE`: `SHELL3 = 1002`, `SHELL4 = 1000`), then fetch the
created object back by id and return it.

- `create_quad` sorts the four nodes counter-clockwise first
  (`sort_quad_nodes`, `elem.py:593`), so the winding — and therefore
  the normal — is deterministic regardless of input order.
- `create_tria` does **not** sort. Its node list also passes through
  `node_obj_list_check`, which builds a set, so the stored winding
  (and the normal direction) is not guaranteed. Check the result with
  `get_normal()` when the normal matters.

**Solid elements** (`create_tetra`, `create_hexa`, `create_penta`)
call `VMeshMdlr.CreateTetra / CreateHexa / CreatePenta(model, pid,
eid, len(node_list), node_list)` and return the new element. The
expected node counts (4 / 8 / 6) follow from the element type names;
the source performs no count validation, so passing the wrong count is
unverified behaviour — see NOTES.md.

All `create_*` methods take a fresh id from
`VistaDb.ModelGetUniqueId(model, "FeElementClass", 0)`, and show the
new element when `show=True`.

## Caveats (verified from the source)

- **`create_bar` is broken as shipped.** It uses the module-level
  global `vista_model` (`elem.py:711`, `elem.py:718`) instead of
  `self.model`, so it raises `NameError` unless a global of that name
  happens to exist. It also sets the element's `Part` attribute to the
  integer `pid` directly (`elem.py:717`); whether `SetObjectValue`
  accepts an int there is unverified.
- **`reverse_split` is broken as shipped.** It references
  `triangle1` / `triangle2`, names that are never defined
  (`elem.py:269`); the local variables are `e1_list` / `e2_list`.
- **`get_elements_cog` is broken as shipped.** It references the
  undefined global `vistamodel` (`elem.py:348`); it should be
  `self.model`.
- **`get_group` needs `group_elements.element_group_wrap`**, imported
  lazily inside the method (`elem.py:809`). That module is not in the
  repo snapshot or this SDK. Use `get_group_old` instead — it is pure
  Python and needs nothing extra.
- `get_nodelist()` on a missing element id: `__get()` returns `None`
  and the method then reads an unbound local (`node_id_list`),
  raising `UnboundLocalError` (`elem.py:67-74`). Check that the
  element exists first (e.g. via `get_object()`).
