# Cache-Aside with Redis Pattern — Architecture Diagram

Two shop processes, one Redis, one database. Redis never talks to the database; each shop does the reading and the filling itself, and each sees what the other wrote.

![Cache-Aside with Redis Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TB
    A["first shop process"]
    B["second shop process"]
    subgraph Box["Redis 8.10.2, in a container the demo starts and stops"]
        K[("product:SKU-0 = 1000, expires in 60 s")]
        L[("lock:product:SKU-0, set with NX, expires in 5 s")]
        CLI["redis-cli, a third program"]
    end
    DB[("database, the source of truth")]
    A -- "get, then set on a miss" --> K
    B -- "get, then set on a miss" --> K
    A -. "refill guard" .-> L
    B -. "refill guard" .-> L
    CLI -. "reads the same key" .-> K
    A -- "read on a miss" --> DB
    B -- "read on a miss" --> DB
```

</details>
