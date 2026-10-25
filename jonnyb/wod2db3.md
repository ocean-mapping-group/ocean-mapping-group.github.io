---
layout: default
title: wod2db3
parent: Jonathan Beaudoin — SVP, Refraction & Snippets (jonnyb)
grand_parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 5
tool_name: wod2db3
source_path: code/jonnyb/wod/wod2db3.c
category: Oceanographic Climatology & Databases (jonnyb)
input_formats:
- NOAA WOD native ASCII/gzipped files (ctdo*, xbt*, etc.)
output_formats:
- .db3 (SQLite3 database)
- .csv
related_tools:
- soundscape
- convertWOA01
- svp_woa01
---

# wod2db3

## Description
`wod2db3` (`code/jonnyb/wod/wod2db3.c`) parses up to 5,000 native NOAA World Ocean Database (`WOD`) cast files (including `.gz` compressed archives via `wod_open_file` in `code/jonnyb/subr/wod.c`) and builds either a SQLite3 database (`wod.db3`, table `tbl1`) or a comma-separated ASCII catalog (`wod.csv`).

Instead of duplicating every depth-temperature-salinity sample inside the database, `wod2db3` indexes each cast's metadata (`instrument`, `observed`, `quadrant`, `wmo_lat`, `wmo_lon`, `latitude`, `longitude`, `year`, `month`, `day`) together with its exact byte offset (`file_offset`) and byte length (`num_bytes`) in the source WOD file, enabling instant spatial/temporal SQL queries and direct random-access cast retrieval in [`soundscape`](soundscape.html).

---

## Usage

```bash
wod2db3 [-v] [-debug_wod] [-csv] [-out <output.db3|output.csv>] <wod_file1 ...>
```

### Examples

**1. Build a SQLite3 index database from WOD CTD files:**

```bash
wod2db3 -out arctic_wod.db3 ctd/obs/ctdo*.gz
```

**2. Export WOD cast metadata and byte offsets to CSV:**

```bash
wod2db3 -csv -out arctic_wod.csv ctd/obs/ctdo*.gz
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `<wod_files ...>` | Up to 5,000 NOAA WOD cast files (`MAX_NUM_INFILES = 5000`). | Required |
| `-out <filename>` | Output filename for the SQLite3 database or CSV file. | `wod.db3` (or `wod.csv` if `-csv`) |
| `-csv` | Write comma-separated ASCII records instead of a SQLite3 `.db3` database. | SQLite3 `.db3` |
| `-debug_wod` | Enable verbose WOD parser debugging (`wod_reader.debug = 1`). | Disabled |
| `-v` | Enable verbose output. | Disabled |

---

## Database Schema (`tbl1`)

When creating a SQLite3 database, `wod2db3` executes:

```sql
CREATE TABLE tbl1 (
    instrument integer,
    observed integer,
    quadrant integer,
    wmo_lat integer,
    wmo_lon integer,
    latitude real,
    longitude real,
    year integer,
    month integer,
    day integer,
    file_offset integer,
    num_bytes integer
);
```
