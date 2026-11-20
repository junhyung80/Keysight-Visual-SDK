# ve-jvisu-sdk

A public SDK for **jvisu** — Python classes that wrap ESI
Visual-Environment's (VE) `VistaDb` API for building and editing
finite-element models: create nodes, elements and parts, read them back,
and drive the model from scripts.

The wrapper classes are the author's own code. This SDK ships them as
runnable code, documents how each class works, and adds tutorials that
show the intended usage.

> **Status: live on GitHub.** The full SDK was pushed on 2026-11-20 to
> the public repo
> [junhyung80/Keysight-Visual-SDK](https://github.com/junhyung80/Keysight-Visual-SDK)
> (test files in commit `fd755a96`, the rest in commit `4a68d5fb`).
> Publication still needs the author's IP/licence check for documenting
> an interface to a commercial product (Visual-Environment).

## What is in here

| Path | Contents |
|---|---|
| `jvisu/` | The vendored package — the author's classes (see NOTES.md for the one deliberate removal in `elem.py`). |
| `jvisu/core/node.py` | `node` — create/read/move nodes. |
| `jvisu/core/elem.py` | `element` — create/read shell & solid elements. |
| `jvisu/core/part.py` | `part` — create/read/modify parts (shell, solid, null, tied, plink). |
| `jvisu/core/material.py` | `material` — create/read materials (vendored to support Tutorial 03). |
| `jvisu/core/check.py` | Type-check helpers shared by the classes. |
| `jvisu/config/type_dict.py` | Type-code tables (`ATYPE`, `ELEMENT_TYPE`, material maps, solver codes). |
| `docs/node.md` | `node` API reference (signature, description, source line). |
| `docs/element.md` | `element` API reference. |
| `docs/part.md` | `part` API reference (+ `material.create_mat1`). |
| `tutorials/01_create_nodes.py` | Create nodes, read ids and coordinates back. |
| `tutorials/02_create_elements.py` | Create tria/quad elements, read normal and area back. |
| `tutorials/03_create_parts.py` | Create a material and a shell part, set thickness. |
| `NOTES.md` | Verification notes: what was checked from code, what could not be verified, and known defects found in the vendored code (fixed nowhere — listed verbatim). |

## Prerequisites

These are **not** provided by this SDK and cannot be installed with
pip — they come with Visual-Environment:

- `VistaDb`, `VToolKit`, `VCmd`, `VHostManager`, `VScn`, `VExpMngr`,
  `VMeshMdlr`, `VgPoint3`, and `visualenv` (used lazily by
  `node.copy()` / `on_curve()` / `element.copy()`).

Third-party packages used by the classes:

- `numpy` (used throughout) and `scipy` (`scipy.spatial.cKDTree`,
  used by `node.coincident_nodes()`).

## Running the tutorials

The tutorials run **inside Visual-Environment's Python environment**
(the VE Python console / macro runner), where `VistaDb` and friends
are importable. They do not run in a plain Python interpreter.

1. Open a model in VE (or start from an empty model).
2. Make sure the SDK root — the folder containing `jvisu/` — is on
   `sys.path` (run the script from the SDK folder, or add the folder
   to `PYTHONPATH` in VE).
3. Run the tutorials in order: `01_create_nodes.py`,
   `02_create_elements.py`, `03_create_parts.py`. Each one prints what
   it created, so you can check the result in VE.

The tutorials were written from the actual source code and use only
verified calls, but they have **not** been executed — there was no
live VE session available while building this scaffold. See NOTES.md.

## The basic pattern

Every class follows the same shape:

```python
import VistaDb
from jvisu.core.node import node

vista_model = VistaDb.GetCurrentModel()   # the model open in VE
nodes = node(vista_model)                 # helper bound to the model
node_obj = nodes.create(0.0, 0.0, 0.0)    # returns the node object
node_id = VistaDb.GetId(node_obj)          # its numeric id
```

- `node.create()` / `element.create_*()` return the created
  **object**.
- `part.create_*()` return the new part **id (an int)**.
- Most getters accept an integer id, an object, or a list of either.

## Known gaps

- Several methods in the vendored code contain defects (undefined
  names, globals) that were found while documenting and are listed —
  not fixed — in NOTES.md.

## Scope

First release: `node`, `element`, `part` (plus `material` for the
tutorials). Natural next steps: `group`, `load`, `contact`,
`constraint`, `result`, `curve/plot`, `geometry/cad`.
