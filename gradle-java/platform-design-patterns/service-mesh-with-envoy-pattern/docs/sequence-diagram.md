# Service Mesh with Envoy Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The checkout calls the proxy, once, with no retry code. Envoy passes the call to payments, which refuses. Envoy tries again, and payments refuses again. Envoy tries a third time, and payments answers. Envoy passes the answer back. The checkout sees one answer, and never saw the refusals.

![Service Mesh with Envoy pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as checkout
    participant E as Envoy
    participant P as payments
    C->>E: charge
    E->>P: attempt 1
    P-->>E: 503
    E->>P: attempt 2
    P-->>E: 503
    E->>P: attempt 3
    P-->>E: 200
    E-->>C: 200
```

</details>

The load-bearing sentence: **the caller sees one answer. The proxy absorbed the refusals.**
