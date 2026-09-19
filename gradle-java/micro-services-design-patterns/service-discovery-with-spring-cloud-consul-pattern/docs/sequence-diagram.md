# Service Discovery with Spring Cloud Consul Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. A copy of Pricing starts and registers with Consul, with a health check. Consul calls the health endpoint every interval and records passing. The copy crashes. The client asks Consul for healthy copies, and Consul still lists it, because the last check passed. The client sends a request to it and fails. On the next check Consul calls the endpoint, gets no answer, marks it critical, and stops listing it.

![Service Discovery with Spring Cloud Consul pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant P as pricing-2
    participant C as Consul
    participant K as client
    P->>C: register, with a health check
    C->>P: check: passing
    P--xP: crashes
    K->>C: healthy copies?
    C-->>K: pricing-2 (stale)
    K->>P: request fails
    C->>P: check: no answer, critical
    K->>C: healthy copies?
    C-->>K: without pricing-2
```

</details>

The load-bearing sentence: **the list is only as fresh as the last check.**
