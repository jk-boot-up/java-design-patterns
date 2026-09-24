# Rate Limiter with Redis Pattern — UML Sequence Diagrams

Four sequences. The fast clock comes first, because it is the one thing a limiter with a single clock can never show.

## 1. Whose Clock?

Two servers with correct clocks spend client-42's 10 searches, and the next is refused. A third server's clock runs one hour fast. It reads the empty bucket, decides the hour is up, refills it, and lets 10 more searches through. Redis stores whatever the server writes.

![Whose clock](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S1 as server-1, correct clock
    participant R as Redis
    participant S3 as server-3, one hour fast
    S1->>R: 10 searches, a token each
    S1->>R: the next search
    R->>S1: 0 tokens: refused
    S3->>R: read the bucket
    R->>S3: 0 tokens, last refilled at the start
    Note over S3: by my clock an hour has passed
    S3->>R: write a full bucket, minus 1
    S3->>R: the rest of the 20 searches
    Note over S3,R: 20 sent, 10 allowed
```

</details>

## 2. A Number Read And Written In Two Steps

The count is a plain number in Redis. Both servers read it before either writes, so both see the last token and both spend it. Afterwards Redis says 0, and nothing looks wrong.

![A number read and written in two steps](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S1 as server-1
    participant R as Redis key search-count:client-42
    participant S2 as server-2
    S1->>R: GET
    R->>S1: 1
    S2->>R: GET
    R->>S2: 1
    S1->>R: SET 0, and serve
    S2->>R: SET 0, and serve
    Note over S1,S2: 2 searches from 1 token. Redis now says 0
```

</details>

## 3. Scaled Out, Still One Bucket

Six servers share one bucket. client-77 sends 90 searches, dealt to the servers in turn. 10 are allowed, whichever servers they landed on. Redis holds one key per client, not per server.

![Scaled out, still one bucket](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as client-77
    participant LB as load balancer
    participant S as servers 1 to 6
    participant R as Redis
    C->>LB: 90 searches
    LB->>S: dealt in turn
    S->>R: a token each, from search-limit:client-77
    R->>S: the first 10: allowed
    R->>S: the other 80: refused
    Note over R: keys held: 2, one for client-42, one for client-77
```

</details>

## 4. Redis Is Stopped

The shared store is a separate program, and it can go away. A server sends 5 searches to the limiter and gets 5 errors: no yes, and no no. The shop has to decide what an error means.

![Redis is stopped](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S as server-1
    participant R as Redis
    S->>R: 1000 clients, one search each
    Note over R: 1000 keys, each deletes itself in 60 minutes
    R-->>R: stopped
    S->>R: 5 searches
    R--xS: 5 errors, no answer
    Note over S: let them through, and there is no limit. refuse them, and 5 customers see an error
```

</details>
