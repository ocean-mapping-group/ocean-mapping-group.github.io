---
layout: default
title: Tool Finder & Cheat Sheet
nav_order: 3
---

# Interactive Tool Finder & Command-Line Cheat Sheet

Use the interactive filter below to find the exact OMG executable for your file format (`.kmall`, `.kmwcd`, `.all`, `.merged`, `.r4`, `.sun`, `.decnav`, `.ss`, `.vert_prof`, `.s7k`, `.000`, `.raw`, `.sgy`, `.jsf`, `.xtf`) or processing stage, or jump down to the copy-paste command recipes.

---

## Interactive Tool & Format Explorer

<div style="background: #1e293b; border: 1px solid #334155; border-radius: 8px; padding: 1rem; margin-bottom: 1.25rem;">
  <div style="display: flex; flex-wrap: wrap; gap: 0.75rem; margin-bottom: 0.75rem;">
    <input id="omg-tool-search" type="text" placeholder="Search by tool name, file extension (.kmall, .r4, .decnav), or task..." style="flex: 1; min-width: 240px; padding: 0.55rem 0.85rem; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: #f8fafc; font-size: 0.9rem;">
    <select id="omg-stage-filter" style="padding: 0.55rem 0.85rem; border-radius: 6px; border: 1px solid #475569; background: #0f172a; color: #f8fafc; font-size: 0.9rem;">
      <option value="">All Pipeline Stages</option>
      <option value="Unpacking">1. Raw Unpacking (.kmall / .all / Vendor)</option>
      <option value="Nav & Attitude">2. Navigation, Attitude & Latency</option>
      <option value="Ray-Tracing & Tide">3. Ray-Tracing, Refraction & Tide</option>
      <option value="Backscatter & WC">4. Sidescan (.ss) & Water Column (.vert_prof)</option>
      <option value="Gridding & Mosaicking">5. Gridding (.r4/.sun) & Mosaicking (.mos)</option>
      <option value="Editing & Visualization">6. Interactive Editing, 3D Viewers & QGIS</option>
      <option value="ADCP, EK & Sub-Bottom">7. ADCP, EK60/80 & Sub-Bottom</option>
    </select>
  </div>
  <div style="display: flex; flex-wrap: wrap; gap: 0.35rem; align-items: center; font-size: 0.78rem; color: #94a3b8;">
    <span>Quick Format Filter:</span>
    <button type="button" class="omg-ext-btn omg-badge" data-ext="">All</button>
    <button type="button" class="omg-ext-btn omg-badge omg-badge-in" data-ext=".kmall">.kmall / .kmwcd</button>
    <button type="button" class="omg-ext-btn omg-badge omg-badge-in" data-ext=".all">.all / .wcd</button>
    <button type="button" class="omg-ext-btn omg-badge omg-badge-out" data-ext=".merged">.merged</button>
    <button type="button" class="omg-ext-btn omg-badge omg-badge-in" data-ext=".decnav">.nav / .decnav</button>
    <button type="button" class="omg-ext-btn omg-badge omg-badge-in" data-ext=".orientation">.orientation / .net_att</button>
    <button type="button" class="omg-ext-btn omg-badge omg-badge-out" data-ext=".r4">.r4 / .sun</button>
    <button type="button" class="omg-ext-btn omg-badge omg-badge-out" data-ext=".ss">.ss / .mos</button>
    <button type="button" class="omg-ext-btn omg-badge omg-badge-out" data-ext=".vert_prof">.watercol / .vert_prof</button>
    <button type="button" class="omg-ext-btn omg-badge" data-ext=".s7k">.s7k / .r2s / .gsf</button>
    <button type="button" class="omg-ext-btn omg-badge" data-ext="ADCP">ADCP / EK60 / SEG-Y</button>
  </div>
</div>

