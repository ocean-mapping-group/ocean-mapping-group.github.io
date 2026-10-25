---
layout: default
title: SE_Weekley_Goodrich_Cornman
parent: SwathEd (SE) Tools
nav_order: 20
tool_name: SE_Weekley_Goodrich_Cornman
source_path: code/SE/SE_Weekley_Goodrich_Cornman.c
category: Interactive QC & Editing (SwathEd)
input_formats: [".merged"]
output_formats: [".merged (beam status flags updated in-place)"]
related_tools: ["swathed", "SE_filters", "SE_AUTOFLAGwin"]
---

# `SE_Weekley_Goodrich_Cornman` — Neighbor-Depth Phase-Space Outlier Filter (`WGC Tool`)

`SE_Weekley_Goodrich_Cornman` (`code/SE/SE_Weekley_Goodrich_Cornman.c`, `code/SE/SE_Weekley_Goodrich_Cornman.h`) implements the `"WGC Tool"` (`sub_window[59..61]`) in [`swathed`](swathed.md). Authored by Jonathan Beaudoin (February 2011) after the Weekley–Goodrich–Cornman lag-1 scatter/phase-space outlier detection method, it plots adjacent sounding depths against one another—$z(b, p)$ vs. $z(b, p+1)$ along-track and $z(b, p)$ vs. $z(b+1, p)$ across-track—and flags soundings whose orthogonal distance from the 1:1 identity line ($y = x$, slope $45^\circ$) exceeds a configurable threshold (`weekley_filter_width`).

---

## Window Architecture (`sub_window[59..61]`)

Clicking the **`WGC`** icon (`icon_window[17]`) on the main `swathed` toolbar calls `view_weekley_box()`, which creates top-level container `sub_window[59]` (`306 × 609` px, titled `"WGC Tool"`) in the bottom-right corner of the display containing two 300×300 pixel phase-space scatterplots:

| Sub-Window | Plot Title | Horizontal Axis ($x$) | Vertical Axis ($y$) | Description |
| :--- | :--- | :--- | :--- | :--- |
| `sub_window[60]` | **`Beam filter` (Along-Track Lag-1)** | Depth $z(j, i)$ at beam $j$, ping $i$ (`box[j][i]`) | Depth $z(j, i+1)$ at beam $j$, ping $i+1$ (`box[j][i+1]`) | Plots every unflagged adjacent along-track sounding pair across the 80 loaded swaths (`SE_NO_SWATHS`). |
| `sub_window[61]` | **`Swath filter` (Across-Track Lag-1)** | Depth $z(j, i)$ at beam $j$, ping $i$ (`box[j][i]`) | Depth $z(j+1, i)$ at beam $j+1$, ping $i$ (`box[j+1][i]`) | Plots every unflagged adjacent across-track sounding pair across all beams (`SE_NO_MAX`) in the 80 swaths. |

Both scatterplots auto-scale their axes (`x_min`, `x_max`, `y_min`, `y_max`) to match the active depth range of the main `swathed` window (`fabs(graphic_param[0].y_max)` to `fabs(graphic_param[0].y_min)`).

---

## Mathematical Formulation & Filtering Algorithm

### 1. Orthogonal Distance to the $45^\circ$ Identity Line (`plot_weekley_box`)
On a continuous seafloor with small ping-to-ping and beam-to-beam depth changes, adjacent depth pairs $(z_1, z_2)$ cluster tightly along the $45^\circ$ diagonal $z_2 = z_1$. For each valid, unflagged neighbor pair (`box[j][i] > 0` and neighbor `> 0`), `plot_weekley_box()` computes the perpendicular Euclidean distance $d_\perp$ from $(z_1, z_2)$ to the diagonal line connecting `(x_min, y_min)` and `(x_max, y_max)`:

$$d_\perp = \frac{|(x_{\max} - x_{\min})(y_{\min} - z_2) - (x_{\min} - z_1)(y_{\max} - y_{\min})|}{\sqrt{(x_{\max} - x_{\min})^2 + (y_{\max} - y_{\min})^2}} = \frac{|z_2 - z_1|}{\sqrt{2}}$$

* Pairs with $d_\perp \le \text{weekley\_filter\_width}$ are plotted as **`GREEN`** crosses.
* Outlier pairs with $d_\perp > \text{weekley\_filter\_width}$ are plotted as **`RED`** crosses outside the two **`MAGENTA`** acceptance envelope lines ($y = x \pm \text{weekley\_filter\_width} / \sin 45^\circ$).

### 2. Two-Pass Outlier Flagging (`do_weekley_filter`)
Pressing the **`w`** key while the cursor is inside the main across-track editing window (`graphic_window[1]`) invokes `do_weekley_filter()`:
1. **Undo State Preservation:** Calls `shift_undo_flags()` so the entire WGC filter pass can be reversed with `u` (Undo).
2. **Across-Track Pass (`Swath filter`):** For each swath $i \in [0, \text{SE\_NO\_SWATHS}-1]$, evaluates $d_\perp$ between adjacent beams `box[j][i]` and `box[j+1][i]`. Whenever $d_\perp > \text{weekley\_filter\_width}$, both `weekley_flags[j]` and `weekley_flags[j+1]` are marked, and all marked soundings are negated (`box[j][i] = -box[j][i]`, `box_flags[j][i]++`, `some_flagged++`).
3. **Along-Track Pass (`Beam filter`):** For each beam index $j \in [0, \text{SE\_NO\_MAX}-1]$, evaluates $d_\perp$ between consecutive pings `box[j][i]` and `box[j][i+1]` across the remaining unflagged soundings, flagging pairs that exceed `weekley_filter_width`.

---

## Interactive Workflow

1. Click the **`WGC`** icon (`icon_window[17]`) on the `swathed` toolbar to open `"WGC Tool"` (`sub_window[59..61]`).
2. Inspect the `Beam filter` (`sub_window[60]`) and `Swath filter` (`sub_window[61]`) plots to see which soundings fall outside the magenta threshold lines (colored `RED`).
3. Press **`w`** inside `graphic_window[1]` to execute `do_weekley_filter()`, immediately rejecting the red outliers and refreshing both the main `swathed` profiles and `WGC Tool` plots.
