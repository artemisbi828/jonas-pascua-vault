or `NOLOCK`

SQL

SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;  

Show more lines

**What it does (ELI5)**

> “Don’t wait for writers. Just read what’s there.”

**Why it helps**

- Avoids blocking by inserts/updates
- Skips waiting on locks
- Big win on busy systems

**Best use**

- Analytics
- Reporting
- One‑off investigations
- “I just need a sense of the numbers”

⚠️ Risk: dirty / inconsistent reads  
✅ Totally fine for exploratory analytics