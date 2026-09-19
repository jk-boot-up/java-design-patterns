# Specification Pattern — Architecture Diagram

One named rule, used by every feature that needs it.

![Specification Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    R["cheapAndAvailable"] --> S["search page"]
    R --> P["promotion"]
    R --> F["free shipping"]
    I["in stock"] --> R
    U["under £10"] --> R
    N["not discontinued"] --> R
```

</details>
