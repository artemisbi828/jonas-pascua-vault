```
Restaurant Manager (Scheduler + Trigger)
        ↓
Head Chef (Orchestrator)
        ↓
Cook (Runner / Executor) -- Executes a task
        | 
        | runs
        ↓ 
Recipe (SQL Query)        
        | 
        | produces
        ↓ 
Dish (Dataset)
        ↓
Takeout Box (CSV/Parquet)
```

| Component | Description | 
| - | - | 
|  Trigger | Event that starts something | 
|  Scheduler | Decides when to start | 
|  Orchestrator | Coordinates multiple tasks | 
|  Executor | Executes a task | 
|  Definition | Describes the work | 
|  Artifact | Output of the work | 
