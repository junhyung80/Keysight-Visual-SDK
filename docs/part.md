# `jvisu.core.part` — the `part` class

Source: `jvisu/core/part.py` (709 lines). Wraps the `FePartClass`
objects of the model open in Visual-Environment.

> **The one thing to remember:** unlike `node.create()` and
> `element.create_*()`, which return the created **object**, every
> `part.create_*()` method returns the new part **ID (an int)**.
> Pass that id to the other methods (or to `element.create_*()` as
> `pid`).

## Construction

```python
import VistaDb
from jvisu.core.part import part

vista_model = VistaDb.GetCurrentModel()
parts = part(vista_model)
```

`part(model)` stores the model and takes a **snapshot** of the part
list: `self.part_list` (`{id: name}`), `self.name_list`,
`self.id_list` (`part.py:13-17`). Parts created *after* construction
do not appear in those attributes — rebuild the helper
(`part(vista_model)`) or use `thickness_list()` /
`get_part_object_list()` when you need a fresh list.

`get_object(PID)` (`part.py:20`) accepts an integer id or a part
object (`checkPartClass`, `check.py:28`) and returns the part object
(`None`, with a printed message, when the id does not exist).

## Methods

| Method | Signature | Description | Source |
|---|---|---|---|
| `__init__` | `part(model=None)` | Store the model; snapshot the part list (id → name). | `part.py:13` |
| `create_shell_part` | `create_shell_part(pid=None, thickness=None, mid=None, pname=None, NINT=None, HCONT=None)` | Create a shell part; returns the new part id (int). | `part.py:210` |
| `create_solid_part` | `create_solid_part(pid=None, mid=None, pname=None, HCONT=None)` | Create a solid part; returns the new part id (int). | `part.py:309` |
| `create_null_part` | `create_null_part(pid=None, pname=None)` | Create a part with no section property; returns the new part id (int). | `part.py:175` |
| `create_tied_part` | `create_tied_part(pid=None, rdist=None, mid=None, pname=None)` | Create a tied-contact part; returns the new part id (int). | `part.py:264` |
| `create_plink_part` | `create_plink_part(pid=None, mid=None, pname=None, RSEAR=None, NLAYR=None, NGESP=None, SPOTRA=None)` | Create a spotweld (plink) part; returns the new part id (int). | `part.py:354` |
| `modify` | `modify(pid, mid=None, thickness=None, NINT=None, HCONT=None)` | Change material / thickness / integration points / HCONT of a part. | `part.py:407` |
| `get_object` | `get_object(PID)` | Part object for an id (or the object itself). | `part.py:20` |
| `get_name` | `get_name(PID)` | Part name. | `part.py:82` |
| `set_name` | `set_name(PID, NAME)` | Rename a part. | `part.py:99` |
| `get_material` | `get_material(pid)` | Material id assigned to a part. | `part.py:424` |
| `set_material` | `set_material(pid, mid)` | Assign a material (by id) to a part. See warning below. | `part.py:431` |
| `get_thickness` | `get_thickness(pid)` | Shell thickness (`ShellThickness1`). | `part.py:440` |
| `set_thickness` | `set_thickness(pid, thickness)` | Set the shell thickness. | `part.py:447` |
| `thickness_list` | `thickness_list()` | `{part_id: [name, thickness]}` for **all** parts (fresh query). | `part.py:115` |
| `get_type` | `get_type(pid)` | Section type code (see ATYPE below). | `part.py:454` |
| `get_hcont` | `get_hcont(pid)` | Optional (contact) thickness of a part. | `part.py:462` |
| `set_hcont` | `set_hcont(pid, opt_thickness)` | Set the optional (contact) thickness. | `part.py:471` |
| `get_part_object_list` | `get_part_object_list(partlist=None)` | `(count, [part objects])` — all parts, or the given ids. | `part.py:130` |
| `cog` | `cog(plist)` | Centre of gravity `[x, y, z]` of the nodes of part(s). | `part.py:45` |
| `get_bounding_box_cg` | `get_bounding_box_cg(plist)` | Centre `[x, y, z]` of a part's bounding box. | `part.py:564` |
| `get_bounding_box_coordinate` | `get_bounding_box_coordinate(plist)` | `[xmin, xmax, ymin, ymax, zmin, zmax]` of a part. | `part.py:576` |
| `get_cog_array` | `get_cog_array(plist, decimals=5)` | `(eid_list, ele_list, coordinate_array)` of the elements' centres. | `part.py:591` |
| `get_node_object_list` | `get_node_object_list(plist)` | Node objects of part(s). | `part.py:627` |
| `get_coordinate_array` | `get_coordinate_array(plist, decimals=5)` | `(nid_list, coordinate_array)` of a part's nodes. | `part.py:634` |
| `list_check` | `list_check(mylist)` | Normalize id / object / list input to a list of part objects. | `part.py:478` |
| `locate` | `locate(pid)` | Select the part(s) in the VE Explorer (Locate). | `part.py:498` |
| `hide` | `hide(pid)` | Hide the part(s) in the viewer. | `part.py:509` |
| `show` | `show(pid)` | Show the part(s) in the viewer. | `part.py:520` |
| `set_color` | `set_color(PID, cvalue=None)` | Set the part colour (`"r g b"`); random colour when omitted. | `part.py:531` |
| `get_color` | `get_color(PID)` | Part colour. | `part.py:558` |
| `delete` | `delete(plist, solver_type=2)` | Delete part(s). `solver_type` 2 = VPS (default); 0 = LS-DYNA, 1 = NASTRAN, 3 = ABAQUS. | `part.py:671` |
| `get_displayed_part_id_list` | `get_displayed_part_id_list()` | Ids of the displayed parts (or `False` when none). | `part.py:704` |

