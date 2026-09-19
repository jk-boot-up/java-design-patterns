# Two-Phase Termination Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The shop tells the worker to stop. The worker is in the middle of order one, having written line one. It carries on, writes lines two and three, and ends the order. At the top of the loop it checks the request, finds it, and does not start order two. It runs its cleanup and ends. The shop, which has been waiting up to five seconds, sees the worker has ended.

![Two-Phase Termination pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S as shop
    participant W as worker
    participant L as ledger
    W->>L: ORD-1 line 1
    S->>W: request stop
    W->>L: ORD-1 lines 2 and 3
    W->>W: check: stop requested
    W->>W: cleanup, and end
    S->>W: awaitStop(5000)
    W-->>S: ended
```

</details>

The load-bearing sentence: **the worker finishes the unit of work before it ends.**
