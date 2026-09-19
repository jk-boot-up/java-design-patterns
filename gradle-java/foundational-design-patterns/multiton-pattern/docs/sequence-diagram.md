# Multiton Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The order code asks for the UK warehouse. The map has none, so it makes one and keeps it. The reports code asks for the UK warehouse. The map has one, and returns the same object. Both now see the same stock.

![Multiton pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant O as order code
    participant W as Warehouse map
    participant R as reports
    O->>W: of(UK)
    W->>W: none yet: make and keep
    W-->>O: UK warehouse
    R->>W: of(UK)
    W-->>R: the same UK warehouse
```

</details>

The load-bearing sentence: **the first ask makes it, and every ask after gets the same one.**
