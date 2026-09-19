# Load Balancing with Spring Cloud LoadBalancer Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The caller asks for a URL whose host is the name catalogue. The balancer asks for the list of instances, and the strategy picks one, say copy a. The request goes to copy a, and the answer comes back. The next request goes through the same steps, and the strategy picks a different copy.

![Load Balancing with Spring Cloud LoadBalancer pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant B as balancer
    participant A as copy-a
    participant Bb as copy-b
    C->>B: http://catalogue/...
    B->>A: request 1
    A-->>C: answer
    C->>B: http://catalogue/...
    B->>Bb: request 2
    Bb-->>C: answer
```

</details>

The load-bearing sentence: **the choice is made again for every request.**