<table id="omg-tool-table">
  <thead>
    <tr>
      <th>Tool</th>
      <th>Pipeline Stage</th>
      <th>Inputs</th>
      <th>Outputs</th>
      <th>Primary Purpose &amp; Example Flag</th>
    </tr>
  </thead>
  <tbody>
    <tr data-stage="Unpacking" data-ext=".kmall .kmwcd .merged .nav_1 .net_att_2 .watercol .param">
      <td><a href="kmall/read_kmall.html"><code>read_kmall</code></a></td>
      <td>Unpacking</td>
      <td><code>.kmall</code>, <code>.kmwcd</code></td>
      <td><code>.merged</code>, <code>.nav_1..3</code>, <code>.net_att_1..2</code>, <code>.watercol</code>, <code>.param</code>, <code>.svp_*</code></td>
      <td>Unpack Kongsberg Rev D–J <code>.kmall</code> bathymetry/snippets and <code>.kmwcd</code> water column (use <code>-just_wc</code> for <code>.kmwcd</code>).</td>
    </tr>
    <tr data-stage="Unpacking" data-ext=".kmall .kmwcd .merged .watercol">
      <td><a href="omg/moveOverWCinfo.html"><code>moveOverWCinfo</code></a></td>
      <td>Unpacking</td>
      <td><code>&lt;line&gt;.merged</code>, <code>justWC_&lt;line&gt;.merged</code></td>
      <td><code>&lt;line&gt;.merged</code> (updated)</td>
      <td>Transfer water-column byte offsets from an unpacked <code>.kmwcd</code>/<code>.wcd</code> header into the bathymetric <code>.merged</code> file.</td>
    </tr>
    <tr data-stage="Unpacking" data-ext=".all .wcd .merged .nav .orientation .param">
      <td><a href="omg/unravel_em3000.html"><code>unravel</code></a></td>
      <td>Unpacking</td>
      <td><code>.all</code>, <code>.wcd</code></td>
      <td><code>.merged</code>, <code>.nav</code>, <code>.orientation</code>, <code>.param</code>, <code>.sv</code></td>
      <td>Unpack legacy Kongsberg Simrad <code>.all</code> and <code>.wcd</code> datagrams (EM120, EM300, EM302, EM710, EM2040, EM3000).</td>
    </tr>
    <tr data-stage="Nav & Attitude" data-ext=".nav .decnav">
      <td><a href="nav/stripNav.html"><code>stripNav</code></a></td>
      <td>Nav &amp; Attitude</td>
      <td><code>.nav</code></td>
      <td><code>.nav.strip</code></td>
      <td>Remove duplicate timestamps, zero coordinates, and speed-jump spikes (<code>stripNav in.nav out.nav.strip 30.0</code>).</td>
    </tr>
    <tr data-stage="Nav & Attitude" data-ext=".nav .merged">
      <td><a href="omg/mergeNav.html"><code>mergeNav</code></a></td>
      <td>Nav &amp; Attitude</td>
      <td><code>.merged</code>, <code>.nav</code></td>
      <td><code>.merged</code> (updated)</td>
      <td>Interpolate 48-byte binary <code>.nav</code> positions onto every ping timestamp in a <code>.merged</code> swath file.</td>
    </tr>
    <tr data-stage="Nav & Attitude" data-ext=".nav .decnav">
      <td><a href="nav/appendNav.html"><code>appendNav</code></a></td>
      <td>Nav &amp; Attitude</td>
      <td><code>.nav</code></td>
      <td><code>.decnav</code></td>
      <td>Concatenate and decimate binary navigation (e.g., <code>appendNav -skip 10 -comp decnav/74/line.decnav merged/74/line.nav</code>).</td>
    </tr>
    <tr data-stage="Ray-Tracing & Tide" data-ext=".merged .orientation .net_att .param">
      <td><a href="omg/mergeAtt.html"><code>mergeAtt</code></a></td>
      <td>Ray-Tracing &amp; Tide</td>
      <td><code>.merged</code>, <code>.orientation</code>, <code>.param</code>, <code>.sv_filtered</code></td>
      <td><code>.merged</code> (ray-traced)</td>
      <td>Apply lever arms (<code>.param</code>), high-rate attitude (<code>-big_att</code>), and 3D beam ray-tracing (<code>-kmall -recalc_trans -saved_surface_arc</code>).</td>
    </tr>
    <tr data-stage="Ray-Tracing & Tide" data-ext=".merged .orientation .net_att .param">
      <td><a href="omg/newMergeAtt.html"><code>newMergeAtt</code></a></td>
      <td>Ray-Tracing &amp; Tide</td>
      <td><code>.merged</code>, <code>.orientation</code>, <code>.param</code>, <code>.sv_filtered</code></td>
      <td><code>.merged</code> (ray-traced)</td>
      <td>Next-generation attitude merger &amp; full 3D cone-cone Snell's Law ray-tracer for multi-sector Kongsberg systems.</td>
    </tr>
    <tr data-stage="Ray-Tracing & Tide" data-ext=".merged .tide">
      <td><a href="tide/tidemerge.html"><code>tidemerge</code></a></td>
      <td>Ray-Tracing &amp; Tide</td>
      <td><code>.merged</code>, ASCII tide file</td>
      <td><code>.merged</code> (tide-reduced)</td>
      <td>Interpolate observed or predicted water levels onto ping timestamps in <code>.merged</code> files.</td>
    </tr>
    <tr data-stage="Backscatter & WC" data-ext=".merged .ss">
      <td><a href="omg/makess.html"><code>makess</code></a></td>
      <td>Backscatter &amp; WC</td>
      <td><code>.merged</code>, <code>.merged.ss_data</code></td>
      <td><code>.ss</code></td>
      <td>Construct a slant-range-corrected GLORIA/OMG sidescan time series (<code>makess -Redo_as_new -use_beam_ang line.merged</code>).</td>
    </tr>
    <tr data-stage="Backscatter & WC" data-ext=".ss">
      <td><a href="omg/deTVG.html"><code>deTVG</code></a></td>
      <td>Backscatter &amp; WC</td>
      <td><code>.ss</code></td>
      <td><code>.ss</code> (normalized)</td>
      <td>Empirically remove residual grazing-angle Time-Varying Gain (TVG) drop-off across the swath (<code>deTVG -box line.ss</code>).</td>
    </tr>
    <tr data-stage="Backscatter & WC" data-ext=".merged .watercol .vert_prof">
      <td><a href="omg/makeWC.html"><code>makeWC</code></a></td>
      <td>Backscatter &amp; WC</td>
      <td><code>.merged</code>, <code>.watercol</code></td>
      <td><code>.vert_prof</code></td>
      <td>Extract a nadir vertical water-column profile curtain raster (<code>OMG1</code> 8-bit) via <code>makeWC -vert_prof line.merged</code>.</td>
    </tr>
    <tr data-stage="Nav & Attitude" data-ext=".merged .file_bounds">
      <td><a href="omg/getBounds.html"><code>getBounds</code></a></td>
      <td>Nav &amp; Attitude</td>
      <td><code>.merged</code></td>
      <td><code>.file_bounds</code>, <code>.100ping_bounds</code>, <code>shpFiles/</code></td>
      <td>Compute geographic bounding boxes and 100-ping coverage polygons (<code>getBounds -100 line.merged</code>).</td>
    </tr>
    <tr data-stage="Gridding & Mosaicking" data-ext=".merged .r4 .8bit .weight">
      <td><a href="grid/weigh_grid.html"><code>weigh_grid</code></a></td>
      <td>Gridding &amp; Mosaicking</td>
      <td><code>.merged</code> list</td>
      <td><code>.r4</code>, <code>.8bit</code>, <code>.weight</code>, <code>.ran</code></td>
      <td>Distance-weighted bathymetric gridding into 32-bit float <code>.r4</code> and 8-bit <code>.8bit</code> rasters (<code>-utmn</code>/<code>-utms</code>, <code>-res</code>).</td>
    </tr>
    <tr data-stage="Gridding & Mosaicking" data-ext=".r4 .sun">
      <td><a href="grid/meds_sun.html"><code>meds_sun</code></a></td>
      <td>Gridding &amp; Mosaicking</td>
      <td><code>.r4</code></td>
      <td><code>.sun</code></td>
      <td>Compute an 8-bit artificial sun-illuminated hillshade raster from a <code>.r4</code> DEM (<code>meds_sun -azi 315 -elev 45 -exag 3</code>).</td>
    </tr>
    <tr data-stage="Gridding & Mosaicking" data-ext=".ss .r4 .mos">
      <td><a href="newmos/mos2.html"><code>mos2</code></a> / <a href="newmos/comboMOS.html"><code>comboMOS</code></a></td>
      <td>Gridding &amp; Mosaicking</td>
      <td><code>.ss</code>, <code>.nav</code>, <code>.r4</code></td>
      <td><code>.mos</code>, <code>.ran</code></td>
      <td>Range-buffered sidescan backscatter mosaicking draped over a <code>.r4</code> bathymetric surface.</td>
    </tr>
    <tr data-stage="Gridding & Mosaicking" data-ext=".r4 .sun">
      <td><a href="grid/r4toESRI.html"><code>r4toESRI</code></a> / <a href="grid/r4toTIFF.html"><code>r4toTIFF</code></a></td>
      <td>Gridding &amp; Mosaicking</td>
      <td><code>.r4</code>, <code>.sun</code></td>
      <td><code>.asc</code>, <code>.flt</code>, <code>.tif</code></td>
      <td>Export OMG <code>.r4</code> and <code>.sun</code> rasters to ESRI ArcGrid or GeoTIFF for external GIS packages.</td>
    </tr>
    <tr data-stage="Editing & Visualization" data-ext=".merged .r4 .sun .watercol">
      <td><a href="SE/swathed.html"><code>swathed</code></a></td>
      <td>Editing &amp; Visualization</td>
      <td><code>.merged</code>, <code>.r4</code>, <code>.sun</code></td>
      <td>Edited <code>.merged</code> flags</td>
      <td>Interactive 6-panel X11/Motif swath sounding editor, patch test calibrator (<code>CALWIN</code>), and water-column inspector.</td>
    </tr>
    <tr data-stage="Editing & Visualization" data-ext=".r4 .sun .8bit .mos .vert_prof">
      <td><a href="JV/jview.html"><code>jview</code></a></td>
      <td>Editing &amp; Visualization</td>
      <td><code>.r4</code>, <code>.sun</code>, <code>.8bit</code>, <code>.mos</code>, <code>.vert_prof</code></td>
      <td>Interactive 2D/3D display</td>
      <td>Interactive 2D/3D OpenGL/X11 raster viewer, profiler, 2D FFT filter, and interactive SVP editor.</td>
    </tr>
    <tr data-stage="Editing & Visualization" data-ext=".r4 .sun .decnav .merged .vert_prof">
      <td><a href="qgis_plugin/"><code>omg_qgis_cli.py</code></a></td>
      <td>Editing &amp; Visualization</td>
      <td><code>.decnav</code>, <code>.merged</code>, <code>.r4</code>, <code>.sun</code>, <code>.vert_prof</code></td>
      <td><code>.vrt</code>, <code>.geojson</code></td>
      <td>Zero-copy GDAL VRT raster wrapper and Qimera-style survey line QC monitor for QGIS 3.x.</td>
    </tr>
    <tr data-stage="Unpacking" data-ext=".s7k .r2s .gsf .merged">
      <td><a href="reson/7k2omg.html"><code>7k2omg</code></a> / <a href="r2sonic/r2s2omg.html"><code>r2s2omg</code></a> / <a href="gsf/gsf2omg.html"><code>gsf2omg</code></a></td>
      <td>Unpacking</td>
      <td><code>.s7k</code>, <code>.r2s</code>, <code>.gsf</code></td>
      <td><code>.merged</code>, <code>.nav</code>, <code>.orientation</code></td>
      <td>Convert Teledyne Reson 7k, R2Sonic, or Generic Sensor Format (GSF) multibeam files into <code>OMG_HDCS</code> (<code>.merged</code>).</td>
    </tr>
    <tr data-stage="ADCP, EK & Sub-Bottom" data-ext="ADCP .000 .raw .sgy">
      <td><a href="adcp/readADCP.html"><code>readADCP</code></a> / <a href="EKlook/EKlook.html"><code>EKlook</code></a></td>
      <td>ADCP, EK &amp; Sub-Bottom</td>
      <td>RDI PD0 (<code>.000</code>), Simrad (<code>.raw</code>)</td>
      <td>Current vectors, echograms, target strength</td>
      <td>Process Teledyne RDI ADCP velocity profiles and Simrad EK60/EK80 split-beam scientific echosounder data.</td>
    </tr>
  </tbody>
