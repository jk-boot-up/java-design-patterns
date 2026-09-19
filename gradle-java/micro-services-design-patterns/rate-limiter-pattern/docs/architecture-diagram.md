# Rate Limiter Pattern — Architecture Diagram

Requests pass the limiter before they reach the service.

![Rate Limiter Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    C["callers"] --> L["rate limiter: a bucket each"]
    L -->|token taken| S["product search"]
    L -->|no token| R["429, retry after N ms"]
```

</details>
