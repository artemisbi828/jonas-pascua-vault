[_TOC_]

```
## Table of Contents

- [Medallion Architecture Overview](#medallion-architecture-overview)
- [Layer Definitions](#layer-definitions)
- [Layer Quick Reference Card](#quick-reference-card)
- [File Naming Conventions](#file-naming-conventions)
- [Audit Columns](#audit-columns)
- [Surrogate Key Strategy](#surrogate-key-strategy)
- [Materialization Strategy](#materialization-strategy)
- [Incremental Patterns](#incremental-patterns)
- [Clustering Strategy](#clustering-strategy)
- [Slowly Changing Dimensions (SCD)](#slowly-changing-dimensions-scd)
- [Date Dimension](#date-dimension)
- [Testing Standards](#testing-standards)
- [YAML Schema File Standards](#yaml-schema-file-standards)
- [Alias Configuration](#alias-configuration)
- [Directory Structure](#directory-structure)
- [In-File Documentation Standards](#in-file-documentation-standards)

```

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   BRONZE    │───▶│   SILVER    │───▶│    GOLD     │───▶│   VIRTUAL   │
│  (Raw/Raw)  │    │ (Refined)   │    │  (Modeled)  │    │   (Views)   │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```