</table>

<script>
document.addEventListener("DOMContentLoaded", function() {
  const searchInput = document.getElementById("omg-tool-search");
  const stageSelect = document.getElementById("omg-stage-filter");
  const extBtns = document.querySelectorAll(".omg-ext-btn");
  const rows = document.querySelectorAll("#omg-tool-table tbody tr");
  let activeExt = "";

  function filterRows() {
    const q = (searchInput.value || "").toLowerCase().trim();
    const st = stageSelect.value || "";
    rows.forEach(function(tr) {
      const text = tr.textContent.toLowerCase();
      const rowStage = tr.getAttribute("data-stage") || "";
      const rowExt = (tr.getAttribute("data-ext") || "").toLowerCase();
      const matchQ = !q || text.includes(q) || rowExt.includes(q);
      const matchStage = !st || rowStage === st;
      const matchExt = !activeExt || rowExt.includes(activeExt.toLowerCase());
      tr.style.display = (matchQ && matchStage && matchExt) ? "" : "none";
    });
  }

  if (searchInput) searchInput.addEventListener("input", filterRows);
  if (stageSelect) stageSelect.addEventListener("change", filterRows);
  extBtns.forEach(function(btn) {
    btn.style.cursor = "pointer";
    btn.addEventListener("click", function() {
      activeExt = btn.getAttribute("data-ext") || "";
      extBtns.forEach(b => b.style.outline = "none");
      btn.style.outline = "2px solid #38bdf8";
      filterRows();
    });
  });
});
</script>

