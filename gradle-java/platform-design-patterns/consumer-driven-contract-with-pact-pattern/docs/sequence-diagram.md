# Consumer-Driven Contract with Pact Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The checkout's test describes what it reads, and runs its own client against Pact's mock. They agree, and Pact writes a pact file. Later, the catalog's build starts. Pact reads the file, and sends the same request to the real catalog over HTTP. It compares the answer with what the file says. Price cents is missing, so it fails the build, and says checkout, and price cents.

![Consumer-Driven Contract with Pact pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant T as checkout test
    participant M as Pact mock
    participant F as pact file
    participant V as catalog build
    participant C as catalog release
    T->>M: run the consumer's client
    M-->>T: agrees
    T->>F: write the pact
    V->>F: read the pact
    V->>C: GET /prices/MUG
    C-->>V: sku, price, currency
    V->>V: priceCents missing: fail, naming checkout
```

</details>

The load-bearing sentence: **the provider learns about the break in its own build.**
