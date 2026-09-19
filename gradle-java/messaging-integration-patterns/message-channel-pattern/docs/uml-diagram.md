# Message Channel Pattern — UML Sequence Diagrams

Four sequences.

## 1. A Full Channel

![A Full Channel](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout
    participant Q as channel of 5
    C->>Q: send x5
    Q-->>C: accepted
    C->>Q: send a sixth
    Q-->>C: ChannelFull
```

</details>

