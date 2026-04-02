## BOMscroller

A time-based BOM navigator built for ERP data.


---

## Overview

BOMscroller is a local web tool for exploring how a Bill of Materials (BOM) evolves over time.

It does **not** compare static version snapshots.  
Instead, it reconstructs BOMs from a **date-driven row model** and compares them visually.

The goal is simple:

> Understand *what changed, where,* and *when* — in a way that matches how BOMs actually behave in real systems.

---
## Example
<img width="1835" height="835" alt="image" src="https://github.com/user-attachments/assets/cd26d16d-dbc9-4a4b-8bf6-381bbeeefd2f" />

---


## Coloring logic

| Relation                  | Color   |
|--------------------------|--------|
| Diff: Left → Center      | Blue   |
| Diff: Center → Right     | Purple |

Changes include: added / removed / replaced / qty changed

Green indicates the current version

---

## Intended use case

- Fast navigation across many revisions  
- Rapid review of BOM changes  
- Clear visual overview of structural changes  
- For teams that currently export to Excel or manually compare versions  

Built for:
- date-effective ERP data  
- human understanding, not raw diff output  

---

## How it works

Under the hood, BOMs are reconstructed from a row-based ERP model where each row is defined by:

- SKU  
- item group (structural position in the BOM)  
- part number  
- quantity  
- validity period (from_date / to_date)  

Rows are aligned using a structural key (`item_grp`), not by part identity.

This means:
- comparisons follow the structure of the BOM  
- part replacements appear as in-place changes  
- new parts appear as local insertions  

The BOM can be rebuilt at any point in time without relying on stored snapshots.

---


## Running locally

```bash
pip install flask
python app.py
```

Then open:

```
http://127.0.0.1:5000
```

---
## How it compares

#### File-based BOM diff tools

[bom-diff](https://github.com/ttran-tech/bom-diff)  
→ Upload and compare two BOM files (Excel/CSV)

[BOM Compare Tool (Sierra Circuits)](https://www.protoexpress.com/tools/bom-compare-tool/)  
→ Upload BOM files and highlight added/removed/changed parts

[Excel BOM Comparer](https://ddbim.com/excelbomcomparer/)  
→ Compare two revisions directly in Excel

---

#### ERP / PLM tools

eg. OpenBOM, NetSuite tools, ERPNext BOM compare

These allow comparing BOM revisions inside a system, typically:

- select BOM A  
- select BOM B  
- view differences  

---

#### BOMscroller (this project)

BOMscroller takes a different approach:

- No file upload  
- No “compare A vs B”  
- No static snapshots  

Instead:

→ Scroll through BOM versions over time, directly from ERP data

---

## Assumptions behind the BOM structure

This project is built around a specific assumption of how BOMs behave in real-world ERP systems:
they are revision-driven, structurally stable, and evolve incrementally over time.

For a detailed explanation of the underlying model and design decisions, see:

→ [BOM assumptions](bom-assumptions.md)

---

## Project status

This is a concept prototype.

The focus is on:

- data model correctness  
- visual clarity  
- realistic BOM behavior  

Not production readiness.
