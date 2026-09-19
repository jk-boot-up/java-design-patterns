# Fluent Interface Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The code starts a search. It calls category with mugs, and gets back a new query. It calls under with twenty five hundred on that, and gets another. It calls in stock, and then run. Only at run does the query do any work. Every earlier call only made a new, slightly different query.

![Fluent Interface pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant Q as query
    C->>Q: search()
    Q-->>C: q0
    C->>Q: q0.category(mugs)
    Q-->>C: q1
    C->>Q: q1.under(2500)
    Q-->>C: q2
    C->>Q: q2.run()
    Q-->>C: Blue Mug, Big Mug
```

</details>

The load-bearing sentence: **each call only makes a new query. Only run does the work.**
