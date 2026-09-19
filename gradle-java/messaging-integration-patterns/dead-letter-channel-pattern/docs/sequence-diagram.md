# Dead Letter Channel Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The worker takes order two. It tries to read the body, and fails. It tries again, and fails. It tries a third time, and fails. The limit is three, so the worker moves order two to the dead letter channel, with the number of attempts and the last error. Then it takes order three, which is fine, and goes on.

![Dead Letter Channel pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant W as worker
    participant H as handler
    participant D as dead letters
    W->>H: ORD-2 (attempt 1)
    H-->>W: fails
    W->>H: ORD-2 (attempt 2)
    H-->>W: fails
    W->>H: ORD-2 (attempt 3)
    H-->>W: fails
    W->>D: ORD-2, 3 attempts, last error
    W->>H: ORD-3, and on
```

</details>

The load-bearing sentence: **the worker gives up on one message so that it does not give up on all of them.**
