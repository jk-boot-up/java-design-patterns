# Message Channel with RabbitMQ Pattern — Architecture Diagram

Three processes, not one. The message lives in the broker, which neither the shop nor the warehouse owns, and what survives a restart is decided twice.

![Message Channel with RabbitMQ Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    subgraph Shop["shop process"]
        C["checkout"]
    end
    subgraph Box["RabbitMQ 4.3.6, in a container the demo starts and stops"]
        X["default exchange"]
        Q[("queue pick-orders, durable")]
        D[("disk: persistent messages only")]
        X --> Q
        Q -. written down .-> D
    end
    subgraph Wh["warehouse process, may not exist yet"]
        W["picker"]
    end
    C -- "send, then carry on" --> X
    Q -- "hand over one order" --> W
    W -- "acknowledgement: done" --> Q
    W -. "crash, no acknowledgement" .-> Q
```

</details>
