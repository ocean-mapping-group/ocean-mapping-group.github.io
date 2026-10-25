---
layout: default
title: Preprocessing Tools
parent: Sidescan Tools
nav_order: 8
has_children: true
---

# Preprocessing Scripts (`sidescan/preproc`)

The `preproc` directory (`code/sidescan/preproc/`) contains C-shell batch processing scripts written by Guy Carpenter (November 1990) to automate the end-to-end preprocessing of GLORIA long-range sidescan sonar passes (specifically the 1989 Northeast Australia cruise `ps89_001` through `ps89_062`).

## Scripts in This Directory

* **[`rebuild_neaust`](rebuild_neaust.md)** — Master batch pipeline script that takes raw `.ios` GLORIA pass files through median gain filtering (`gainmed_neaust`), slant-range and navigation preprocessing (`preprocI_plus` -> `.slr`), empirical beam mapping (`mapbeam`), beam removal (`debeam2` -> `.beam`), azimuth repair (`neaust_fixazi`), time mark fixing (`fixmark`), and multi-pass beam table joining (`joinbeam`).
* **[`neaust_fixazi`](neaust_fixazi.md)** — C-shell script invoked by `rebuild_neaust` to recompute and smooth corrupted towfish azimuths on specific passes (`ps89_001.beam` to `ps89_003.beam`) using [`azimerge -layback 150`](../merge/azimerge.md) and [`smthazi -t 6 -f 3`](../azibat/smthazi.md).
* **[`rebuild_neaust.bak`](rebuild_neaust.bak.md)** — Earlier backup of `rebuild_neaust` covering stages 1–4 (`gainmed_neaust`, `preprocI_plus`, `mapbeam`, and `debeam2`).
* **[`rebuild.bak`](rebuild.bak.md)** — Initial template header script for batch GLORIA pass rebuilding.
