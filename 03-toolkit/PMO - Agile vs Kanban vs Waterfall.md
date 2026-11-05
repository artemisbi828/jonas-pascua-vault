
# 🧭 The Four Work Styles — Material Differences + Mini‑Stories

## **1. SCRUM — “Time‑boxed, team‑committed, iterative”**

**Core idea:**  
Work happens in fixed-length sprints (usually 2 weeks). The team commits to a defined scope, works in cross-functional collaboration, and inspects/adapts at regular ceremonies.

**How it feels:**  
Predictable cadence, structured rituals, sprint goals, and a shared commitment to finishing what was planned.

**Mini‑story:**  
A BI team starts a 2‑week sprint. They commit to building a new KPI, fixing two data quality issues, and updating a dashboard. Mid-sprint, a VP asks for a “quick” new metric. The team says, “We’ll evaluate it for next sprint.” Work is protected; scope is stable.

**Diagnostic signal:**  
If your team constantly changes priorities mid-sprint, or doesn’t actually commit to a sprint goal, you’re _not_ doing Scrum—regardless of what Azure DevOps board you use.

---

## **2. Kanban — “Continuous flow, pull-based, WIP-limited”**

**Core idea:**  
No sprints. Work flows continuously. The team pulls new work only when capacity frees up. WIP limits prevent overload.

**How it feels:**  
Smooth, steady, low-drama. Priorities can shift at any time because nothing is “locked” into a sprint.

**Mini‑story:**  
A data engineering team has a Kanban board with WIP limits: only 2 items in “In Progress.” A new urgent data fix comes in. They finish one item, then pull the urgent one next. No sprint commitments to break, no ceremonies to reschedule.

**Diagnostic signal:**  
If your team says “we do Scrum” but actually works on whatever comes in next, with no sprint boundaries, you’re doing Kanban.

---

## **3. Waterfall — “Sequential, gated, plan-first”**

**Core idea:**  
Work moves through predefined phases: requirements → design → build → test → deploy. You don’t go backward unless something breaks.

**How it feels:**  
Heavy upfront planning, long timelines, and a strong expectation that requirements won’t change midstream.

**Mini‑story:**  
A reporting project begins with a 4‑week requirements phase. Only after sign-off does the team design the semantic model. Only after that do they build. When the business changes a requirement halfway through, the PM says, “That will be a change request.”

**Diagnostic signal:**  
If your team insists on full requirements before starting, or treats changes as disruptions rather than normal, you’re closer to Waterfall.

---

## **4. Ad Hoc — “Reactive, unstructured, interrupt-driven”**

**Core idea:**  
No process. Work is done based on who yells loudest, what’s on fire, or what someone remembers.

**How it feels:**  
Chaotic. No prioritization, no WIP limits, no commitments, no predictability.

**Mini‑story:**  
A clinician emails a BI analyst directly asking for a new metric. The analyst starts working on it immediately. Halfway through, someone Slacks them about a broken dashboard, so they switch. Then a director calls about a data export. Everything is half-done, nothing is planned.

**Diagnostic signal:**  
If your team’s work is driven by interruptions, not a board or a plan, you’re in Ad Hoc territory—even if you _say_ you’re doing Scrum.

---

# 🧩 Quick Comparison Table

|Method|Cadence|How Work Starts|How Change Is Handled|Team Experience|
|---|---|---|---|---|
|**Scrum**|Fixed sprints|Planned & committed|Next sprint|Predictable, structured|
|**Kanban**|Continuous|Pulled when capacity frees|Anytime|Smooth, flexible|
|**Waterfall**|Sequential phases|After full requirements|Change request|Rigid, plan-heavy|
|**Ad Hoc**|None|Whoever asks loudest|Constantly|Chaotic, stressful|

---
## **Section 1 — Mental Model (Executive 1‑Pager)**

**TL;DR:**

- **Agile = philosophy (why + principles)**
- **Kanban = method (how to manage flow)**
- Kanban can be used **inside Agile**, but Agile ≠ Kanban.

---

### **1) Definition Table**

|Concept|Description|Example|
|---|---|---|
|**Agile**|A **set of principles and values** for building products iteratively, emphasizing adaptability, customer feedback, and continuous improvement. It is _not a specific process_ but a mindset.|A team releases small features weekly, adjusts based on user feedback, and reprioritizes backlog dynamically.|
|**Kanban**|A **workflow management method** that visualizes work, limits work-in-progress (WIP), and optimizes flow efficiency. It is a **concrete implementation tool**.|A board with columns (To Do → In Progress → Done) with WIP limits ensuring no stage gets overloaded.|

---

### **2) Relationships (Simple → Complex)**

1. **Work Management → Process → Framework → Philosophy**
    
    - Kanban = **Process / Method (tactical)**
    - Agile = **Philosophy (strategic)**
