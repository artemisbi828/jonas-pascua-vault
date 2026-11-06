# AI Prompt - Data Object Naming

**Purpose:** Reusable entry point for converting long data-object requests into compact Markdown.

## Prompt

```text
Use [[Standard - Data Object Naming]] for naming rules.
Use [[Standard - Notation - Compact Runbook Markdown]] for the required output format.

Convert the input below into that compact workbook format.
Return only: Do This, Transformations, Object Map, Warnings, and Open Decisions.
Use the Do This table, source -> target notation, Mermaid flowchart, and ASCII tree.
Do not write an introduction or explanatory essay.
Do not invent missing keys, abbreviations, timezones, datatypes, or decisions.
Use ? or [manual] for missing evidence and flag it.
Keep accepted mappings stable on reruns; show only changes, new warnings, and new decisions.

INPUT
[paste request, schema, SQL, sample data, or notes]
```

Format reference: [[Standard - Process - Compact Markdown Runbook]]
Rules reference: [[Standard - Naming - Artifacts]]
