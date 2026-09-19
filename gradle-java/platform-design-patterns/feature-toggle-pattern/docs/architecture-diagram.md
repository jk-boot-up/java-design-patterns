# Feature Toggle Pattern — Architecture Diagram

The checkout asks the table at run time. The table can be changed without a deploy.

![Feature Toggle Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    C["checkout, deployed once"] -->|isOn gift-wrap, customer| T[("toggle table")]
    A["someone with access"] -->|changes a rule| T
```

</details>
