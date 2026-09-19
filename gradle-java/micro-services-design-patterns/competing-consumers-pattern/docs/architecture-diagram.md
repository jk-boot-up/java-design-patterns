# Competing Consumers Pattern — Architecture Diagram

Consumers do not know each other. They know the queue.

![Competing Consumers Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    P["producers"] --> Q["one queue"]
    Q --> A["consumer A"]
    Q --> B["consumer B"]
    Q --> C["consumer C"]
    A --> D["shared database"]
    B --> D
    C --> D
```

</details>
