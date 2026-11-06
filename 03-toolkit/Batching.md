Yes. I'd treat **batching as only one member of a broader family: decomposition and concurrency strategies**.

The biggest distinction is:

> **Breaking work into smaller pieces does not itself make it faster.**  
> The speedup usually comes from reducing overhead/resource pressure, enabling **parallelism**, or both.

Spring Batch Reference explicitly separates chunking, partitioning, multi-threading, and parallel steps as different processing/scaling approaches. [[docs.spring.io]](https://docs.spring.io/spring-batch/reference/scalability.html)

### Useful taxonomy

```
ACCELERATING WORK
│
├── DECOMPOSE
│        │   Break large work into smaller units
│        │
│        ├── Batch
│        │   └── Process N items at a time
│        │
│        ├── Chunk
│        │   └── Break a stream/workload into manageable pieces
│        │
│        ├── Partition
│        │   └── Divide by logical boundaries
│        │            ├── ID range
│        │            ├── Date range
│        │            ├── Location
│        │            └── Source
│        │
│        ├── Shard
│        │   └── Distribute portions across independent resources
│        │
│        └── Segment
│            └── Generic logical subdivision
│
├── CONCURRENTLY EXECUTE
│        │   Work overlaps in time
│        │
│        ├── Parallelize
│        │   └── Multiple pieces execute simultaneously
│        │
│        ├── Multithread
│        │   └── Multiple threads process work
│        │
│        ├── Multiprocess
│        │   └── Multiple processes/workers
│        │
│        └── Fan-out
│            └── One task dispatches multiple independent tasks
│
└── DISTRIBUTE
         │   Spread work across resources
         │
         ├── Worker Pool
         ├── Load Balance
         ├── Remote Partition
         └── Distributed Processing
```

### The words I'd keep distinct

**Batching**

1,000,000 rows
      ↓
10,000 rows
10,000 rows
10,000 rows

Means **process in groups**.

It can help operationally without being parallel.

---

**Chunking**

Very similar, but I associate it more with **breaking a continuous workload into manageable processing units**. Some batch-processing frameworks explicitly use chunks as processing/commit units. [[docs.spring.io]](https://docs.spring.io/spring-batch/docs/4.3.8/reference/html/scalability.html)
```
Large workload
     ↓
[chunk][chunk][chunk][chunk]
```

---

**Partitioning**

More structurally meaningful:

```
10M rows
│
├── IDs 1–1M
├── IDs 1M–2M
├── IDs 2M–3M
└── ...
```

Partitions can then be independently processed, including in parallel. [[docs.spring.io]](https://docs.spring.io/spring-batch/reference/scalability.html)

So:

> **Batch = how much at once**  
> **Partition = which portion belongs together**

---

**Parallelization**

Now you're actually talking about **speed through simultaneous work**:

```
Sequential

A → B → C → D

Parallel
      ┌→ A ─┐
      ├→ B ─┤
START ├→ C ─┤→ DONE
      └→ D ─┘
```

A partitioned workload is particularly suitable for this because independent partitions can be assigned to separate workers. [[docs.spring.io]](https://docs.spring.io/spring-batch/reference/scalability.html)

---

**Fan-out / Fan-in**

One of my favorites for your orchestration vocabulary:

```
                  ┌→ Worker A ─┐
                  ├→ Worker B ─┤
Source → FAN-OUT ─┼→ Worker C ─┼→ FAN-IN → Result
                  └→ Worker D ─┘
```

Conceptually:

> **Fan-out = distribute independent work**  
> **Fan-in = recombine/coordinate the results**

### I'd use this vocabulary in your glossary

```
Decomposition
│
├── Batching                → group work into bounded sets
├── Chunking                → break work into manageable units
├── Partitioning            → divide work by logical boundaries
└── Segmentation            → generic subdivision
Execution
│
├── Sequential              → one after another
├── Concurrent              → overlapping execution
└── Parallel                → simultaneous execution
Distribution
│
├── Fan-out                 → distribute work
├── Worker Pool             → multiple processors consume work
├── Load Balance            → distribute workload across resources
└── Fan-in                  → aggregate/join results
```

``

And **`decompose → partition → parallelize`** is probably the cleanest phrase for the specific concept you're after:

```
MONOLITHIC WORKLOAD
        │
    Decompose
        ↓
    Partitions
    ↙     ↓  ↓   ↘
 W1     W2 W3  W4
    ↘     ↓  ↓   ↙
    Parallelize
            ↓
       COMPLETE
```

That lets you avoid calling every optimization "batching" when the material distinction may actually be **decomposition**, **partitioning**, or **parallelization**.