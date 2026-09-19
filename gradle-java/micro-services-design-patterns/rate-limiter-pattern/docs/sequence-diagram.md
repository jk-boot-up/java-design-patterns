# Rate Limiter Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. A client sends a request. The limiter finds that client's bucket and works out how many tokens have been earned since the last request, without going over the size. There is one token, so it takes it and passes the request on. The client sends another at once. There is none, so the limiter refuses, and works out that one token will be due in a thousand milliseconds, and says so.

![Rate Limiter pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as client
    participant L as limiter
    participant S as search
    C->>L: request
    L->>L: refill, take a token
    L->>S: pass it on
    C->>L: request, straight away
    L->>L: refill, no token
    L-->>C: 429, retry after 1000 ms
```

</details>

The load-bearing sentence: **the limiter says no early, and says when to come back.**
