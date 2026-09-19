# Active Object Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The worker is busy on a slow import. The checkout thread
calls reserve. The call packs the request into a message, drops it in the
mailbox, and returns a future straight away. The future is not done. The
import finishes, the worker takes the reserve message next, applies it, and
completes the future. The checkout thread, holding that future, now sees the
answer.

![Active Object pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout thread
    participant M as mailbox
    participant W as worker thread
    Note over W: busy on a slow import
    C->>M: reserve(1) becomes a message
    M-->>C: future, not done yet
    W->>M: import finishes, takes the next message
    W->>W: applies reserve, stock 49
    W-->>C: completes the future
```

</details>

The load-bearing sentence: **the call returned before the work started.**