---

## Copy-Paste Command-Line Recipes

### 1. Unpack & Ray-Trace a Kongsberg `.kmall` + `.kmwcd` Line

```bash
LINE="0029_20260315_042139_Almirante_Viel"
DAY="74"
mkdir -p merged/$DAY decnav/$DAY ss/$DAY shpFiles/$DAY

# 1. Unpack .kmwcd water column first (if present), then .kmall bathymetry
read_kmall -just_wc -out merged/$DAY/$LINE raw/$DAY/$LINE.kmwcd
mv merged/$DAY/$LINE.merged merged/$DAY/justWC_$LINE.merged
read_kmall -out merged/$DAY/$LINE raw/$DAY/$LINE.kmall
moveOverWCinfo merged/$DAY/$LINE.merged merged/$DAY/justWC_$LINE.merged
rm -f merged/$DAY/justWC_$LINE.merged

# 2. Select active navigation (.nav_1) and attitude (.net_att_2 with fallback to .orientation_1)
cp merged/$DAY/$LINE.nav_1 merged/$DAY/$LINE.nav
if [ -s "merged/$DAY/$LINE.net_att_2" ]; then
  cp merged/$DAY/$LINE.net_att_2 merged/$DAY/$LINE.orientation
else
  cp merged/$DAY/$LINE.orientation_1 merged/$DAY/$LINE.orientation
fi

# 3. Filter navigation, merge onto pings, and create 10:1 decimated .decnav
stripNav merged/$DAY/$LINE.nav merged/$DAY/$LINE.nav.strip 30.0
cp merged/$DAY/$LINE.nav.strip merged/$DAY/$LINE.nav
mergeNav merged/$DAY/$LINE.merged merged/$DAY/$LINE.nav
appendNav -skip 10 -comp decnav/$DAY/$LINE.decnav merged/$DAY/$LINE.nav

# 4. Ray-trace with lever arms (.param) and high-rate attitude
mergeAtt -Saved_surface_arc -recalc_trans -big_att -kmall \
  -param merged/$DAY/$LINE.param \
  -att merged/$DAY/$LINE.orientation \
  merged/$DAY/$LINE.merged

# 5. Generate sidescan (.ss), water column curtain (.vert_prof), and bounds
makess -Redo_as_new -use_beam_ang merged/$DAY/$LINE.merged
mv merged/$DAY/$LINE.ss ss/$DAY/$LINE.ss
deTVG -box ss/$DAY/$LINE.ss
makeWC -vert_prof merged/$DAY/$LINE.merged
getBounds -100 merged/$DAY/$LINE.merged
```

### 2. Grid Bathymetry (`.r4`) & Create a Sun-Illuminated Hillshade (`.sun`)

```bash
# Create list of .merged files
ls merged/*/*.merged > merged_lines.list

# Grid to 25 m resolution in UTM Zone 20S (-utms -60.0)
weigh_grid -utms -60.0 -bounds -62.10 -57.90 -63.35 -59.84 \
  -res 25.0 -list merged_lines.list -out bransfield_25m

# Generate artificial sun-illumination (.sun) from the .r4 floating-point grid
meds_sun -in bransfield_25m.r4 -out bransfield_25m.sun -azi 315 -elev 45 -exag 4.0

# Inspect interactively in jview or export to GeoTIFF / QGIS VRT
jview bransfield_25m.r4 -sun bransfield_25m.sun
r4toTIFF -in bransfield_25m.r4 -out bransfield_25m.tif
```