## How the `create_*` methods work

All five creators share the same id logic (`part.py:175-405`):

1. With `pid` given: if no part with that id exists, the new id is
   taken from `VistaDb.ModelGetUniqueId(model, "FePartClass", pid)`;
   if it already exists, the code raises `Part number already
   exists`, catches it, prints it, and returns `None`.
2. With `pid` omitted: `ModelGetUniqueId(model, "FePartClass", 0)`.
3. A `FePartClass` object is created, given a colour (`set_color`,
   random when no value is passed) and the id, and named `pname`
   (default `"PID_<id>"`).

Then each kind adds its section (a `FeSectionClass` object attached
as the part's `Property`), with the section `Type` taken from
`jvisu/config/type_dict.py:1` (`ATYPE`):

| Creator | Section `Type` | Extra parameters |
|---|---|---|
| `create_shell_part` | `SHELL` = 3 | `thickness` → `ShellThickness1`; `IntegrationPoints` defaults to 5, overridden by `NINT`; `mid` → `set_material`; `HCONT` → `set_hcont` |
| `create_solid_part` | `SOLID` = 5 | `mid` → `set_material`; `HCONT` → `set_hcont` |
| `create_null_part` | *(no section at all)* | — |
| `create_tied_part` | `TIED` = 57 | `rdist` → extended attribute `RDIST`; `mid` → `set_material` |
| `create_plink_part` | `PLINK` = 54 | `RSEAR` (double), `NLAYR` (int), `NGESP` (int), `SPOTRA` (double) as extended attributes; `mid` → `set_material` |

Every creator finishes with `VExpMngr.RefreshExplorer("Parts")` and
returns the new part id.

## Materials (companion module)

`set_material(pid, mid)` needs a material id. The vendored
`jvisu/core/material.py` provides it; the one verified here is:

| Method | Signature | Description | Source |
|---|---|---|---|
| `create_mat1` | `create_mat1(name=None, mid=None, rho=7.8e-6, e_value=210, nu=0.3)` | Create a VPS material type 1 and return the material **object**. Shear/bulk moduli are computed from `e_value`/`nu`; yield stress is set to `1e30`. | `material.py:158` |
| `get_object` | `get_object(mid)` | Material object for an id. | `material.py:17` |
| `get_name` | `get_name(mid)` | Material name. | `material.py:131` |

Per `jvisu/config/type_dict.py:50` (`vps_mater_type`), VPS material
type 1 maps to `FeMatEPIsotropicClass` (class id 3109, type 13). Get
the id with `VistaDb.GetId(mat_obj)` and pass it as `mid` to
`create_shell_part` / `set_material`. The other creators in
`material.py` (`create_mat16/100/101/117/200/301/302`, `material.py:186`
onwards) are vendored but not documented here yet — same pattern,
different VPS material types.

## Caveats (verified from the source)

- **`set_material` has a bug on its error path.** When the material id
  does not exist, the error message formats an undefined name `MID`
  (`part.py:438`) instead of `mid`, so the call raises `NameError`
  rather than printing the message. Only assign materials that exist
  (or check with `material.get_object(mid)` first).
- **`get_material` on a part with no material assigned** calls
  `VistaDb.GetId(None)` (`part.py:424-428`); the behaviour in that
  case is unverified — see NOTES.md.
- **`get_thickness` reads `ShellThickness1`** from the part's section
  (`part.py:440-445`). On a part whose section has no such value
  (e.g. a null or solid part) the return is unverified.
- **`create_shell_part` / `create_solid_part` pass the part *object***
  (not the id) to `set_hcont` (`part.py:256`, `part.py:348`); that
  works because `set_hcont` resolves its argument through
  `get_object`, which accepts objects. (They pass the new id to
  `set_material`: `part.py:253`, `part.py:345`.)
- `delete()`'s `solver_type` codes come from `type_dict.py:147-150`
  (`solver_lsdyna = 0`, `solver_nastran = 1`, `solver_vps = 2`,
  `solver_abaqus = 3`).
