# Load Balancing with Spring Cloud LoadBalancer Pattern — Architecture Diagram

The caller names a service. The balancer picks a copy each time.

![Load Balancing with Spring Cloud LoadBalancer Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    C["caller: http://catalogue/..."] --> B["load balancer"]
    L["instance list from configuration"] --> B
    B --> A["copy-a"]
    B --> Bb["copy-b"]
    B --> Cc["copy-c, slow"]
```

</details>
