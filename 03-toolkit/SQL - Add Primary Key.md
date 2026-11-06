```sql
alter table dbo.Categories
alter column CategoryKey int not null
go

alter table dbo.Categories
add primary key (CategoryKey)
go

alter table std.Dates 
add constraint [PK__std__Dates] 
primary key clustered (DateKey)
go
```


---
#status/deferred/quick-paste-merge-later 
You haven't asked this specific question in our current session, but your memory is spot on—this is a classic debate in database design.

You are not "wrong" to prefer `int` or `bigint`. They are faster, take up less space, and as you noted, are much easier to read. However, the shift toward UUIDs (or hashes) is usually driven by specific problems that occur when an application starts to scale up or needs higher security.

Here is the breakdown of the "race condition" and "sequence agnostic" concepts you mentioned, and why they might force you away from integers.

### 1. The "Race Condition" (Centralized Bottleneck)

The issue with `int` is that it usually relies on **Auto-Increment**. To get the next ID (e.g., `#1001`), the database must lock the counter, increment it, and then release it.

- **In a single database:** This is fine. The database handles the locking.
    
- **In a distributed system:** If you have multiple database servers (sharding) or an offline-first mobile app, you have a problem. ==If Server A creates User `#50` and Server B also creates User `#50` at the same exact time, you have a **collision**==.
    

To prevent this with integers, you would need a central "Traffic Cop" server just to hand out numbers. This creates a bottleneck and a race to get the next number.

UUIDs solve this:

Because a UUID is mathematically guaranteed to be unique (1 in 340 undecillion chance of collision), Server A and Server B can generate IDs simultaneously without ever talking to each other. There is no race because they aren't competing for the "next" number.

### 2. What "Sequence Agnostic" Means

This refers to the fact that UUIDs do not require knowledge of the previous state of the database.

- **Integer (Sequence Dependent):** You cannot know that your ID is `#50` until the database tells you that `#49` was the last one used. You are dependent on the sequence.
    
- **UUID (Sequence Agnostic):** The application (or even the frontend client) can generate the ID _before_ the data is even sent to the database.
    

Why this matters:

It allows you to create complex relationships in your code before saving. For example, you can create a User and an Order object in your code, assign them both UUIDs, and link them together in memory before the database transaction ever happens.

### 3. The Security Argument (Enumeration)

This is the most common reason people switch, even for small apps.

If your URL looks like `myapp.com/user/105`, I can simply change the URL to `myapp.com/user/106` to see someone else's data. Even if you have permissions blocking me, I can:

- **Scrape your growth:** I can sign up today and get ID `#1000`, and sign up tomorrow and get ID `#1100`. Now I know exactly how many users you gained in 24 hours. Competitors love this data.
    
- **Guess identifiers:** It makes "Insecure Direct Object Reference" (IDOR) attacks much easier to execute.
    

### The Best of Both Worlds: Hybrid Approach

Since you prefer integers (and they _are_ better for database performance because they index faster), many developers use a hybrid strategy:

1. **Internal Primary Key (`bigint`):** Use this for all your Foreign Keys and Joins inside the database. It keeps your queries fast and your storage low.
    
2. **External Public ID (`uuid`):** Add a separate column for a UUID. Use _this_ one in your URLs, APIs, and public-facing interfaces.
    

**Would you like me to write a quick SQL snippet showing how to set up that "Hybrid" table structure?**