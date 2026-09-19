# Blue-Green and Canary Pattern — Architecture Diagram

One router. Two releases. A setting decides the share.

![Blue-Green and Canary Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    C(["customers"]) --> R{"router: green share"}
    R -->|95%| B["blue: v1"]
    R -->|5%| G["green: v2"]
    B --> DB[("one database")]
    G --> DB
```

</details>
