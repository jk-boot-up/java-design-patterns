# Active Object with Spring Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The worker has read the stock, which is zero, and is holding it while it does a slow step. A caller then adds five through this. That call skips Spring's proxy, so it runs right there on the caller's own thread, and changes the field to five. The worker finishes its slow step and writes what it read, zero, plus ten. The five is gone. Nothing failed, and nothing was logged.

![Active Object with Spring pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant W as worker thread
    participant F as stock field
    participant C as caller thread
    W->>F: read: 0
    Note over W: holding the old value
    C->>F: this.restock(5): stock is 5
    W->>F: write 0 + 10
    Note over F: 10, not 15
```

</details>

The load-bearing sentence: **the lock-free design holds only for the calls that go through the proxy.**
