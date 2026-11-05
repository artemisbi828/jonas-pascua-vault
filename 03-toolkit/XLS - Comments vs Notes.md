#status/deferred/quick-paste-merge-later 

Excel actually has **two different annotation systems** now — **Notes** (the old yellow sticky‑note style) and **Comments** (the modern threaded chat‑style). They serve different purposes, and choosing the right one makes your workbook cleaner and more maintainable.

Here’s the breakdown in a way that fits how you think about structure, clarity, and workflow design.

---

# 🟨 **Notes** (formerly “Comments” in older Excel)

**Best for:**

- Static explanations
- Documentation
- Field definitions
- Instructions for users
- Data dictionary–style metadata
- Anything that should _not_ trigger a conversation

### **Pros**

- Simple, unobtrusive, lightweight
- Ideal for documenting input fields (“Enter amount in USD”, “Pick from Accounts list”)
- Works consistently across Excel Desktop, Mac, and Online
- Doesn’t clutter the sheet with conversation bubbles
- Can be printed if needed
- Perfect for your intake form’s “field help” or “business rule” annotations

### **Cons**

- No threading or replies
- Not good for collaboration or back‑and‑forth discussion
- No @mentions
- Not ideal for audit trails or decision history

---

# 💬 **Comments** (modern threaded comments)

**Best for:**

- Collaboration
- Review cycles
- Asking questions about data
- Tagging teammates
- Tracking decisions or issues
- Temporary discussions that will eventually be resolved

### **Pros**

- Threaded conversations
- @mentions notify people
- Good for review workflows
- Great for “Why is this number off?” or “Can you verify this account?”
- Works well in Excel Online for team collaboration

### **Cons**

- Not meant for documentation
- Clutters the sheet visually with purple indicators
- Threads can get messy if used as permanent notes
- Harder to maintain long‑term
- Not ideal for stable metadata or instructions

---

# 🎯 **When to use which (practical guidance)**

### **Use Notes for:**

- Explaining what a column means
- Giving instructions for data entry
- Documenting business rules
- Adding metadata to your Accounts table
- Clarifying validation rules
- Anything that should persist as part of the “data model”

This aligns with your preference for **architectural clarity and ergonomic documentation**.

### **Use Comments for:**

- Asking a teammate to review a row
- Flagging an issue (“This account looks duplicated”)
- Discussing a discrepancy
- Temporary collaboration during development
- Anything that should eventually be resolved and removed

This aligns with **workflow communication**, not documentation.

---

# 🧠 Jonas‑specific recommendation

For your intake pipeline:

- **Use Notes** to document:
    
    - What “Account” means
    - How to propose new accounts
    - Sanitization rules
    - What “Amount” expects
    - What “CreatedAt” and “SysUser” represent
- **Use Comments** only when collaborating with others on the workbook, e.g.:
    
    - “Can you confirm this account belongs to the Ortho category?”
    - “This row looks duplicated — please check.”

This keeps your workbook clean, scalable, and aligned with your controlled‑vocabulary + referential‑integrity mindset.

---

If you want, I can help you design a **documentation pattern** using Notes that makes your Excel intake form feel like a proper data-entry UI — consistent, ergonomic, and self‑explanatory.