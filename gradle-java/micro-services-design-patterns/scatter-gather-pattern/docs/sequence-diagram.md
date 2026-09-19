# Scatter-Gather Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The page asks the gatherer for the best price, with a deadline of five hundred milliseconds. The gatherer sends the question to Acme, Beta, Cargo and Delta at the same moment. Acme, Beta and Cargo answer straight away. Delta does not. When the deadline arrives, the gatherer stops waiting for Delta, records it as too slow, and returns three quotes and one missing supplier. The page shows the best of the three.

![Scatter-Gather pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant P as page
    participant G as gatherer
    participant S as four suppliers
    P->>G: ask, deadline 500 ms
    G->>S: the question, to all at once
    S-->>G: Acme 1250, Beta 1190, Cargo 1340
    Note over S: Delta does not answer
    G-->>P: 3 quotes, missing: Delta (too slow)
    P->>P: show the best: Beta 1190
```

</details>

The load-bearing sentence: **the gatherer decides when to stop waiting, not the slowest supplier.**
