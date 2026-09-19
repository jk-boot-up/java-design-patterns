# Service Mesh Pattern — Architecture Diagram

Every service has a proxy. The proxies apply the policy.

![Service Mesh Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    C["checkout"] --- PC["proxy"]
    R["refunds"] --- PR["proxy"]
    PC -->|retry, identity, count| PP["proxy"]
    PR --> PP
    PP --- P["payments"]
    POL["policy, set in one place"] -.-> PC
    POL -.-> PR
    POL -.-> PP
```

</details>
