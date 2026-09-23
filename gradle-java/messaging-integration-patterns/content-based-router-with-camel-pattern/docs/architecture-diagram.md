# Content-Based Router with Camel Pattern — Architecture Diagram

Senders post to one queue. A Camel route reads it and posts each order on again. Receivers read only their own queue.

![Content-Based Router with Camel Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    S["the shop, posting orders"] --> Q["orders queue"]
    Q --> R["Apache Camel route"]
    R --> A["express-shipping"]
    R --> B["standard-shipping"]
    R --> C["digital-delivery"]
    R --> D["fraud-review"]
    R --> E["manual-review: the otherwise branch"]
    R --> F["router-errors: when a branch fails"]
    subgraph K["RabbitMQ, in a container"]
        Q
        A
        B
        C
        D
        E
        F
    end
```

</details>
