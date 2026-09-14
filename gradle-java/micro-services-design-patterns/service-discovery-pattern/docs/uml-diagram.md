# Service Discovery Pattern — UML Sequence Diagram

## The Happy Path: Ask, Then Call

Two steps where the naive client had one. The extra step is the point.

![Service Discovery pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as DiscoveringPricingClient
    participant R as ServiceRegistry
    participant P1 as pricing-1
    participant P2 as pricing-2
    participant P3 as pricing-3

    Note over P1,P3: each instance registered itself at startup

    C->>R: instances("Pricing")
    R-->>C: [pricing-1, pricing-2, pricing-3]
    Note over C,R: asked again on the next call, too

    C->>P1: price("SKU-1234")
    P1-->>C: £449.99
    Note over C,P1: 10ms — first on the list, nothing clever
```

</details>

## The Deployment: An Instance Leaves Politely

`pricing-1` is taken out of service by a rolling deployment. It deregisters on the
way out, so the list is true before the first call that would have hit it.

```mermaid
sequenceDiagram
    autonumber
    participant D as Deployment
    participant P1 as pricing-1
    participant R as ServiceRegistry
    participant C as DiscoveringPricingClient
    participant P2 as pricing-2

    D->>P1: shut down
    P1->>R: deregister("pricing-1")
    Note over R: takes effect at once

    C->>R: instances("Pricing")
    R-->>C: [pricing-2, pricing-3]
    C->>P2: price("SKU-1234")
    P2-->>C: £449.99
    Note over C,P2: the shopper never noticed a deployment happened
```

## The Crash: A Stale Entry, And What Saves It

`pricing-1` dies without deregistering. The registry does not know, and says so
confidently. The client survives anyway.

```mermaid
sequenceDiagram
    autonumber
    participant P1 as pricing-1
    participant R as ServiceRegistry
    participant C as DiscoveringPricingClient
    participant P2 as pricing-2
    participant Log as CallLog

    P1--xP1: process dies
    Note over P1,R: no message is sent —<br/>a crashed process cannot send one

    C->>R: instances("Pricing")
    R-->>C: [pricing-1, pricing-2]
    Note over R: still believes pricing-1 is alive

    C->>P1: price("SKU-1234")
    P1--xC: ServiceUnavailableException
    C->>Log: note(STALE, "pricing-1 is not answering")

    C->>P2: price("SKU-1234")
    P2-->>C: £449.99
    Note over C,P2: 15ms instead of 10ms.<br/>A stale entry cost five milliseconds,<br/>not an outage.
```

## The Lease Expiring

Nobody calls anything here. Time simply passes, and the registry stops lying.

```mermaid
sequenceDiagram
    autonumber
    participant Clock as SimulatedClock
    participant P2 as pricing-2
    participant R as ServiceRegistry

    Note over R: pricing-1 crashed at 0ms.<br/>pricing-2 is alive and heartbeating.

    P2->>R: heartbeat("pricing-2")
    Clock->>Clock: advance(1000)
    R-->>R: instances("Pricing") → 2
    P2->>R: heartbeat("pricing-2")
    Clock->>Clock: advance(1000)
    R-->>R: instances("Pricing") → 2
    P2->>R: heartbeat("pricing-2")
    Clock->>Clock: advance(1000)
    R-->>R: instances("Pricing") → 2
    P2->>R: heartbeat("pricing-2")
    Clock->>Clock: advance(1000)

    R-->>R: instances("Pricing")
    Note over R: pricing-1's last heartbeat is now<br/>more than LEASE_MILLIS old
    R->>R: EXPIRED pricing-1 missed its heartbeats
    R-->>R: → 1
```

## The Comparison: No Registry At All

```mermaid
sequenceDiagram
    autonumber
    participant C as HardcodedPricingClient
    participant P1 as pricing-1
    participant P2 as pricing-2
    participant P3 as pricing-3

    C->>P1: price("SKU-1234")
    P1-->>C: £449.99
    Note over C,P1: correct, fast, and fine — for now

    Note over P1: stopped by a deployment

    C->>P1: price("SKU-1234")
    P1--xC: ServiceUnavailableException
    Note over C,P3: pricing-2 and pricing-3 are up.<br/>The client cannot reach either.<br/>It has no second name to try.
```

## Notes

**Compare the first diagram with the last.** The pattern adds exactly one message:
`instances("Pricing")`. Everything else — the call, the answer, the latency — is
identical. One extra question, asked before every call, is the entire mechanical
cost.

**The second and third diagrams are the same event with one line removed.** In the
deployment, `pricing-1` sends `deregister`. In the crash, it does not. That single
missing message is the difference between a list that is true and a list that is
confidently wrong, and there is no way to make a dying process send it reliably.
Which is why the third diagram needs a client that keeps going.

**Count the messages in the crash diagram.** The client talks to a dead instance,
catches the failure, writes a note, and calls the next one. Four steps to survive
something that took `HardcodedPricingClient` off the air completely. There is a
test that pins each of them, including the note, because a silent recovery is a
recovery nobody can measure.

**The fourth diagram has no client in it at all.** That is not an oversight. Lease
expiry is something the registry does on its own schedule, in response to the
absence of messages rather than the arrival of one. In the code it happens
opportunistically inside `instances(...)`, which is the honest way to model it
without a background thread — and it means a dead entry costs nothing until
somebody actually asks.

**Nothing in any diagram asks an instance whether it is alive.** All the arrows
about liveness point *from* the instance *to* the registry. A registry that polled
would need a list of who to poll, and building that list is the original problem
wearing a hat.
