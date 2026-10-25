---
layout: default
title: avNav
parent: Navigation Tools
nav_order: 13
tool_name: avNav
source_path: code/nav/avNav.c
category: Navigation & Georeferencing
input_formats: [".nav (jcu_nav_rec binary)"]
output_formats: [".nav (jcu_nav_rec binary)"]
related_tools: ["filtnav", "mergeNav", "stripNav", "appendNav", "AuketoNav"]
---

# avNav

## Description
`avNav` smooths or low-pass filters binary OMG navigation files (`jcu_nav_rec`, `.nav`) using one of three user-selectable filtering algorithms:
1. **Boxcar Moving Average (`-nosmooth <N>`, default `20` samples):** Averages `lat`, `lon`, `time`, `velocity`, `azi`, and (unless `-donttouchdepth` is set) `depth` over a window of $N$ records. By default it decimates the output by $N$, or preserves the 1:1 record count if `-keeporignumrec` is specified.
2. **Cosine-Squared Tapered Low-Pass Filter (`-cos_taper <seconds>`):** Applies a time-domain $\cos^2$ weighted moving average over $\pm \text{longperiod}$ seconds to `tide_rec.azi` (e.g., for extracting long-period RTK heave drift / tides) or `tide_rec.velocity` (if `-do_vel` is set), preserving the original record count and timestamps.
3. **Median Filter (`-median <N>`):** Computes a running median of `tide_rec.azi` over windows of $N$ records, stepping by $N$.

---

## Usage

```bash
avNav [OPTIONS] -comp <output.nav> <input_nav_file(s)>
```

### Common Workflow Examples

**1. Smooth a `.nav` file with a 10-sample moving average while keeping the original number of records and vector-averaging azimuth:**
```bash
avNav -nosmooth 10 -keeporignumrec -realazi -comp smoothed.nav raw_line.nav
```

**2. Extract low-frequency RTK altitude / heave drift stored in `azi` using a $\pm 60\text{ s}$ cosine-squared taper:**
```bash
avNav -cos_taper 60 -comp lowpass_rtk_tide.nav rtk_height.nav
```

**3. Low-pass filter vessel velocity (`tide_rec.velocity`) using a $\pm 30\text{ s}$ cosine-squared taper:**
```bash
avNav -cos_taper 30 -do_vel -comp smooth_vel.nav line01.nav
```

---

## Arguments

| Option | Description | Default |
|---|---|---|
| `-comp <filename>` | **Required.** Output binary `.nav` filename (`jcu_nav_rec` format). | None |
| `<navfile(s)>` | **Required.** One or more input binary `.nav` files (up to 300 files). | None |
| `-nosmooth <N>` | Boxcar smoothing window length in samples (records). If `nosmooth > numrec`, automatically clamps to `0.99 * numrec - 2` to compute a single whole-file average position. | `20` |
| `-keeporignumrec` | Used with `-nosmooth`. Steps by `1` record (`firstrec = 0`, `lastrec = numrec`, `step = 1`, clamping edge indices to `[0, numrec-1]`) so the output `.nav` file has the exact same number of records as the input instead of decimating by `nosmooth`. | Disabled (decimates by `nosmooth`) |
| `-realazi` | Used with `-nosmooth`. Computes the circular vector mean of `tide_rec.azi` (`atan2(sum(sin(azi)), sum(cos(azi))) * 180 / M_PI`) for non-zero azimuths instead of a linear arithmetic average, preventing $0^\circ / 360^\circ$ wrap-around artifacts. | Disabled (linear average of `azi`) |
| `-donttouchdepth` | Used with `-nosmooth`. Leaves `tide_rec.depth` un-averaged (retains the last read record's depth in the window). | Disabled (averages `depth`) |
| `-cos_taper <sec>` | Enable cosine-squared time-domain low-pass filtering over a half-width of `<sec>` ($\pm \text{longperiod}$ seconds). Preserves all input records and positions, replacing only `azi` (or `velocity` if `-do_vel`). | Disabled |
| `-do_vel` | Used with `-cos_taper`. Filters `tide_rec.velocity` instead of `tide_rec.azi`. | Disabled (`azi`) |
| `-max_to_include <M>` | Used with `-cos_taper`. Maximum number of neighboring fixes before or after the center fix to include in the time taper window. | `100000` |
| `-median <N>` | Enable median filtering of `tide_rec.azi` over windows of `<N>` records (decimated by `<N>`). *(Note: in the source code, `cen_tide_rec.azi` receives `get_median()`, while `nav_write` writes `tide_rec`).* | Disabled |
| `-v` | Enable verbose diagnostic output for each averaged record. | Disabled |

---

## How It Works

### 1. Boxcar Smoothing Mode (Default / `-nosmooth`)
* Determines `numrec = filesize / 48`.
* If `-keeporignumrec` is set, evaluates every center index $k \in [0, \text{numrec}-1]$; otherwise steps $k$ from `nosmooth / 2` to `numrec - nosmooth / 2` in increments of `nosmooth`.
* For each window $i \in [-\text{nosmooth}/2, \text{nosmooth}/2 - 1]$, sums `time` (including `centisecs / 100.0`), `lat`, `lon`, `velocity`, `azi`, and `depth`, plus $\cos(\text{azi})$ and $\sin(\text{azi})$ for non-zero `azi`.
* Divides accumulated sums by the window count `actuali` (or uses `atan2(sin_azi, cos_azi)` when `-realazi` is passed) and writes the smoothed `jcu_nav_rec`.

### 2. Cosine-Squared Taper Mode (`-cos_taper <longperiod>`)
* Reads all `numrec` timestamps into `TtimE[]` and the target variable (`azi` or `velocity`) into `RP_rtk[]`.
* For each record $k \in [0, \text{numrec}-1]$, marches backward ($m \le k$) and forward ($m > k$) while $\Delta t = |T_k - T_m| \le \text{longperiod}$ and count $< \text{max\_to\_include}$.
* Computes weights using a raised cosine-squared taper:
  $$w(\Delta t) = \cos^2\left(\frac{\pi}{2} \cdot \frac{\Delta t}{\text{longperiod}}\right)$$
* Normalizes `Lowpass_RP_rtk[k] = sum(w * RP_rtk[m]) / sum(w)` and writes all `numrec` records to the output file with the filtered value stored in `azi` (or `velocity`).
