---
layout: default
title: Embedded GSF C Library (gsf_lib)
parent: 5. Core Libraries, Researcher Suites & Utilities
nav_order: 4
has_children: true
---

# GSF Library (`gsf_lib`)

The `gsf_lib` directory contains the C reference implementation of the **Generic Sensor Format (GSF)** library (version `GSF-v03.04`, originally developed by J. S. Byrne at SAIC/Leidos), compiled into `libgsf.a` and linked by OMG tools such as [`omg2gsf`](../gsf/omg2gsf.html), [`gsf2omg_7101`](../gsf/gsf2omg_7101.html), [`gsftest`](../gsf/gsftest.html), and [`jgsf2omg`](../gsf/jhc/jgsf2omg.html).

## Module Summary

| Source Module | Role | Description |
| :--- | :--- | :--- |
| [`gsf`](gsf.html) | Core API & File I/O | Top-level entry points (`gsfOpen`, `gsfClose`, `gsfRead`, `gsfWrite`, `gsfSeek`, `gsfGetMBParams`, `gsfPutMBParams`, scale factor management, and error handling). |
| [`gsf_dec`](gsf_dec.html) | Byte-Stream Decoder | Decodes network-byte-order GSF records and sensor-specific subrecords into host C structures (`gsfRecords`). |
| [`gsf_enc`](gsf_enc.html) | Byte-Stream Encoder | Encodes host C structures (`gsfRecords`) into 4-byte-aligned network-byte-order GSF records. |
| [`gsf_indx`](gsf_indx.html) | Direct-Access Indexing | Builds, appends, and queries binary `.ndx` index files to support random record access (`GSF_READONLY_INDEX`, `GSF_UPDATE_INDEX`). |
| [`gsf_info`](gsf_info.html) | File Capability Queries | Informational helper functions (`gsfFileSupportsRecalculateXYZ`, `gsfFileSupportsRecalculateTPU`, `gsfFileSupportsRecalculateNominalDepth`, `gsfFileContainsMBAmplitude`, `gsfFileContainsMBImagery`). |
