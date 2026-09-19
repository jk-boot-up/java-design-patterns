# Pessimistic Offline Lock Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. Clerk A asks the lock manager for the blue mug and gets it, with a fifteen minute expiry. Clerk B asks for the same lock, and the manager refuses and says A holds it. A edits and writes, and the store checks with the manager that A holds the lock, which it does. A lets go. B asks again, and now gets the lock.

![Pessimistic Offline Lock pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as clerk A
    participant B as clerk B
    participant L as lock manager
    participant S as store
    A->>L: acquire MUG-BLUE
    L-->>A: granted
    B->>L: acquire MUG-BLUE
    L-->>B: refused, locked by A
    A->>S: write
    S->>L: does A hold the lock?
    L-->>S: yes
    A->>L: release
    B->>L: acquire MUG-BLUE
    L-->>B: granted
```

</details>

The load-bearing sentence: **the clash never starts, because the second clerk is stopped at the door.**