2. **Agile Ecosystem**
    
    - Agile  
        → Scrum (time-boxed framework)  
        → Kanban (flow-based method)  
        → XP (engineering practices)
3. **Layering**
    
    - Agile defines **principles**
    - Kanban operationalizes **flow optimization under those principles**

---

### **3) Why They Are Different**

|Dimension|Agile|Kanban|
|---|---|---|
|Nature|Philosophy|Method|
|Time Structure|Iterative (often sprints)|Continuous flow (no fixed iterations)|
|Change Cadence|Built into iteration boundaries|Anytime (real-time reprioritization)|
|Prescriptiveness|Low|Medium (explicit rules: WIP limits, flow metrics)|

---

### **4) Why the Distinction Matters (Exec Angle)**

- **Governance clarity:**  
    Confusing Agile with Kanban leads to misaligned expectations (e.g., expecting sprint velocity from a flow team).
- **Metrics integrity:**
    - Agile/Scrum → velocity
    - Kanban → cycle time, throughput
- **System design (your BI domain):**  
    Data models must reflect different **time semantics**:
    - Sprint-based (batch windows)
    - Flow-based (event streams)

---

### **5) Final Mental Model (Simple / ELI5)**

> **Agile = “Be flexible and learn fast.”**  
> **Kanban = “Make work visible and don’t overload yourself.”**

Or:

```
Agile = Operating System (philosophy)
Kanban = App (workflow engine)
```

---

## **Section 2 — ASCII Trees (Obsidian-ready)**

### **A. Hierarchy (Philosophy → Methods)**

```
Agile (Philosophy)
├── Scrum (Framework - Iterations)
│   ├── Sprint Planning
│   ├── Daily Standup
│   └── Retrospective
├── Kanban (Flow Method)
│   ├── Visual Board
│   ├── WIP Limits
│   └── Flow Metrics
└── XP (Engineering Practices)
    ├── Pair Programming
    ├── TDD
    └── Continuous Integration
```

---

### **B. Orthogonal Axes (Time Semantics)**

```
Time Model Axis
├── Iterative (Batch)
│   └── Scrum
└── Continuous (Flow)
    └── Kanban
```

---

### **C. Flow Lifecycle (Kanban)**

```
Backlog → Ready → In Progress → Review → Done
            ↑          ↓
        (WIP Limit Controls)
```

---

### **D. Agile Lifecycle (Conceptual)**

```
Plan → Build → Measure → Learn → Adjust → (repeat)
```

---

## **Section 3 — Deep Breakdown (Architect Lens)**

---

### **Agile**

**1) Purpose**

- Maximize responsiveness to change
- Deliver incremental value with feedback loops

**2) Scope**

- Organization-wide philosophy (product, engineering, ops, analytics)

**3) Dependencies**

- Strong stakeholder feedback loops
- Adaptive backlog prioritization
- Cultural buy-in

**4) Limitations**

- Ambiguity without implementation discipline
- Can degrade into “chaos” without structure

**5) Anti-Patterns (Critical)**

- “Fake Agile” → doing ceremonies without feedback loops
- Treating Agile as a strict process (it’s not)
- Measuring success via output instead of outcomes

---

### **Kanban**

**1) Purpose**

- Optimize flow efficiency
- Reduce bottlenecks and cycle time

**2) Scope**

- Team-level execution (can scale upward)

**3) Dependencies**

- Stable workflow states
- Accurate tracking of work items
- WIP policy enforcement

**4) Limitations**

- Weak on planning/forecasting without augmentation
- Can drift without continuous improvement discipline

**5) Anti-Patterns (Very Common)**

- **“Kanban board = Kanban” (wrong)**
- No WIP limits → loses core value
- Treating it like Scrum without sprints
- Ignoring flow metrics (cycle time, throughput)

---

## **Semantic Collisions (Where People Get Confused — Important for BI)**

|Collision|Reality|
|---|---|
|Agile = Scrum|Scrum is just one Agile framework|
|Kanban = board tool|Board ≠ methodology|
|Agile vs Kanban|Not competitors — different layers|
|Velocity vs Throughput|Different measurement systems|

---

## **Executive Takeaway**

- **Agile answers:** _“How should we think?”_
- **Kanban answers:** _“How should we move work?”_
- Combining both gives **adaptive + efficient systems**

---

## (Optional) For Your BI/Analytics Context

- **Agile teams** → backlog-driven dashboards, sprint-based KPIs
- **Kanban teams** → event-driven pipelines, real-time cycle tracking
- Strong opportunity: unify both in **semantic model → dual time grain (iteration + flow)**

---

## Want Examples?

I can generate **1–2 targeted examples** for:

- Power BI / Azure DevOps pipeline modeling
- Real-world team workflow (Scrum vs Kanban hybrid)

Just tell me which context you want.