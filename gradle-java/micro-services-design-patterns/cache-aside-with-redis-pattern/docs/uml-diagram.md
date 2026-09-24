# Cache-Aside with Redis Pattern — UML Sequence Diagrams

Four sequences. The plain write comes first, because it is the headline find and the one thing a cache with a hand-moved clock could never show.

## 1. A Plain Write Switches The Expiry Off

A price-sync job writes SKU-0 back with a plain SET. Redis treats it as a new value with no expiry, and throws the old expiry away. The price changes in the database, and the stale entry never goes.

![A plain write switches the expiry off](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant J as price-sync job
    participant R as Redis
    participant D as database
    participant C as customer
    J->>R: SET product:SKU-0 2000, no expiry
    C->>R: TTL product:SKU-0
    R-->>C: -1, which means never
    D-->>D: price changes to 2100
    Note over R: 2 seconds later the key is still there
    C->>R: GET product:SKU-0
    R-->>C: 2000, stale for ever
```

</details>

## 2. Real Expiry

The entry is given 2 seconds. The price changes underneath it. Nobody deletes the key; Redis removes it on its own clock, and the next read fetches the new price.

![Real expiry](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant S as shop
    participant R as Redis
    participant D as database
    S->>R: SET product:SKU-0 1000, expires in 2 s
    D-->>D: another system sets 2000
    S->>R: GET product:SKU-0
    R-->>S: 1000, stale
    loop until Redis says the key is gone
        S->>R: EXISTS product:SKU-0
    end
    R-->>R: time is up, key removed by Redis itself
    S->>R: GET product:SKU-0
    R-->>S: nothing
    S->>D: read SKU-0
    D-->>S: 2000
```

</details>

## 3. A Real Stampede

Fifty requests across two shop instances ask for SKU-0 just after it went. The database takes 500 milliseconds, so every request misses before any refill lands: more than 40 database reads for one price.

![A real stampede](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as shop A, 25 requests
    participant B as shop B, 25 requests
    participant R as Redis
    participant D as database
    A->>R: GET product:SKU-0, 25 times
    B->>R: GET product:SKU-0, 25 times
    R-->>A: nothing, 25 times
    R-->>B: nothing, 25 times
    A->>D: read SKU-0, 25 times, 500 ms each
    B->>D: read SKU-0, 25 times, 500 ms each
    Note over D: more than 40 reads for one price
```

</details>

## 4. A Lock Kept In Redis

The same fifty requests. Each one that misses tries to set a lock key with NX. Exactly one wins and reads the database; the rest, in both instances, wait for the price to appear in Redis. One database read.

![A lock kept in Redis](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant A as shop A
    participant B as shop B
    participant R as Redis
    participant D as database
    A->>R: SET lock:product:SKU-0 NX, expires in 5 s
    R-->>A: OK, you hold it
    B->>R: SET lock:product:SKU-0 NX
    R-->>B: refused, somebody holds it
    A->>D: read SKU-0
    D-->>A: 1000
    A->>R: SET product:SKU-0 1000, then DEL the lock
    B->>R: GET product:SKU-0
    R-->>B: 1000
    Note over A,D: 1 database read for 50 requests
```

</details>
