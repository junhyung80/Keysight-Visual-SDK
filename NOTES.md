# NOTES — verification, gaps, and known defects

How this SDK was built, what was checked against the source, what
could **not** be verified, and the defects found in the vendored code.
Nothing in the "Known defects" section was fixed: the vendored files
are byte-identical copies of the originals (verified with `cmp`), except
`core/elem.py`, from which two methods were deliberately removed before
publication (the file is otherwise unchanged), so the defects are listed
here instead.

## Sources

Single source of truth: the `VE_MCP` repo snapshot at
`~/workspace/ve_mcp/work/repo/` (checked 2026-11-20), specifically:

- `jvisu/core/node.py` (818 lines), `jvisu/core/elem.py` (937 lines),
  `jvisu/core/part.py` (709 lines) — the documented classes
- `jvisu/core/check.py` (216 lines), `jvisu/config/type_dict.py`
  (176 lines) — their import closure
- `jvisu/core/material.py` (439 lines) — vendored to support
  Tutorial 03 (`create_mat1`, `create_object`, `get_object`,
  `get_name` read and verified; the remaining creators were not
  individually reviewed)
- `scripts/ve_commands.py` (usage: `VistaDb.GetCurrentModel()` at
  lines 87, 105, 276) and `scripts/vista_adapter.py` (usage patterns
  for reading parts / creating shell elements) — context only

## What was verified

- Every method signature, parameter name and return value in
  `docs/node.md`, `docs/element.md` and `docs/part.md` was read from
  the method body in the source file (not from names alone). Line
  numbers in the docs refer to the vendored files. For `node.py`,
  `part.py`, `check.py`, `material.py` and `type_dict.py` the vendored
  copies are byte-identical to the originals, so the numbers match the
  originals too; `elem.py` numbers refer to the vendored copy.
- The node tutorial pattern (`VistaDb.GetCurrentModel()` →
  `node(vista_model)` → `nodes.create(...)` → `VistaDb.GetId(...)`)
  matches the code: `node.__init__(model)` (`node.py:13`),
  `node.create(cx, cy, cz, nid=None, show=False)` (`node.py:255`,
  returns the created node object), `VistaDb.GetId` used across
  `jvisu` and `ve_commands.py`.
- The vendored files are byte-identical to the sources (checked with
  `cmp` on 2026-11-20): `core/node.py`, `core/part.py`,
  `core/check.py`, `core/material.py`, `config/type_dict.py`.
  `core/elem.py` is identical except for the deliberate removal noted
  above.
- The tutorial scripts pass `python3 -m py_compile` (syntax only —
  see "not verified" below).

## What could NOT be verified (no live VE session)

- **The tutorials were never executed.** There is no
  Visual-Environment on this machine, so `VistaDb`, `VToolKit`,
  `VCmd`, `VHostManager`, `VScn`, `VExpMngr`, `VMeshMdlr`, `VgPoint3`
  and `visualenv` cannot be imported here. Every tutorial call was
  checked against the source code, but runtime behaviour (including
  whether VE accepts the exact call sequences) is unverified.
- Return types/values of `VistaDb` calls are documented as the code
  treats them (e.g. `ModelGetUniqueId` returning an int id,
  `ElementGetData` returning `(elem_id, part_id, num_nodes,
  node_id_list)`). They were not confirmed against VE documentation.
- The exact steps to run a script in VE (console vs. macro runner,
  menu path, `sys.path` handling) are **not** documented here — the
  author should confirm and fill them in.
- `create_tetra` / `create_hexa` / `create_penta` node counts (4 / 8 /
  6) are conventions from the element type names and the
  `VMeshMdlr.Create*` calls. The source performs no count validation,
  so the behaviour for a wrong count is unverified.
- `element.create_bar` sets the element's `Part` attribute to the
  integer `pid` directly (`elem.py:717`); whether `SetObjectValue`
  accepts an int there (rather than a part object) is unverified.
- `part.get_material()` on a part with no material assigned calls
  `VistaDb.GetId(None)` (`part.py:424-428`); the behaviour is
  unverified.
- `part.get_thickness()` reads `ShellThickness1` from the section
  (`part.py:440-445`); the return for a part whose section has no such
  value (null / solid part) is unverified.
