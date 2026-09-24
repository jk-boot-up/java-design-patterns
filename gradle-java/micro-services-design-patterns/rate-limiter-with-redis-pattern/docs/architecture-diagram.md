# Rate Limiter with Redis Pattern — Architecture Diagram

Many servers, one Redis. The bucket lives in Redis; the arithmetic on it happens in each server, with that server's clock.

![Rate Limiter with Redis Pattern — Architecture Diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart LR
    C["client-42, 90 searches"]
    LB["load balancer, deals in turn"]
    subgraph S["search servers, 3 or 6, each its own program"]
        S1["server-1: Bucket4j, own clock"]
        S2["server-2: Bucket4j, own clock"]
        S3["server-3: Bucket4j, clock one hour fast"]
    end
    subgraph Box["Redis 8.10.2, in a container the demo starts and stops"]
        K[("search-limit:client-42, tokens and last refill time, deletes itself when full")]
    end
    C --> LB
    LB --> S1
    LB --> S2
    LB --> S3
    S1 -- "read, sum, write only if unchanged" --> K
    S2 -- "read, sum, write only if unchanged" --> K
    S3 -. "refills with the wrong time" .-> K
```

</details>
