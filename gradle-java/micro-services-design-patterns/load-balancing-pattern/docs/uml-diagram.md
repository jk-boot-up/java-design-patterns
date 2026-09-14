# Client-Side Load Balancing — UML Sequence Diagrams

Five sequences over the same three instances. What changes between them is only who
gets asked — and that is the whole pattern.

Throughout: `catalog-1` and `catalog-2` answer in 10 milliseconds, `catalog-3` takes
60, because it is on older hardware.

## One Request, Step By Step

Every request goes through the same three beats: ask who is available, choose one,
and report back how long it took.

![Client-side load balancing sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as CatalogClient
    participant B as LoadBalancer
    participant K as CatalogCluster
    participant I as the chosen instance

    C->>K: instances()
    K-->>C: [catalog-1, catalog-2, catalog-3]

    C->>B: choose(candidates)
    B-->>C: catalog-2
    Note over C,B: the client never asks which balancer it is holding

    C->>I: productName("SKU-1234")
    I-->>C: "Espresso Machine"
    Note over C,I: 10ms

    C->>B: observed(catalog-2, 10ms)
    Note over B: round-robin ignores this — least-latency learns from it
```

</details>

## Act One: Always The First On The List

Twelve requests, and the same instance every time.

```mermaid
sequenceDiagram
    autonumber
    participant C as CatalogClient
    participant B as FirstInstanceBalancer
    participant C1 as catalog-1 (10ms)
    participant C2 as catalog-2 (10ms)
    participant C3 as catalog-3 (60ms)

    loop twelve times
        C->>B: choose([c1, c2, c3])
        B-->>C: catalog-1
        C->>C1: productName("SKU-1234")
        C1-->>C: "Espresso Machine"
    end

    Note over C1: 12 requests — 100%
    Note over C2: 0 requests — idle, and paid for
    Note over C3: 0 requests — idle, and paid for
    Note over C,C3: total 120ms — the fastest act in the whole demo
```

The thing to notice is the last note. This is not the slow one. Nothing here fails,
nothing times out, and every request gets the right answer promptly. The cost is
two machines being billed for doing nothing, and one machine whose death takes the
entire shop with it.

## Act Two: Round-Robin Takes Turns

```mermaid
sequenceDiagram
    autonumber
    participant C as CatalogClient
    participant B as RoundRobinBalancer
    participant C1 as catalog-1 (10ms)
    participant C2 as catalog-2 (10ms)
    participant C3 as catalog-3 (60ms)

    C->>B: choose(...)
    B-->>C: catalog-1
    C->>C1: productName
    C1-->>C: 10ms

    C->>B: choose(...)
    B-->>C: catalog-2
    C->>C2: productName
    C2-->>C: 10ms

    C->>B: choose(...)
    B-->>C: catalog-3
    C->>C3: productName
    C3-->>C: 60ms
    Note over C,C3: the slow box, chosen as often as the fast ones

    Note over C1,C3: after twelve: 4 / 4 / 4 — total 320ms
```

A perfectly even split, and nearly three times act one's total. Round-robin sent a
third of the shop's traffic to the slowest machine the shop owns, because
round-robin does not know what "slow" means and was never told. **Fair is not the
same as fast.**

## Act Three: Least Latency Measures, Then Prefers

```mermaid
sequenceDiagram
    autonumber
    participant C as CatalogClient
    participant B as LeastLatencyBalancer
    participant C1 as catalog-1 (10ms)
    participant C2 as catalog-2 (10ms)
    participant C3 as catalog-3 (60ms)

    Note over B: knows nothing yet — measures before it judges

    C->>B: choose(...)
    B-->>C: catalog-1
    C->>C1: productName
    C1-->>C: 10ms
    C->>B: observed(catalog-1, 10ms)

    C->>B: choose(...)
    B-->>C: catalog-2
    C->>C2: productName
    C2-->>C: 10ms
    C->>B: observed(catalog-2, 10ms)

    C->>B: choose(...)
    B-->>C: catalog-3
    C->>C3: productName
    C3-->>C: 60ms
    C->>B: observed(catalog-3, 60ms)
    Note over B: now believes 10 / 10 / 60 — nobody configured that

    loop the remaining nine
        C->>B: choose(...)
        B-->>C: catalog-1
        C->>C1: productName
        C1-->>C: 10ms
    end

    Note over C1,C3: 10 / 1 / 1 — total 170ms
```

One hundred and seventy milliseconds instead of three hundred and twenty, and the
slow box was asked exactly once: the once it took to find out it was slow.

Two things in this diagram are worth more than the timing. The first is the note in
the middle — the client discovered those latencies from its own requests, and a
client in a different rack would have measured different ones. That is the only
thing client-side balancing can do that server-side balancing structurally cannot.

The second is that `catalog-2` is *exactly as fast* as `catalog-1` and received one
request out of twelve. The tie broke towards whoever was measured first, so the
client found a favourite and kept it. Harmless with one client; with a thousand
clients they all pick the same favourite, crowd it until it is slow, and then all
leave it together. A learning balancer needs a random tie-break or it will herd.

## Act Four: Two Well-Behaved Clients, One Idle Machine

```mermaid
sequenceDiagram
    autonumber
    participant W as Web client
    participant M as Mobile client
    participant C1 as catalog-1 (10ms)
    participant C2 as catalog-2 (10ms)
    participant C3 as catalog-3 (60ms)

    Note over W: its own counter, starting at 0
    Note over M: its own counter, also starting at 0

    W->>C1: request 1
    W->>C2: request 2
    M->>C1: request 1
    M->>C2: request 2

    Note over C1: 2 requests
    Note over C2: 2 requests
    Note over C3: 0 requests — nothing at all
```

There is no mistake in this diagram, and that is what makes it the important one.
Each client took perfect turns. Each counter did exactly what a counter should.
Between them they left a machine completely idle, because the counter lives inside
one client and counts one client's requests.

**A client-side balancer can only balance the traffic it can see, and it can only
see its own.** When that is not good enough, the answer is not a cleverer client —
it is one balancer in front of the cluster, seeing every request. That is
server-side balancing, and it is the right answer more often than this pattern's
fans admit.

## Notes

- The first four diagrams are the *same* client code. `CatalogClient` is not
  modified between acts; only the object passed to its constructor changes. That is
  Strategy doing its job.
- `observed` appears in act three and is absent from acts one and two, because it is
  a default method that those balancers do not implement. Round-robin should not have
  to pretend to learn.
- Every millisecond in these diagrams comes out of `SimulatedClock`, which moves only
  when something moves it. The 320ms timeline costs no real time, so the numbers are
  exact rather than approximately reproducible.
