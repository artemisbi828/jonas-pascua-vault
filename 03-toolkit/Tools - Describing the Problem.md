
[Ontology]



**Procrastivity:** Doing "high-quality" work or research that serves as a sophisticated way of avoiding the actual task at hand.

**The "So What?" Factor:** Information that fails the "So what does this mean for our goal?" test.

**Niche-Hole:** Getting sucked into a specific, high-level detail that only matters to one person while the rest of the group waits.

**Expert Overspill:** When a specialist provides 100% of their knowledge when the group only needed 5%.

❌ -- `NO`
✅ -- vs `How do we get to YES?`


# Not Good Enough
**“this is currently reactive and brittle, and I’m proposing a deliberate framework to fix it”** without sounding accusatory or territorial.
- are not sufficient and require a more robust approach.
- are not meeting the required standard.
- need to be reworked.

```
In the current state, RBAC rules are being defined reactively rather than through a shared, well‑understood framework. This is evident in the volume of recurring Snowflake access issues, where users frequently cannot access the data required for their roles, resulting in ongoing tickets and manual intervention.

Given that the majority of these access requests and remediation efforts surface through the security and data teams, I’ve outlined this model not only to formalize Row‑Level Security (RLS), but also to serve as a guiding structure for RBAC more broadly. The intent is to move from implicit or ad‑hoc grants toward an explicit, auditable access model.

The involvement of the development team has not yet been fully articulated within this model, though DEV access is expected to follow the same explicit‑grant principles. Ongoing corrective mechanisms—such as nightly revocation of access for inactive or terminated employees—are considered essential to maintaining long‑term integrity and reducing manual clean‑up.
```

---
# Underlying or Hidden Issues → Latent Issues

> Some issues are **operationally observable**, surfacing through tickets when access is missing. Others are **latent by nature**, as excess access does not generate user complaints and only surfaces through audit or compliance review.

> Under‑entitlement produces **signal‑generating failures**, whereas over‑entitlement creates **signal‑silent risk** that remains latent until audited.


- **Under‑access** → _Observed / signal‑driven / ticket‑generating_
- **Over‑access** → _Latent / silent / audit‑revealed_

### **1. Latent (Unobserved) Issues**

Problems that **exist without generating complaints** and only surface through **audit or formal review**.

Strong, clinical terms:

- **Latent issues** ✅ (best general term)
- **Dormant risk**
- **Hidden control failure**
- **Unsignaled defects**
- **Audit‑discovered issues**
- **Compliance‑latent risk**

Example phrasing:

> “These risks are latent and do not surface operationally, as users have no incentive to report excess access.”

Access example:

> Users do not complain about **over‑entitlement**, but it represents a HIPAA exposure.

---

## Governance‑grade paired language (recommended)

This framing is especially effective:

> **Observed vs. Latent Risk**

Or:

> **User‑Signaled vs. Audit‑Revealed Issues**

Or:

> **Operationally Visible vs. Compliance‑Latent Issues**


### **2. Signal‑driven (Observed) Issues**

Problems that surface because **someone experiences friction and raises it**.

Common labels:

- **Reported issues**
- **Observed failures**
- **User‑signaled defects**
- **Operationally visible issues**
- **Reactive findings**

Example phrasing:

> “These issues are operationally visible and surface through user‑reported tickets or escalations.”

Access example:

> Users raise tickets because they **lack** access required to perform their role.