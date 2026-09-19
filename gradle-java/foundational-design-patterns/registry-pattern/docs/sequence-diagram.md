# Registry Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. A test registers a gateway that has already taken one charge, and finishes, without clearing the registry. A second test then builds a checkout, which takes nothing in its constructor, and places an order. The checkout asks the registry for the gateway and gets the first test's leftover one. It charges it. The second test checks that exactly one charge was made in total, and finds two. It fails, though nothing in it changed.

![Registry pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant T1 as test one
    participant R as Registry
    participant T2 as test two
    participant C as RegistryCheckout
    T1->>R: register(gateway with 1 charge)
    Note over R: never cleared
    T2->>C: new RegistryCheckout()
    T2->>C: place(10000)
    C->>R: get(PaymentGateway)
    R-->>C: test one's leftover gateway
    T2->>T2: expected 1 charge, saw 2
```

</details>

The load-bearing sentence: **neither test changed, and one failed, because the order changed.**
