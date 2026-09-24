# Publisher-Subscriber with Redis Pattern — Architecture Diagram

Separate programs. The order service and every subscriber reach Redis over connections of their own, one of them from a second Java process. Redis keeps a pile of unread messages for each subscriber, and nothing else.

![Publisher-Subscriber with Redis Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    subgraph Shop["demo process"]
        O["order service"]
        E["email"]
        A["analytics, stops reading"]
    end
    subgraph Box["Redis 8.10.2, in a container the demo starts and stops"]
        C{{"channel orders.placed"}}
        PE[("pile for email")]
        PA[("pile for analytics, limit 1mb")]
        C --> PE
        C --> PA
    end
    subgraph Loy["second Java process"]
        L["loyalty points"]
    end
    O -- "publish once, told a count" --> C
    PE -- "own connection" --> E
    PA -. "past the limit: connection closed" .-> A
    C -- "own connection" --> L
```

</details>
