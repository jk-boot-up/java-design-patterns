# Message Channel Pattern — Data Flow Diagram

What happens to a message sent to the channel.

![Message Channel Pattern — Data Flow Diagram](images/data-flow-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TD
    Send(["send(message)"])
    T{"right type?"}
    Wrong(["WrongType: refused"])
    F{"room in the channel?"}
    Full(["ChannelFull: refused"])
    Q["queued, and the sender carries on"]
    R["a receiver takes it later, once"]
    Send --> T
    T -- no --> Wrong
    T -- yes --> F
    F -- no --> Full
    F -- yes --> Q --> R
```

</details>
