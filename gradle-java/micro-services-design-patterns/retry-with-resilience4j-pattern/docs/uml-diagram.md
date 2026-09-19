# Retry with Resilience4j Pattern — UML Sequence Diagrams

Four sequences.

## 1. A Recovered Call

![A Recovered Call](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant P as payments client
    participant G as gateway
    P->>G: attempt 1: timeout
    P->>P: wait 1 ms
    P->>G: attempt 2: timeout
    P->>P: wait 2 ms
    P->>G: attempt 3: R-1
```

</details>

## 2. A Lost Answer

![A Lost Answer](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant P as payments client
    participant G as gateway
    P->>G: charge, key K-5
    G-->>P: timeout (the charge happened)
    P->>G: charge again, key K-5
    G-->>P: R-1 (recognised, not charged again)
```

</details>

