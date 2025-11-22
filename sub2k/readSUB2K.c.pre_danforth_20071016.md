---
layout: default
title: readSUB2K.c.pre_danforth_20071016
parent: SUB2K Tools
grand_parent: code
nav_order: 6
---
# readSUB2K.c.pre_danforth_20071016

## Description
`readSUB2K.c.pre_danforth_20071016` is an older variant of the `readSUB2K` utility, designed for processing Submetrix 2000 sonar data and converting it into OMG_HDCS format. Its core functionality is largely identical to `readSUB2K.c`, offering similar processing steps for sidescan intensity scaling, data quality filtering, nadir pre-filtering, coverage control, phase-to-angle conversion, attitude data integration, and environmental corrections. The suffix `_pre_danforth_20071016` indicates that this version predates specific modifications made by Bill Danforth on October 16, 2007.

## Usage
The usage and arguments for `readSUB2K.c.pre_danforth_20071016` are essentially the same as `readSUB2K`. Please refer to the documentation for [`readSUB2K`](readSUB2K.md) for detailed information on command-line options.

## How It Works
The underlying logic and processing steps, including ISIS block processing, quality control, phase-to-angle conversion, sidescan intensity processing, and OMG_HDCS output, are the same as described in the documentation for [`readSUB2K`](readSUB2K.md). Specific internal differences or optimizations related to the pre-Danforth modifications may exist but do not change the high-level functionality.
