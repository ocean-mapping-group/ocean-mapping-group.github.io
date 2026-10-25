---
layout: default
title: LocalAI / LLM & RAG Dataset
nav_order: 5
has_children: false
---

# LLM / RAG & Fine-Tuning Resources for LocalAI Multibeam Processing

This repository is structured to serve two purposes simultaneously:
1. **A human-readable guide** for Ocean Mapping Group (OMG) graduate students and researchers processing multibeam sonar data.
2. **A machine-readable knowledge base and instruction dataset** for building a LocalAI-based multibeam processing and troubleshooting assistant.

---

## Machine-Readable Datasets in `/llm/`

| File | Format | Description & Intended Use |
| :--- | :--- | :--- |
| **[`omg_tools_catalog.json`](omg_tools_catalog.json)** | JSON | Structured tool schema catalog covering core OMG C executables and wrapper scripts (`read_kmall`, `RTlite`, `moveOverWCinfo`, `stripNav`, `appendNav`, `mergeNav`, `newMergeAtt`, `mergeAtt`, `mergeHeave`, `mergeTide`, `deTVG`, `makess`, `getBounds`, `make_blank`, `weigh_grid`, `r4to8bit`, `addSUN`, `glfill`, `stretchacres`, `mos2`, `swathed`, `jview`, `tor4`, `tomos`, `bunravel`, `unravel_KMALL_2500m_RevHplus_netatt2_parallel`). Includes exact CLI syntax, flag definitions, required companion files, pre-conditions, post-conditions, and diagnostic error strings. Ideal for **LLM tool-calling / function-calling** and deterministic command synthesis. |
| **[`omg_workflows_and_troubleshooting.jsonl`](omg_workflows_and_troubleshooting.jsonl)** | JSON Lines (`.jsonl`) | Curated instruction-tuning and RAG Q&A pairs (`instruction`, `input`, `output`, `category`, `tools_used`) covering end-to-end Kongsberg `.kmall`/`.kmwcd` and `.all`/`.wcd` unraveling, sensor selection, ray-tracing, bathymetric gridding, sidescan mosaicking, and troubleshooting of real-world processing errors. Ready for **LoRA / QLoRA fine-tuning** (e.g., Llama-3, Qwen-2.5-Coder, Mistral) or **few-shot prompt retrieval**. |

---

## RAG Chunking Strategy for Markdown Documentation

Every tool and workflow page in this repository includes structured **YAML frontmatter** designed for metadata-filtered vector retrieval:

```yaml
---
layout: default
title: read_kmall
parent: KMALL Tools
tool_name: read_kmall
source_path: code/kmall/read_kmall.c
category: kmall_unraveling
input_formats:
  - .kmall
  - .kmwcd
output_formats:
  - .merged
  - .param
  - .nav_1
  - .net_att_2
related_tools:
  - moveOverWCinfo
  - stripNav
  - mergeNav
  - newMergeAtt
  - makess
---
```

### Recommended Ingestion Pipeline for LocalAI / Chroma / Qdrant / pgvector

1. **Split by Markdown H2 (`## `) Headers:** Each tool page is organized into consistent semantic sections (`Overview`, `Syntax & CLI Options`, `Companion Files Read & Written`, `Workflow Context & Examples`, `Troubleshooting & Common Pitfalls`).
2. **Attach Frontmatter Metadata to Every Chunk:** Preserve `tool_name`, `source_path`, `category`, `input_formats`, `output_formats`, and `related_tools` in the vector store metadata payload for every H2 chunk.
3. **Graph-Augmented Retrieval via `related_tools`:** When a user asks about a pipeline step (e.g., `read_kmall`), automatically retrieve the `Workflow Context` and `Troubleshooting` chunks of its `related_tools` (`moveOverWCinfo`, `mergeNav`, `newMergeAtt`).
