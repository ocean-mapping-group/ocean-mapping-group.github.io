---
layout: default
title: convSUB16.c2
parent: SUB2K Tools
grand_parent: code
nav_order: 2
---
# convSUB16.c2

## Description
`convSUB16.c2` is a variant of the `convSUB16` utility, designed to convert 16-bit intensity sidescan data from Submetrix 2000 into an 8-bit GLORIA format (typically a `.sst` file). Its core functionality is largely identical to `convSUB16.c`, offering similar scaling options (linear, square root, TVG, or logarithmic) for compressing the data. This version might represent an older iteration or a slightly modified build for specific purposes.

## Usage
The usage and arguments for `convSUB16.c2` are essentially the same as `convSUB16`. Please refer to the documentation for [`convSUB16`](convSUB16.md) for detailed information on command-line options.

## How It Works
The underlying logic and processing steps, including data loading, scaling algorithms, and conversion to 8-bit GLORIA records, are the same as described in the documentation for [`convSUB16`](convSUB16.md). Minor internal differences or optimizations may exist but do not change the high-level functionality.
