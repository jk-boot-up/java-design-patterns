# Blue-Green and Canary Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The rollout sets the green share to five percent. Traffic flows, and five in a hundred requests go to version two. The rollout counts version two's failures. One in five failed, which is twenty percent, above the gate. So the rollout halts, and sets the share back to zero. All traffic is on version one again.

![Blue-Green and Canary pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant O as rollout
    participant R as router
    participant G as v2
    O->>R: green share 5%
    R->>G: 5 of 100 requests
    G-->>O: 1 failed of 5, 20%
    O->>O: above the gate
    O->>R: green share 0%
```

</details>

The load-bearing sentence: **the rollout watches the failures, and moves the setting.**
