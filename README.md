## BOMscroller

A time-based BOM navigator built for live ERP data.


---

## Overview

BOMscroller is a local web tool for exploring how a Bill of Materials (BOM) evolves over time.

It does **not** compare static version snapshots.  
Instead, it reconstructs BOMs from a **date-driven row model** and compares them visually.

The goal is simple:

> Understand *what changed, where,* and *when* — in a way that matches how BOMs actually behave in real systems.

---
## Example
<img width="1835" height="835" alt="image" src="https://github.com/user-attachments/assets/a8f9e183-f807-4eef-84a2-c89b39fe1eac" />

---


## Coloring logic

| Relation                  | Color   |
|--------------------------|--------|
| Change Left vs Center    | Blue   |
| Change Center vs Right   | Purple |

Changes include:
- different quantity
- different part number
- add new or remove part

Green is the current version

---

## What this tool is

- A visual diff tool for BOM evolution  
- Based on date-effective data  
- Designed for human understanding  

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
