# Documentation & Mapping Roadmap

This document serves as the bridge between the C source code and the public documentation for the ocean mapping project. It tracks our progress in ensuring that all core technologies are accurately represented on the website.

## 1. Core Inventory (Source Code Map)
The following maps every identified source file and utility to its corresponding role in the ecosystem:

### Core Engine (`glSeis` & `hydro_core`)
These files manage the main rendering engine, viewport interaction, and data management systems.
- **Core Logic**: `glseis/glSeis.c`, `glseis/doTS`, `glseis/do_5m`, `glseis/do_15m`, `glseis/do30m`
- **View & Geometry**: `glseis/SEIS_watercolumn.h`, `glseis/SEIS_watercolumn.c`, `glseis/SEIS_oGL_draw.h`, `glseis/SEIS_oGL_draw.c`
- **Lifecycle**: `glseis/SEIS_launcher.c`, `glseis/SEIS_initialise.c`

### Mapping & Representation (`cmaps`)
These files manage the transformation of raw data into displayable values (color, depth).
- **Core Logic**: `cmaps/CnCcolorMap.c`, `cmaps/CnCcolorMapV.c`
- **Definitions**: Included in associated `.h` headers for color scaling and palette rotation.

### Pipelines & Utility Tools (`labs` & `bin`)
These tools provide the "missing links" between raw data files and active visualization.
- **Pre-processing**: `labs/mkbp.c`, `labs/mkbp_skeleton.c` (Batch Processing)
- **Data Extraction**: `labs/EM_unpack.c`, `labs/EM_unpack`
- **Utilities**: `bin/xv`, and various conversion scripts in the root tree.

## 2. Documentation Gap Analysis
The following table tracks our requirements for the `ocean-mapping-group.github.io` site:

| Program / Module | Current Doc Status | Primary Function | Target Output |
| :--- | :--- | :--- | :--- |
| **glSeis Core** | Partial / Basic | Render Engine & Navigation | "View Guide" |
| **cmaps Suite** | Missing Deep-Dive | Color Mapping Logic | "Data Transformation" |
| **mkbp/EM_unpack** | Not Documented | Data Preparation & Extraction | "Automation Pipeline" |
| **Shell Tools** | Not Documented | Execution convenience scripts | "Quick Start Guide" |

## 3. Implementation Roadmap (Phased Construction)
We will generate new `.md` files in the `ocean-mapping-group.github.io/` directory to match the existing layout.

### Phase 1: The Viewport (Current Target)
**Focus:** `glSeis` and primary interaction scripts.
**Goal:** Detailed documentation of how users navigate, select layers, and interact with the core viewer.

### Phase 2: Data Translation Logic
**Focus:** `cmaps`.
**Goal:** Document the math behind color-mapping and how it interprets different survey types.

### Phase 3: The Processing Pipeline
**Focus:** `mkbp`, `EM_unpack` & `lab` tools.
**Goal:** Technical documentation for developers on preparing data before it is rendered by the engine.

---
*Last updated during Discovery Mapping sequence.*