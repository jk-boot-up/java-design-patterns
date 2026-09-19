# Proxy with Spring Pattern — Architecture Diagram

A generated proxy sits between every caller and the real bean.

![Proxy with Spring Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    C["caller"] --> P["generated proxy"]
    P --> A["RoleAspect"]
    A --> B["real bean"]
    B -.->|this.render skips the proxy| B
```

</details>
