# Leader Election Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. A holds the lease with token one. A pauses. Its lease expires. B asks the store and is granted the lease with token two. B sends the report with token two, and the sink records it. A wakes, still believing it leads, and sends with token one. The sink has seen token two, so it refuses A's write. Only B's report was sent.

![Leader Election pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as node A
    participant S as lease store
    participant B as node B
    participant K as report sink
    A->>S: acquire (token 1)
    Note over A: pauses, lease expires
    B->>S: acquire
    S-->>B: lease, token 2
    B->>K: write, token 2
    A->>K: write, token 1
    K-->>A: refused: 1 is older than 2
```

</details>

The load-bearing sentence: **the thing being written to is the last line of defence against a stale leader.**
