# Obsidian Notes Normalization: Automation & QA

This guide defines the AI-assisted scrub process for Obsidian notes, enforcing semantic consistency and reducing complexity.

---

## Concept Index (Constraint Enforcement)

Both `terminology-prime-names.md` and `finance-business-concepts.md` must maintain this complete list of **Prime Names**:

```
aggregate, margin, collection, posting, void, write-off, bad debt, addback, capex, opex, overhead, conversion, score, satisfaction, effort, promoter, charge, adjustment, revenue, cogs, gross profit, cost (labor), cost (marketing), cost (other), ebitda, ebitda margin
```

**Validation Rule:** If a prime name appears in one file, it must be defined or referenced in both. Use automated diff to flag missing entries.

---

## Normalization Workflow

### Phase 1: Discovery
- [ ] Scan all Obsidian notes for terms matching `terminology-prime-names.md` **Anti-Patterns** column.
- [ ] Flag but do not auto-replace if context is ambiguous (e.g., "total" in a table header vs. "total satisfaction score").
- [ ] List findings: file, line, term, replacement candidate.

### Phase 2: Semantic Consolidation (M→1)
- [ ] Identify notes with duplicate or near-duplicate content across different file names/locations.
- [ ] Flag for manual review: **"Should these merge into single source?"**
- [ ] If yes: Consolidate → Keep highest-quality version → Redirect stale notes with backlinks → Remove orphan duplicates.
- [ ] If no (intentional variation): Document reason in both file headers.

### Phase 3: Decomposition (1→M)
- [ ] Scan notes > 1000 words or >15 sections; flag for potential split.
- [ ] Ask: **"Does this note mix multiple elemental concepts without strong causal link?"**
- [ ] If yes: Extract into separate notes; link with "Related" or "Derived from".
- [ ] If no: Document why it's monolithic (e.g., "Integrated case study").

### Phase 4: Anti-Pattern Replacement (Mechanical)
- [ ] Replace anti-pattern terms with prime names using lookup table.
- [ ] Safe replacements (low ambiguity):
  - `total customer satisfaction` → `aggregate satisfaction score`
  - `overall margin` → `margin (noun)`
  - `capture cash` → `collect` or `posting (cash)`
  - `efficiency ratio` → `margin (ratio)`
- [ ] Flag for manual review (higher ambiguity):
  - `total` (could be Grand Total, line total, or anti-pattern)
  - `overall` (depends on sentence structure)

### Phase 5: Vague Phrase Detection & Tagging
- [ ] Scan for vague language:
  - Unquantified: "significant growth", "notable improvement", "material impact"
  - Unattributed: "they said", "it's clear", "everyone knows"
  - Generic: "interesting", "important", "critical" (without context)
- [ ] Replace with specifics (data, source, stakeholder) or tag `#needscontext` for manual review.

### Phase 6: Duplication & Miscategorization Detection
- [ ] Cross-reference file names and locations:
  - Are there semantically similar titles in different folders? (e.g., `EBITDA.md` in /finance/ and /metrics/?)
  - Does file location match content? (e.g., strategy notes in /ops/ vs /finance/?)
- [ ] Flag: **"Possible duplicate or miscategory. Review and consolidate or move."**
- [ ] Ask: **"Does this file add utility or just increase search/navigation friction?"**

### Phase 6b: Unused Asset Cleanup
- [ ] Scan for image attachments referenced in note links vs. embedded in markdown.
- [ ] List: Attachments not linked anywhere.
- [ ] Ask: **"Keep or delete?"** Delete if not actively used.

### Phase 7: Reference Gap Detection
- [ ] For each note, identify all external references (links, citations, data sources).
- [ ] Flag: Missing references (broken links, implied but not stated).
- [ ] Create task: **"Find and add [missing source]"** or **"Justify [inferred claim]"**.

---

## Automation Triggers

### Manual Triggers
- **EOD Obsidian Close:** Run Phases 1–5; output report for review.
- **Weekly Review:** Run Phases 6–7; surface consolidation opportunities.
- **On-Demand:** User invokes via command (e.g., `/obsidian-scrub [folder]`).

### Automated Outputs
- **Report:** `NORMALIZATION_REPORT_[TIMESTAMP].md`
  - Sections: Summary, Findings by Phase, Priority Tasks, Flagged for Manual Review.
- **Task List:** Auto-generated `todo.txt` entries:
  - `[ ] Consolidate: [file-a] + [file-b]`
  - `[ ] Review anti-pattern: [term] in [file:line]`
  - `[ ] Verify reference: [link] in [file]`
  - `[ ] Remove unused: [attachment] from [file]`

### Error Handling
- **Conflict:** Multiple candidate replacements for one term → Flag for manual choice.
- **Circular Reference:** Note A links to Note B links to Note A → Flag as potential merge candidate.
- **Missing Metadata:** Notes without folder context → Suggest category based on keywords.

---

## Manual Review Checklist (Post-Automation)

- [ ] **Consolidation:** Approve/reject proposed merges; update links if approved.
- [ ] **Decomposition:** Approve/reject proposed splits; create new notes if approved.
- [ ] **Anti-Pattern Replacement:** Approve each flagged replacement or mark as context-dependent.
- [ ] **Vague Phrases:** Decide: research data, add source, or delete assertion.
- [ ] **Duplicates:** Decide: keep one (which?), move to correct location, or delete.
- [ ] **Missing References:** Decide: find source, add citation, or remove claim.
- [ ] **Unused Assets:** Delete unused attachments; confirm zero broken links.

---

## Example: EOD Automation Output

```
NORMALIZATION_REPORT_20260715_1800.md

## Summary
- 47 notes scanned; 12 flagged for review
- 8 anti-pattern terms found (4 auto-replaceable, 4 ambiguous)
- 2 potential duplicates detected
- 1 unused image (./assets/old-chart.png)

## Priority Tasks
- [ ] Consolidate: finance/EBITDA.md + metrics/operating-profit.md
- [ ] Review vague phrase: "significant growth" in growth-strategy.md:line 23
- [ ] Delete unused: ./assets/old-chart.png
- [ ] Add source: "Industry standard is 35% margin" in cost-structure.md:line 15

## Flagged for Manual Review (Ambiguous Replacements)
- cost-analysis.md:line 8: "total" → "aggregate" or "Grand Total"? [Manual choice needed]
- dashboard-spec.md:line 42: "efficiency ratio" → "margin (ratio)"? [Confirm measure type]

## Unchanged Anti-Patterns (Context-Dependent)
- profit-roadmap.md:line 5: "all-in total cost" [Keep as-is; "all-in" modifier clarifies]
```

---

## Integration: AI-Assisted Scrub Process

**Tool:** Invoke Copilot with prompt:
```
Normalize this Obsidian note against the Prime Names framework.
Use terminology-prime-names.md and finance-business-concepts.md as reference.
Replace anti-patterns. Flag ambiguous terms. Note duplications or miscategories.
Output as checklist with all changes highlighted.
```

**Result:** Review suggested changes; apply approved edits; move to task list for manual decisions.

---

## Maintenance

- **Weekly:** Update `Concept Index` if new prime names are added.
- **Monthly:** Re-run full scrub on all folders; track trends (e.g., "most common anti-pattern").
- **As-Needed:** Add new concepts to both reference files; validate with other docs.
