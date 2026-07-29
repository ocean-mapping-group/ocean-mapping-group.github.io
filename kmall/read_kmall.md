---
layout: default
title: read_kmall
parent: Raw Data Handling
---

# read_kmall

`read_kmall` is a core utility designed to parse and process multibeam sonar data stored in the KMall format. Within our data pipeline, it serves as a critical entry point for "unraveling" raw seafloor records into a structured state suitable for downstream analysis.

### Role in Data Pipeline
The tool focuses on the extraction of essential beam geometry and intensity values while handling the specific memory-mapped structures inherent to large KMall datasets. It bridges the gap between raw disk blocks and our internal processing models, ensuring that headers are correctly parsed and that spatial metadata is preserved during the transition from "raw" to "processed."

### Key Functions
- **Header Validation**: Ensures the file conforms to expected KMall specifications before reading begins.
- **Coordinate Transformation**: Initial mapping of local beam coordinates into a standardized system.
- **Memory Management**: Optimized for large datasets where full data loading is not feasible, utilizing indexed lookups to streamline performance.

### Technical Note
Unlike standard raw input tools, `read_kmall` includes specific logic to handle the evolution of seafloor survey headers across different sensor generations, ensuring backward compatibility with older survey data while maintaining high performance on modern hardware.