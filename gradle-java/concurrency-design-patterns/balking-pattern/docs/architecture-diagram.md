# Balking Pattern — Architecture Diagram

Callers ask; the draft decides whether to act.

![Balking Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    T["autosave timer"] --> D["draft"]
    B["Save button"] --> D
    D -->|needed, and free| S["storage: write"]
    D -.->|nothing new, or busy: returns at once| R["a result for the caller"]
```

</details>
