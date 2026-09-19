# Cache-Aside Pattern — Architecture Diagram

The cache sits beside the path to the database, not in front of it.

![Cache-Aside Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    A["application"] -->|1 ask| C["cache"]
    A -->|2 on a miss| D["database"]
    A -->|3 remember| C
```

</details>
