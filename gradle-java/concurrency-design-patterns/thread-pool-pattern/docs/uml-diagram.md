# Thread Pool Pattern — UML Sequence Diagrams

Four sequences: the pool's queue at capacity, the pool-starvation
deadlock, the unbounded-queue trap, and the harness's own lost-update
proof, copied unchanged from §46.

## 1. The Pool's Queue Reaches Capacity, And Says No

![Thread Pool pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Main as Test thread
    participant Pool as ThreadPoolExecutor «1 worker, queue capacity 3»
    participant Worker as worker thread

    Main->>Pool: execute(held task)
    Pool->>Worker: hands the held task to the one worker
    Worker->>Worker: parked at a Gate
    Note over Main: CountDownLatch confirms the worker<br/>has started the held task and is now parked
    Main->>Pool: execute(ord-1), execute(ord-2), execute(ord-3)
    Note over Pool: queue size == 3 == capacity, guaranteed
    Main->>Pool: execute(ord-overflow)
    Pool-->>Main: rejection handler runs synchronously — refused, no wait
```

</details>

## 2. Pool Starvation — A Task Waiting On A Task In Its Own Pool

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Main as Test thread
    participant Pool as ThreadPoolExecutor «1 worker»
    participant Outer as outer task «running on the only worker»

    Main->>Pool: submit(outer task)
    Pool->>Outer: hands outer to the only worker
    Outer->>Pool: submit(inner task)
    Note over Pool: inner is queued — no worker is free,<br/>the only one is Outer itself
    Outer->>Outer: inner.get(timeoutMillis)
    Note over Outer: inner never runs, so this always times out
    Outer-->>Main: returns "TIMED OUT" after the rescue timeout
    Note over Pool: left alone, with no timeout, this never resolves
```

</details>

## 3. The Unbounded-Queue Trap — A Backlog With No Ceiling

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Main as Test thread
    participant Pool as newFixedThreadPool(2)
    participant W1 as worker 1
    participant W2 as worker 2

    Main->>Pool: execute(held task), execute(held task)
    Pool->>W1: hands held task 1
    Pool->>W2: hands held task 2
    W1->>W1: parked at a Gate
    W2->>W2: parked at a Gate
    Note over Main: CountDownLatch confirms both workers<br/>have started and are now parked
    Main->>Pool: execute(ord-1) .. execute(ord-500)
    Note over Pool: every one of the 500 is accepted —<br/>the internal queue has no capacity to say no
    Main->>Pool: backlog() -> 500
```

</details>

## 4. The Harness's Own Proof — A Lost Update, Every Run

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant T1 as Thread 1
    participant T2 as Thread 2
    participant R as Rendezvous «2 parties»
    participant S as shared int, starts at 10

    T1->>S: read -> 10
    T2->>S: read -> 10
    T1->>R: meet()
    T2->>R: meet()
    Note over R: both released together, only once both have arrived
    T1->>S: write 10 - 1 = 9
    T2->>S: write 10 - 1 = 9
    Note over S: final value: 9, not 8 — one decrement is lost, every run
```

</details>

This is the same mechanism §46 built and this project's `HarnessSelfTest`
proves again, copied unchanged, before act two or act three relies on it.
