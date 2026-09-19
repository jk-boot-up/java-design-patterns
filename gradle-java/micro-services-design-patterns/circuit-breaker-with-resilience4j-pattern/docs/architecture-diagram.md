# Circuit Breaker with Resilience4j Pattern — Architecture Diagram

The proxy asks the breaker before a call reaches the service.

![Circuit Breaker with Resilience4j Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    P["product page"] --> X["Spring proxy"]
    X --> B["circuit breaker: window, threshold"]
    B -->|closed or probe| S["recommendations service"]
    B -->|open| F["fallback: empty list"]
    S -->|failure| B
```

</details>
