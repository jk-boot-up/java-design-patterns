# Competing Consumers with RabbitMQ Pattern — Architecture Diagram

One queue in the broker, several pickers each on their own connection. An order is in one of three places: waiting in the queue, held by a picker and not yet said done, or gone. Prefetch decides how many a picker may hold.

![Competing Consumers with RabbitMQ Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    subgraph Shop["shop process"]
        C["checkout"]
    end
    subgraph Box["RabbitMQ 4.3.6, in a container on a random port"]
        Q[("queue pick-orders: waiting")]
        H1["held by picker A, not yet done"]
        H2["held by picker B, not yet done"]
        Q -- "hand over, up to prefetch" --> H1
        Q -- "hand over, up to prefetch" --> H2
    end
    subgraph P1["picker A process"]
        A["tray, then pick, then say done"]
    end
    subgraph P2["picker B process"]
        B["tray, then pick, then say done"]
    end
    C -- "send, then carry on" --> Q
    H1 --> A
    H2 --> B
    A -- "done: forget it" --> H1
    B -- "done: forget it" --> H2
    H1 -. "A crashes: all of it back, marked seen before" .-> Q
```

</details>
