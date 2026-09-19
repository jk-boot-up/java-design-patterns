# Timeout Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The page starts a call to the supplier and waits up to a hundred milliseconds. The supplier has started, and is held. The time is up. The page stops waiting and shows stock unknown. Later the supplier finishes the work. Nobody is waiting for it, and the answer goes nowhere.

![Timeout pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant P as page
    participant S as supplier
    P->>S: stockOf(MUG-BLUE), wait up to 100 ms
    Note over S: started, held
    P-->>P: time is up
    P->>P: show: stock unknown
    S->>S: finishes later
    Note over P,S: nobody is waiting for the answer
```

</details>

The load-bearing sentence: **the caller stops waiting, and the supplier carries on.**
