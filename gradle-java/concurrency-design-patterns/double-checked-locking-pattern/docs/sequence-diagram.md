# Double-Checked Locking Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. Thread A and thread B both ask for the price list, and both see that it is missing. Thread A takes the lock, looks again, finds nothing, builds the price list, stores it in the volatile field and releases the lock. Thread B then gets the lock, looks again, and finds the price list already there, so it does not build one. Both threads have the same price list, and it was built once.

![Double-Checked Locking pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as thread A
    participant L as lock
    participant B as thread B
    participant F as volatile field
    A->>F: read: missing
    B->>F: read: missing
    A->>L: take
    A->>F: read again: missing
    A->>F: build, store
    A->>L: release
    B->>L: take
    B->>F: read again: built
    B->>L: release
```

</details>

The load-bearing sentence: **the second check is what stops the second build.**
