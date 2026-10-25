# OMG Multibeam Survey & Processing Monitor — QGIS Plugin

A **Qimera / CARIS HIPS-style Map & Processing Monitor Plugin for QGIS 3.22+** designed for the UNB Ocean Mapping Group (OMG) multibeam sonar software suite.

---

## Key Features

1. **Zero-Copy Loading of `.r4`, `.sun`, `.8bit`, `.mos`, and `.weight` Rasters (`VRTRawRasterBand`):**
   - Reads the 1024-byte big-endian `JHC_header` (`"OMG1"`, `code/subr/array.h`) directly in Python and generates a lightweight GDAL Virtual Raster (`.vrt`) sidecar (`<ImageOffset>1024</ImageOffset>`, `<ByteOrder>MSB</ByteOrder>`).
   - Opens `.r4` (32-bit float bathymetry), `.sun` (shaded relief), `.8bit` (greyscale depth), and `.mos` (sidescan backscatter mosaic) instantaneously in QGIS **without converting or duplicating data on disk**.
   - Automatically styles `.r4` bathymetric grids with a multi-stop depth pseudocolor ramp.
2. **Qimera / HIPS-Style Survey Line Processing Stage Matrix:**
   - Scans `raw/`, `merged/`, `decnav/`, and `ss/` to track every survey line across all pipeline stages:
     - `Raw (.kmall / .all)` $\rightarrow$ `Water Column (.kmwcd / .watercol)` $\rightarrow$ `Unpacked (.merged)` $\rightarrow$ `Active .nav` $\rightarrow$ `Filtered decnav` $\rightarrow$ `Active .orientation` $\rightarrow$ `SVP (.sv_filtered)` $\rightarrow$ `deTVG` $\rightarrow$ `Sidescan (.ss)`.
   - Renders color-coded survey tracklines on the QGIS Map Canvas categorized by pipeline stage (`COMPLETE`, `BATHY READY`, `UNPACKED`, `RAW ONLY`).
   - Clicking any line in the table zooms the QGIS Map Canvas to that line and displays its `.param` vessel lever-arm offsets and `.sv_filtered` sound velocity cast.
3. **Live File-System Watcher (`QFileSystemWatcher`):**
   - Automatically detects when background unraveling or gridding scripts (`unravel_KMALL_2500m_RevHplus_netatt2_parallel`, `bunravel`, `tor4`, `addSUN`, `tomos`) create or update files on disk and refreshes the table and QGIS layers in real time.
4. **Integrated Command Runner & Interactive `swathed -locate` / `jview` Launcher:**
   - Execute `getBounds`, `make_blank`, `tor4`, `r4to8bit`, `addSUN`, `mos2`, `swathed -locate <grid.r4> merged/*.merged`, and `jview` directly from the QGIS dock panel.

---

## Installation in QGIS (Linux / macOS / Windows)

Symlink or copy the `omg_qgis_plugin` folder into your QGIS 3 Python plugins directory:

```bash
mkdir -p ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins
ln -s /home/iwc/coding/qgis_omg_plugin/omg_qgis_plugin \
      ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/omg_qgis_plugin
```

Then in QGIS:
1. Open **Plugins $\rightarrow$ Manage and Install Plugins... $\rightarrow$ Installed**
2. Check **OMG Multibeam Survey & Processing Monitor**
3. Click the **OMG Multibeam Monitor** toolbar icon (or **Raster $\rightarrow$ OMG Multibeam Monitor**).

---

## Standalone CLI Usage (Outside QGIS / For LocalAI Agent)

You can also use `omg_qgis_cli.py` from the command line to inspect headers, generate `.vrt` sidecars, or scan workspaces:

```bash
# Inspect OMG1 rasters and generate .vrt sidecars:
python3 /home/iwc/coding/qgis_omg_plugin/omg_qgis_cli.py raster --vrt /home/iwc/coding/code/grid/dome.r4 /home/iwc/coding/code/grid/dome.sun_315

# Scan an entire survey workspace directory:
python3 /home/iwc/coding/qgis_omg_plugin/omg_qgis_cli.py scan /path/to/survey_project --geojson tracklines.geojson
```
