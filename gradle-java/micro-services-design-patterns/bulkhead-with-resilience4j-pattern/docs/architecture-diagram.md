# Bulkhead with Resilience4j Pattern — Architecture Diagram

Each kind of work passes through its own compartment.

![Bulkhead with Resilience4j Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    F["supplier feed"] --> BF["feed compartment: 2 permits"]
    C["checkout"] --> BC["checkout compartment: 4 permits"]
    BF --> P["slow partner API"]
    BC --> S["checkout logic"]
```

</details>
