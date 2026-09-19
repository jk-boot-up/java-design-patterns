# Content-Based Router Pattern — Architecture Diagram

Senders send to the router. Receivers read their own channel.

![Content-Based Router Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    S["senders"] --> R["content-based router"]
    R --> W["warehouse channel"]
    R --> D["digital delivery channel"]
    R --> F["fraud review channel"]
    R --> M["manual review: the fallback"]
```

</details>
