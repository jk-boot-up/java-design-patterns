# Balking Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The timer calls save. The draft has a new edit and no save running, so it records the version and starts writing. While the write is held, the customer clicks Save. The draft sees a save is running and returns already saving, at once. The customer edits again, and the version moves on. When the first write finishes, the draft marks clean only up to the version it saved, so it is still dirty, and the next save writes the new edit.

![Balking pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant T as timer
    participant D as draft
    participant S as storage
    participant C as customer
    T->>D: save()
    D->>S: write version 1 (held)
    C->>D: save()
    D-->>C: ALREADY_SAVING
    C->>D: edit (version 2)
    S-->>D: write done
    D->>D: clean up to version 1 only
    T->>D: save(): writes version 2
```

</details>

The load-bearing sentence: **the version is what keeps the edit made during a save from being lost.**
