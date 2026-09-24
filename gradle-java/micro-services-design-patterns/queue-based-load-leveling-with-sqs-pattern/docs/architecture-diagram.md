# Queue-Based Load Leveling with SQS Pattern — Architecture Diagram

The queue is not in anybody's process. Checkout puts orders on it, packers take them off, and it lives in SQS, played by LocalStack in one container the demo starts and stops.

![Queue-Based Load Leveling with SQS Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    subgraph Shop["checkout process"]
        C["checkout: 100 orders at once"]
    end
    subgraph Box["LocalStack 4.14.0, one container the demo starts and stops"]
        Q[("SQS queue: 100 waiting, then 90 waiting and 10 in flight")]
    end
    subgraph Packing["packing service processes"]
        A["packer A: 10 a round"]
        B["packer B"]
    end
    C -- "1. send, 10 to a request" --> Q
    Q -- "2. take up to 10, hidden for the visibility timeout" --> A
    A -- "3. delete after packing" --> Q
    Q -. "timeout ran out: handed out again" .-> B
```

</details>
