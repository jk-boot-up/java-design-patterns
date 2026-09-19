# Pipe and Filter Architecture Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. An order arrives, and waits in front of parse. Parse takes it, and takes one tick. It passes to the line in front of price. Price takes three ticks. While price works on it, parse is already working on the next order. The order then passes to pack, and comes out.

![Pipe and Filter Architecture pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant D as door
    participant P as parse
    participant R as price
    participant K as pack
    D->>P: order 1
    P->>R: order 1, after 1 tick
    D->>P: order 2
    Note over R: 3 ticks on order 1
    P->>R: order 2, waits
    R->>K: order 1
```

</details>

The load-bearing sentence: **each stage works on a different order at the same moment.**
