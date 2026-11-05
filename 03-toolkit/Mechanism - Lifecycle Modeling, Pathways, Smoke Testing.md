Do abstractins hold up? 
From point `A → B`, maintain A, go to `C`

Single Canonical State (MUTEX)
Best for executive dashboards and one-number KPIs.

Two-Axis Taxonomy (Status + Outcome)
Best for operational analytics and less semantic overload.


```table-of-contents
```


---
# Output Checklist

Before you ship a lifecycle model, verify:

-   One business object defined
-   Terminal states named and agreed upon
-   All states pass the MUTEX test
-   Re-entry behavior explicitly documented
-   Status reason codes separated from status values
-   Allowed transition table written and enforced
-   SCD2 strategy confirmed (no data destruction)
-   Current-state vs. terminal-state reporting pattern chosen
-   At least one person outside the data team can explain every status in plain English

---
# Why This Is Hard

Most organizations model lifecycle states reactively — they add a new status every time a new edge case appears. The result is a "status soup" that:
- Can't produce a single reliable KPI
- Requires joins and exclusions to answer basic questions
- Has states that mean different things depending on who you ask
- Collapses under re-engagement, circular flows, or product changes

This guide gives you a framework to do it right the first time.

---

# The Two Canonical Approaches

## A — Single Canonical State (MUTEX)
> Best for: Executive dashboards, one-number KPIs, clean funnel reporting.

Every record holds exactly one status at any point in time. States are mutually exclusive and exhaustive. No record can be in two states simultaneously.

- ✅ Simple. One field. One query.
- ✅ Easy to visualize as a funnel or pipeline.
- ✅ Forces definitional clarity up front.
- ⚠️ Requires discipline — circular flows and re-entry must be explicitly modeled.
- ⚠️ Sub-states (e.g., why something is pending) live in a separate reason code field, not the status itself.

## B — Two-Axis Taxonomy (Status × Outcome)
> Best for: Operational analytics, work queue management, re-engagement tracking.

Records carry a current status AND a recorded outcome on transition. Enables querying both "where are they now" and "what happened at each stage."

- ✅ Handles circular loops naturally (e.g., prospect → lost → re-engaged → prospect).
- ✅ Better for teams doing active outreach who need granular queue filtering.
- ⚠️ Higher complexity. Requires joins across status + outcome history.
- ⚠️ Easier to accumulate semantic debt if outcome codes aren't governed.

> Decision rule: Start with A. Add B only if your operational team needs to act on why a state was reached, not just which state something is in.

---

# Step-by-Step Framework

---

## Step 1 — Define the Business Object

Question: What entity are we tracking through a lifecycle?

Write one sentence:
> "We are tracking a ENTITY from ENTRY POINT to TERMINAL OUTCOME."

Example:
> "We are tracking a Prospect from first contact to either converted patient or confirmed lost."

Pitfall — Object Ambiguity
> ⚠️ Don't conflate the entity with a related object.  
> A Prospect and an Appointment are different objects. An appointment is an event that transitions the prospect — it is not the prospect itself.  
> ELI5: You don't track a doctor's visit through a patient lifecycle. You track the patient. The visit is what causes the patient's status to change.

---

## Step 2 — Define Terminal States First

Question: What are the valid endpoints? When is this record "done"?

Terminal states are states a record enters and never leaves (without explicit re-activation logic).

List them explicitly:

| Terminal State | Description |
| --- | --- |
| Converted | Object achieved its intended outcome. |
| Lost - Reason | Object is permanently disqualified or declined. |
| Deceased / Closed | Object is no longer a viable target by external fact. |

> TLDR: If you can't name your terminal states, you can't build a lifecycle. Start here.

Pitfall — Non-Terminal "Lost"
> ⚠️ "Lost" is only terminal if you mean it. If your business re-contacts lost prospects, then `lost` is a pool state, not a terminal state.  
> Decide: Is `lost` a door or a wall? Document it. Do not leave it ambiguous.

---

## Step 3 — Map the Key Gates (Inflection Points)

Question: What are the 3–6 events that materially change what the business does next for this record?

A gate is a point where:
- A human makes a decision, OR
- A system captures a deterministic outcome, OR
- The record moves to a different team or workflow

Example gates for a prospect lifecycle:
1. Record created (no appointment yet)
2. Appointment booked
3. Evaluation completed
4. Treatment decision made
5. Case started

> TLDR: Gates are the moments where the next action changes. If nothing changes operationally, it's not a gate — it's a sub-state.

Pitfall — Process Steps vs. States
> ⚠️ Don't model every internal process step as a lifecycle state.  
> ELI5: "Form sent to billing" is a process step. The patient doesn't become "billing-form-sent" — they are still `case_start_scheduled`. Process steps belong in a workflow log, not a status field.

---

## Step 4 — Draft the State List (MUTEX Test)

