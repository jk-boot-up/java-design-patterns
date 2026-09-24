# Rate Limiter with Redis Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. A price-comparison robot called client-42 has one search left of its 10. Two of the shop's search servers get a search from it at almost the same moment. Server one asks Redis for client-42's bucket, and Redis answers: one token left. Server two asks too, before server one has written anything, and also hears: one token left. Server one takes the token and writes back a bucket with none left, but only on one condition: that the bucket in Redis is still exactly the one it read. It is, so the write lands and server one runs the search. Server two now tries the same conditional write. The bucket has changed since server two read it, so Redis turns the write down. Server two reads again, finds no tokens, and refuses the search, telling client-42 to come back in 60 minutes. One token, one search served, one refused.

![Rate Limiter with Redis sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S1 as server-1
    participant R as Redis key search-limit:client-42
    participant S2 as server-2
    S1->>R: read the bucket
    R->>S1: 1 token left
    S2->>R: read the bucket
    R->>S2: 1 token left
    S1->>R: write 0 tokens, only if still what I read
    R->>S1: landed
    Note over S1: search allowed
    S2->>R: write 0 tokens, only if still what I read
    R->>S2: turned down, it changed
    S2->>R: read again
    R->>S2: 0 tokens left
    Note over S2: refused, retry after 60 minutes
```

</details>

The load-bearing sentence: **every server spends from the one bucket in Redis, and a server's write lands only if nobody changed the bucket since it read it, so the last token is spent once.**

For the plain count that spends it twice, the fast clock and the rest of the failure modes, see [`uml-diagram.md`](uml-diagram.md).