- `element.sort_quad_nodes()` claims counter-clockwise order; the
  orientation is relative to a normal estimated from the first three
  input nodes and was not verified geometrically.
- `material.create_mat1`'s mapping (VPS type 1 →
  `FeMatEPIsotropicClass`, type 13) is traced from
  `vps_mater_type[1] = (3109, 13)` and
  `vista_mater_class_name[3109]` in `type_dict.py`; the physical
  meaning of that mapping was not checked against VE documentation.

## Known defects in the vendored code (found while documenting)

These are in the author's original files. They are **not** fixed in
the vendored copies. Fix them upstream and re-vendor.

1. **`node.get_nodes_by_user_box` — undefined name.** `node.py:781`
   builds `coordinate_list` from `nodes_list`, which does not exist
   in that scope (the local variable is `node_obj_list`). Calling the
   method raises `NameError`. Its docstring still describes the
   intended box/cylinder behaviour.
2. **`element.reverse_split` — undefined names.** `elem.py:269` uses
   `triangle1` / `triangle2`; the locals are `e1_list` / `e2_list`
   (and `e1_set` / `e2_set`). Raises `NameError`.
3. **`element.get_elements_cog` — undefined global.** `elem.py:348`
   calls `VistaDb.ModelGetObjectFromId(vistamodel, ...)`; the global
   `vistamodel` does not exist (should be `self.model`). Raises
   `NameError`.
4. **`element.create_bar` — undefined global.** `elem.py:711` and
   `elem.py:718` use the module-level global `vista_model` instead of
   `self.model`. Raises `NameError` unless such a global happens to
   exist in the calling scope. Tutorial 02 deliberately does not use
   it.
5. **`node.coincident_nodes` — undefined global.** `node.py:465-466`
   use the global `vista_model` instead of `self.model`. Same failure
   mode as (4).
6. **`part.set_material` — undefined name on the error path.**
   `part.py:438` formats the message with `MID`, but the parameter is
   `mid`. When the material id does not exist, the call raises
   `NameError` instead of printing the message.
7. **`element.get_group` — missing lazy import.** `elem.py:809`
   imports `group_elements.element_group_wrap`, which is not in the
   repo. Use `get_group_old` (`elem.py:822`, pure Python) instead.
8. **`node.get_nearest_node` — inconsistent return.**
    `node.py:422-440` returns `(None, None)` on empty input but a
    single node object on success.
9. **`element.get_nodelist` — unbound local on a missing element.**
    When `__get()` returns `None`, `node_id_list` is never assigned
    and the final `return node_id_list` (`elem.py:67-74`) raises
    `UnboundLocalError`.
10. **`node.delete` — error path.** If `list_check()` fails it prints
    `type error` and returns `None`; the `else` branch of `delete()`
    (`node.py:99-106`) then calls `list(None)`, raising `TypeError`.
11. **`node._to_xyz` helper calls undefined `as_xyz`** (`node.py:677`).
    Harmless in practice: the call sits in `try/except` and falls
    through to the `hasattr(p, "x")` check.
12. **`element.copy` moves the copies to a new part.** `elem.py:358-377`
    creates a fresh part id and moves all copied elements into it.
    This is the shipped behaviour, not a bug — but it surprises anyone
    expecting an in-place copy.

## Packaging notes

- The original repo has **no `__init__.py` files** anywhere under
  `jvisu/` (it relies on namespace packages inside VE). The vendored
  copy adds empty `jvisu/__init__.py`, `jvisu/core/__init__.py` and
  `jvisu/config/__init__.py` so the package imports as a regular
  package outside VE. These are the only files that differ from the
  original, apart from `core/elem.py` (two methods deliberately removed —
  see above); all other vendored files are byte-identical.
- `material.py` is vendored although `node`/`elem`/`part` do not
  import it: Tutorial 03 needs a real material id, and creating one
  through `material.create_mat1` is the verified way to get it. Its
  own import closure (`check.py`, `type_dict.py`) is already vendored.
- VE-provided modules are **not** vendored: `VistaDb`, `VToolKit`,
  `VCmd`, `VHostManager`, `VScn`, `VExpMngr`, `VMeshMdlr`, `VgPoint3`,
  `visualenv`. `icode3` is not included either. `numpy` and `scipy`
  are third-party dependencies, not vendored.