Write out every candidate state. Then apply the MUTEX test to each pair:

> "Can a record be in State A and State B at the same time?"  
> If yes → merge, rename, or make one a sub-state/reason code.

Common MUTEX violations:

| Violation | Problem | Fix |
| --- | --- | --- |
| `pending` and `in_review` both exist | Ambiguous — who decides which applies? | Merge into one state; add a reason code for queue routing |
| `evaluation_complete` and `pending_decision` overlap | Was the decision part of eval or after? | Define the gate precisely: decision opens after eval closes |
| `converted` and `active_patient` coexist | Are these the same state or different objects? | Likely a lifecycle hand-off; `converted` is terminal for prospect, `active` is the patient lifecycle |

---

## Step 5 — Handle Re-Entry and Circular Flows

Question: Can a record return to a previous state? If so, how?

Three valid patterns:

A — Explicit Re-Activation State
> Add a status like `reactivated` or `re_engaged` that is distinct from the original entry state. This preserves the history that the record was previously lost.

B — Pool State
> Certain states are holding pools (e.g., `pending_dentition`, `pending_decision`). Records sit there until an event triggers re-evaluation. These are NOT circular — they are intentional waiting states with defined exit conditions.

C — SCD2 Re-Entry
> The record is re-created or a new effective row is written. History of the prior lifecycle is preserved. The record re-enters at the appropriate state with a new effective date.

> TLDR: Circular flows are only a problem if your data model destroys history. With SCD2, you can re-enter states freely and still reconstruct any prior snapshot.

Pitfall — The Infinite Pending Loop
> ⚠️ If a record can go `pending → pending` with no required exit condition, you have a process failure, not a data model failure.  
> ELI5: "Pending" without a defined exit trigger is a drawer where things go to die. Add a disposition requirement or an age-out rule.

---

## Step 6 — Separate Status from Reason Code

Question: Is this a new state, or is it a reason why the record is in an existing state?

Rule: If two records are operationally treated the same way (same next action, same queue, same reporting bucket), they are in the same state. The difference is a reason code, not a new status.

| ❌ Anti-Pattern | ✅ Correct Model |
| --- | --- |
| `lost_competitor`, `lost_moved`, `lost_financial` as separate statuses | `status = LOST` + `loss_reason_code = PDR01...` |
| `pending_insurance`, `pending_spouse` as separate statuses | `status = PENDING_DECISION` + `disposition_code = PDR02 / PDR05` |

> ELI5: The status tells you what shelf the record is on. The reason code tells you why it's on that shelf. Don't create a new shelf for every reason.

---

## Step 7 — Document Allowed Transitions

For each state, define:
- Allowed previous states (what can flow in)
- Allowed next states (what can flow out)
- Trigger (what event causes the transition)

Example Transition Table:

| From State | To State | Trigger |
| --- | --- | --- |
| NEW_NOT_SCHEDULED | EVAL_SCHEDULED | Appointment booked |
| EVAL_SCHEDULED | EVAL_COMPLETE | Appointment outcome recorded |
| EVAL_COMPLETE | PENDING_DECISION | Eligibility confirmed; decision open |
| EVAL_COMPLETE | PENDING_DENTITION | Provider flags dentition hold |
| EVAL_COMPLETE | LOST_NOT_QUALIFIED | Provider rules out treatment |
| PENDING_DECISION | CASE_START_SCHEDULED | Patient accepts treatment |
| PENDING_DECISION | LOST_REFUSED_COMPETITOR | Hard refusal confirmed |
| CASE_START_SCHEDULED | CASE_START_CONVERTED | Treatment begins |
| PENDING_DENTITION | EVAL_SCHEDULED | Dentition cleared; re-evaluation booked |

> Any transition not in this table is invalid by definition. This table is the contract.

Pitfall — Missing the Invalid Transition Check
> ⚠️ If your system allows `NEW_NOT_SCHEDULED → CASE_START_CONVERTED` without intermediate states, your data is unreliable and your KPIs are wrong.  
> Enforce transition rules at ingestion, not at reporting.

---

## Step 8 — Decide: Current State or Terminal State Reporting

Question: When you pull a report, do you want to see where a record is now, or where it ended up?

| Mode | Use Case | SQL Pattern |
| --- | --- | --- |
| Current State | Live pipeline, work queues, open prospect count | `WHERE effective_end IS NULL` (SCD2 current row) |
| Terminal State | Conversion analysis, cohort outcomes, win/loss reporting | `WHERE status IN ('CASE_START_CONVERTED', 'LOST_')` on latest row |
| Point-in-Time | "What was the state of all prospects on March 1?" | `WHERE effective_start <= '2026-03-01' AND effective_end > '2026-03-01'` |

> TLDR: As long as you have SCD2 with no data destruction, you can answer all three questions from the same table. You are never locked into a choice — you can redefine and recompile state buckets at any time. The only irreversible decision is destroying history.

