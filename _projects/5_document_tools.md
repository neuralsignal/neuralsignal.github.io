---
layout: page
title: Document & productivity tools
description: Tools for document generation, conversion, and knowledge management
img:
order: 50
category: data tools
---

### Obsidian export

I use Obsidian for most of my writing, so I built a tool that converts Obsidian-flavored Markdown into PDF and DOCX documents. It handles wikilinks, embeds, Mermaid diagrams, and callouts through a 5-stage processing pipeline. You can set up profiles for different styling needs.

[neuralsignal/obsidian-export](https://github.com/neuralsignal/obsidian-export)

### Obsidian import

The inverse — pulls content from PDFs, Word documents, PowerPoint, spreadsheets, and other formats into Obsidian-ready Markdown with YAML frontmatter. Useful for batch-importing reference material.

[neuralsignal/obsidian-import](https://github.com/neuralsignal/obsidian-import)

### Excel financial model tooling

A tool that takes a YAML spec and generates Excel workbooks with formulas, styling, and named ranges. I built it to automate the tedious parts of financial modeling — P&L statements, DCF analyses, budgets, scenario comparisons. Works as both a CLI tool and a Python API.

[neuralsignal/excel-model](https://github.com/neuralsignal/excel-model)
