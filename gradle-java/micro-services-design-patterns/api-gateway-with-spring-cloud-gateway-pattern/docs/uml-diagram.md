# API Gateway with Spring Cloud Gateway Pattern — UML Sequence Diagrams

Four sequences.

## 1. A Request Without A Token

![A Request Without A Token](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as client
    participant G as gateway
    participant S as any service
    C->>G: GET /api/catalogue/...
    G-->>C: 401
    Note over S: never called
```

</details>

## 2. A Slow Service

![A Slow Service](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as client
    participant G as gateway
    participant P as pricing
    C->>G: GET /api/pricing/...
    G->>P: forward
    Note over G,P: no answer within the timeout
    G-->>C: 504
```

</details>

