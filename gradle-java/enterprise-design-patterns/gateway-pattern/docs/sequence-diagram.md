# Gateway Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. Checkout asks the gateway to charge forty nine ninety nine. The Acme gateway builds the provider's request, with the amount in minor units, the currency and the card token. It calls the provider, which times out. The gateway logs it and tries once more. The provider answers with code zero zero and a reference. The gateway turns that into an approved result with a receipt, and checkout writes paid.

![Gateway pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as Checkout
    participant G as AcmeGateway
    participant A as Acme client
    C->>G: charge(4999, tok_ada)
    G->>A: postCharge(fields)
    A-->>G: 91, timed out
    G->>G: log, try again
    G->>A: postCharge(fields)
    A-->>G: 00, AC-4999
    G-->>C: APPROVED, AC-4999
```

</details>

The load-bearing sentence: **checkout never sees a field name or a code.**