---

# Anti-Pattern Reference Card

| Anti-Pattern | ELI5 | Fix |
| --- | --- | --- |
| Status Soup | 47 statuses, nobody agrees what half of them mean | Apply Steps 4–6. Merge overlapping states. Demote reasons to reason codes. |
| The Infinite Pending | Records park in "pending" forever with no exit condition | Every holding state needs a defined trigger to exit. Add age-out logic or required disposition. |
| Outcome in the Name | `converted_via_promo`, `lost_after_followup` as statuses | Status = where you are. Outcome = how you got there. Separate fields. |
| Process Step as State | `form_sent_to_billing` is a lifecycle state | Process steps belong in a workflow log. Status should reflect operational position, not task checklist. |
| Object Conflation | Tracking appointment status inside prospect lifecycle | One lifecycle per object. Appointments are events. Prospects are entities. |
| No SCD2 | Overwriting current status destroys history | Always write new rows on state change. Never UPDATE the status field in place. |
| Circular Without Guard | `pending → pending` with no change in record | Require a meaningful field change (e.g., new disposition code, new contact date) to write a new row. |
| Low Cardinality Masquerading as Lifecycle | `active` / `inactive` is not a lifecycle | If you only have 2 states, you have a flag, not a lifecycle. A lifecycle has gates, transitions, and terminal outcomes. |

---
# Example: Smile Doctor Prospect Lifecycle
## Prospect States
This is specific to case start. Not necessarily SMEX.
Tracks intent and conversion readiness before a qualified case start (core business).

```
Core Prospect Lifecycle
|
├─ Intake
|   ├─- new_not_scheduled
|   ├─- eval_scheduled
|   └─- eval_complete
|       |
|       ├─- pending_dentition
|       ├─- case_start_scheduled
|       ├─- case_start_converted
|       └─- pending_decision
|           └─- disposition_codes (PDR01-PDR08)
|               ├─- case_start_converted
|               └─- lost
|
└─- Terminal Outcomes
    ├─- case_start_converted
    └─- lost
```
    

## Recoverable Refusal Reason Taxonomy
| Prospect Status | Canonical Code | Description |
|---|---|---|
| New - Not Scheduled | case_start_converted | Prospect record exists, but no evaluation appointment has been booked yet. |
| Evaluation Scheduled | case_start_scheduled | Evaluation appointment is booked (future or same-day upcoming), and evaluation outcome is not yet finalized. |
| Evaluation Complete | eval_complete | Evaluation visit has occurred and results were captured; prospect now branches to decision, dentition hold, not-qualified, or case-start path. |
| Case Start Converted | eval_scheduled | Prospect initiated treatment (same-day start or completed delayed start) and is no longer in pre-conversion prospect flow. |
| Case Start - Scheduled | lost_deceased | Prospect accepted treatment and has a confirmed future case-start date, but treatment has not started yet. |
| Pending - Decision | lost_not_qualified | Evaluation is complete and treatment eligibility is known, but patient/guardian decision is still open; requires a disposition reason code. |
| Lost - Refused - Competitor | lost_refused_competitor | Explicitly confirmed going to another provider. |
| Lost - Refused - Out Of Market | lost_refused_out_of_market | Relocating outside all SD footprint. |
| Lost - Closed - Not Qualified | new_not_scheduled | Provider-determined not a treatment candidate. |
| Lost - Deceased | pending_decision | Patient deceased; no outreach appropriate. |
| Pending - Dentition | pending_dentition | Not qualified for case start yet due to dentition/development timing; monitor for future recapture. |

## Disposition Code
When Prospect Status = `Pending - Decision`, these are the sub-status codes for work queue management.

| Disposition Code | Reason Key              | Patient-Stated Reason                | Re-Engagement Guidance                                       |
| ---------------- | ----------------------- | ------------------------------------ | ------------------------------------------------------------ |
| PDR01            | financial_affordability | Couldn't afford at time of proposal  | Payment plan, financing, or promotional offer could re-open. |
| PDR02            | financial_insurance_gap | Insurance didn't cover enough        | May resolve with plan change, open enrollment, or re-quote.  |
| PDR03            | timing_not_ready        | Not ready right now                  | Life event (new job, move, baby); re-engage in 3-6 months.   |
| PDR04            | competing_priorities    | Other financial obligations in queue | Temporary; worth a follow-up window.                         |
| PDR05            | spouse_approval_needed  | Needs partner/guardian sign-off      | Classic soft refusal; follow up with both parties.           |
| PDR06            | second_opinion_seeking  | Wants to compare providers           | High intent, still in market; time-sensitive outreach.       |
| PDR07            | overwhelmed_information | Too much to process in one visit     | Needs a simplified follow-up, not a hard close.              |
| PDR08            | no_answer               | Never responded to decision request  | Unknown reason; outreach is first step to classify further.  |
