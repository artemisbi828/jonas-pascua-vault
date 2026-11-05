# Message Notation Standard

## Purpose
Rewrite rough messages into **minimal, punchy, human-readable notation**.

Prioritize:
1. key point
2. sources / states being compared
3. magnitude of difference
4. implication or next step

Remove history, filler, and explanation unless needed to understand the point.

## Core Rules

- Prefer one line per point.
- Use short source/state names.
- Use `vs` for direct comparisons.
- Use `→` for result, implication, or next step.
- Use `Δ` for numeric difference.
- Use `|` for 3+ side-by-side values.
- Use `{a, b, c}` when naming a comparison set without listing values.
- `Δ` = **left minus right** unless explicitly stated otherwise.
- Preserve important uncertainty: `~`, `likely`, `expected`, etc.
- Do not add prose that the source message does not need.

## Patterns

### 2-way comparison

```text
A vs B → Δ +65
A vs B → Δ -$400K
```

With values:

```text
ours 617 vs manual 552 → Δ +65
```

With a dimension:

```text
2026-09-21: ours 617 vs manual 552 → Δ +65
2026-09-22: ours 602 vs manual 524 → Δ +78
```

### 3+ way comparison

```text
pulse: 400K | ascend: 380K | manual: 365K
```

When one source is the baseline:

```text
vs manual:
- ours 617 → Δ +65
- other 602 → Δ +50
```

Comparison set only:

```text
~$400K diff across {expected, current-state, ascend-state}
```

### Status / open loop

```text
topic: current state → outcome / next step
```

Examples:

```text
referral-sources-1: Sang has MVP inputs → Amber unblocked / ideally closed
referral-sources-2: current model cannot support full ask → PMO level-set needed
orthofi-net-production: ~$400K diff across {expected, current-state, ascend-state} → impact analysis
```

## Rewrite Instruction

When given a rough message:

1. Identify the **topic**.
2. Identify the **sources, states, or alternatives** being compared.
3. Surface the **difference or key finding** first.
4. End with the **outcome, status, or next action** only when useful.
5. Choose the shortest matching pattern above.
6. Output the cleaned message only unless explanation is requested.

Prefer:

```text
topic: A vs B → Δ n → action
```

or:

```text
topic: A: n | B: n | C: n → action
```

Avoid:

- long setup before the point
- repeated context
- unnecessary complete sentences
- JSON unless machine readability is required
- ambiguous `+/-` differences without a clear comparison direction
- explaining notation that is already obvious from context
