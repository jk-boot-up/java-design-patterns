# Queue-Based Load Leveling Pattern — Architecture Diagram

The burst goes into the queue. The worker takes from it at its own pace.

![Queue-Based Load Leveling Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    B["burst: 100 orders at once"] --> Q["queue"]
    Q -->|10 a tick| W["order service"]
    Q -.->|full: refused| R["refused"]
```

</details>
