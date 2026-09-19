# Message Channel Pattern — Architecture Diagram

The sender and the receiver only know the channel.

![Message Channel Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    C["checkout"] -->|send| Q["channel: pick-orders"]
    Q -->|receive| W["warehouse"]
```

</details>
