# Chain of Responsibility with Spring Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. A request comes in. The chain asks the address check, which has no opinion. It asks the stock check, which has no opinion. It asks the fraud check, which throws, because the service is down. The chain catches the exception and answers, referred, naming the fraud check. The payment limit check never runs.

![Chain of Responsibility with Spring pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant K as caller
    participant C as ScreeningChain
    participant A as address
    participant S as stock
    participant F as fraud
    K->>C: screen(request)
    C->>A: check (no opinion)
    C->>S: check (no opinion)
    C->>F: check
    F-->>C: throws
    C-->>K: REFERRED by fraud
```

</details>

The load-bearing sentence: **the walker decides what a failing link means.**
