# Execute Around Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The caller calls with connection, and hands over a piece of work. The pool opens a connection, and gives it to the work. The work runs a query, and fails. The pool closes the connection anyway, in its finally block, and the failure goes on to the caller. The caller did not write any closing.

![Execute Around pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as caller
    participant P as pool
    participant W as the work
    C->>P: withConnection(work)
    P->>P: open a connection
    P->>W: run(connection)
    W-->>P: failed
    P->>P: close, in finally
    P-->>C: the failure
```

</details>

The load-bearing sentence: **the closing happens whatever the work does.**
