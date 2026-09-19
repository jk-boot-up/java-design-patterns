# Future/Promise Pattern — Architecture Diagram

Where each piece runs, and the one object that stands between a reader
and a writer that may never otherwise meet.

![Future/Promise pattern architecture diagram](images/architecture-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TB
    subgraph Reader["reader side — the page thread"]
        direction TB
        Page["ConcurrentProductPage.render()"]
    end

    subgraph Pool["worker pool — three lookups at once"]
        direction TB
        W1["price lookup"]
        W2["stock lookup"]
        W3["rating lookup"]
    end

    subgraph Handoff["the Future/Promise split, act three"]
        direction TB
        F["CompletableFuture<br/>one object, two halves"]
        Writer["writer thread<br/>calls complete()"]
    end

    subgraph Naive["naive — no overlap at all"]
        direction TB
        Seq["SequentialProductPage<br/>one lookup, then the next,<br/>then the last"]
    end

    Page -->|submit, get three Futures| W1
    Page -->|submit, get three Futures| W2
    Page -->|submit, get three Futures| W3

    Writer -->|complete value| F
    Page -.->|get, blocks until complete| F

    Seq -.->|no submit, no Future, no overlap| W1
```

</details>

## Reading The Diagram

**Three arrows leave `Page` in the pattern half, all at once.** That
simultaneity is the entire pattern: three submissions, in immediate
succession, each returning before any lookup has finished.

**The `Handoff` box is deliberately separate from the pool.** `Future`
and `Promise` do not require an executor at all — `FutureAndPromise`
spawns one plain thread — because the split between reading and writing a
result is a property of `CompletableFuture` itself, not of thread pools.
