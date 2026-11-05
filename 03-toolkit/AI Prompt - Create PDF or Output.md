The format the team wants is **number-for-number proof**, not a findings essay. A first draft organized by findings, changes and proof tables was rejected with "not what they would want to see". The version they loved put a dashboard screenshot for each location next to "Pulse says X, Ascend was Y, now Z, because W".

**No fluff:** no unit tests, CI, method narrative or process. The reader wants the number, the screenshot, the cause, and the query that proves it.

**Page 1: one summary table**, then 2-4 bullets of what changed.

**Queries appendix:** every number traces to a labelled query (Q1..Qn), referenced in each case's "What moved" and in the differences table. Run each query right before building and take the numbers from its output. Also save them as one `.sql` file next to the PDF.

### Rules
- **Facts only** (`feedback_team_docs_facts_only`): no names, no next steps, no "should".
- No em dashes. Money shown the way the dashboard shows it.
- Keep a short list of remaining differences only if asked, each with a cause.
- Screenshots are dashboard content only. Delete any capture that shows chat or desktop.