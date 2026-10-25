---
layout: default
title: GSF Library (gsf_lib)
nav_order: 9
has_children: true
---

# GSF Library (`gsf_lib`)

The `gsf_lib` directory contains the C reference implementation of the **Generic Sensor Format (GSF)** library (version `GSF-v03.04`, originally developed by J. S. Byrne at SAIC/Leidos), compiled into `libgsf.a` and linked by OMG tools such as [`omg2gsf`](../gsf/omg2gsf.md), [`gsf2omg_7101`](../gsf/gsf2omg_7101.md), [`gsftest`](../gsf/gsftest.md), and [`jgsf2omg`](../gsf/jhc/jgsf2omg.md).

## Module Summary

| Source Module | Role | Description |
| :--- | :--- | :--- |
| [`gsf`](gsf.md) | Core API & File I/O | Top-level entry points (`gsfOpen`, `gsfClose`, `gsfRead`, `gsfWrite`, `gsfSeek`, `gsfGetMBParams`, `gsfPutMBParams`, scale factor management, and error handling). |
| [`gsf_dec`](gsf_dec.md) | Byte-Stream Decoder | Decodes network-byte-order GSF records and sensor-specific subrecords into host C structures (`gsfRecords`). |
| [`gsf_enc`](gsf_enc.md) | Byte-Stream Encoder | Encodes host C structures (`gsfRecords`) into 4-byte-aligned network-byte-order GSF records. |
| [`gsf_indx`](gsf_indx.md) | Direct-Access Indexing | Builds, appends, and queries binary `.ndx` index files to support random record access (`GSF_READONLY_INDEX`, `GSF_UPDATE_INDEX`). |
| [`gsf_info`](gsf_info.md) | File Capability Queries | Informational helper functions (`gsfFileSupportsRecalculateXYZ`, `gsfFileSupportsRecalculateTPU`, `gsfFileSupportsRecalculateNominalDepth`, `gsfFileContainsMBAmplitude`, `gsfFileContainsMBImagery`). |
