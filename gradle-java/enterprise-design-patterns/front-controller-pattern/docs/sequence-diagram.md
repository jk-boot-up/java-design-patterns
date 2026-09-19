# Front Controller Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. A visitor asks for the orders page without a token. The request goes to the front controller. The logging filter passes it on. The authentication filter sees no token and the path is not public, so it answers four oh one without going further. The logging filter, on the way back, records the request and its outcome. The orders handler was never called.

![Front Controller pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant V as visitor
    participant F as front controller
    participant L as logging filter
    participant A as authentication filter
    participant H as orders handler
    V->>F: GET /orders (no token)
    F->>L: apply
    L->>A: next
    A-->>L: 401 please sign in
    L->>L: log: GET /orders -> 401
    L-->>V: 401
    Note over H: never called
```

</details>

The load-bearing sentence: **a private page is protected without the handler knowing.**
