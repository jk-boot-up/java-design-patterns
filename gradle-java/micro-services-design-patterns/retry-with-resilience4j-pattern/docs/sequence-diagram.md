# Retry with Resilience4j Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. Checkout calls pay. The retry around pay calls the payments client. The retry around the client calls the gateway, which times out. The client waits and tries the gateway again, and again, three times in all, then throws. That failure reaches checkout's retry, which starts the whole thing again. The gateway is called nine times before the customer sees an error.

![Retry with Resilience4j pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant K as checkout
    participant P as payments client
    participant G as gateway
    K->>P: charge (attempt 1)
    P->>G: 3 attempts, all time out
    P-->>K: GatewayTimeout
    K->>P: charge (attempt 2)
    P->>G: 3 attempts
    K->>P: charge (attempt 3)
    P->>G: 3 attempts
    Note over G: 9 calls
```

</details>

The load-bearing sentence: **each retrying layer multiplies the one below it.**
