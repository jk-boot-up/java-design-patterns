# Adapter Pattern — UML Sequence Diagram

Shows the runtime interaction: `CheckoutService` calls `quoteRate()` once,
on whatever `ShippingRateProvider` it was constructed with, and the
`AcmeShippingAdapter` translates that single call into the shape
`AcmeShippingSdk` actually expects — the caller never sees pounds or
cents.

![Adapter pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    actor Client as CheckoutService
    participant Adapter as AcmeShippingAdapter
    participant Sdk as AcmeShippingSdk

    Client->>Adapter: quoteRate("94107", 3.5)
    activate Adapter
    Adapter->>Adapter: weightLb = 3.5 kg * 2.20462
    Adapter->>Sdk: fetchCostInCents("94107", 7.71617)
    activate Sdk
    Sdk-->>Adapter: 1348 (cents)
    deactivate Sdk
    Adapter->>Adapter: dollars = 1348 / 100, HALF_UP
    Adapter-->>Client: $13.48
    deactivate Adapter

    Note over Client,Sdk: CheckoutService never imports AcmeShippingSdk -- swap in FlatRateShippingProvider and this diagram collapses to one direct call.
```

</details>

## Notes

- The client makes exactly **one** call: `quoteRate(destinationZip,
  weightKg)`. It never calls `fetchCostInCents` and never touches pounds
  or cents.
- The adapter performs the conversion in two places around the single
  delegated call: kilograms → pounds *before* calling the adaptee, and
  cents → dollars *after* the adaptee returns.
- `AcmeShippingSdk` does exactly one thing — compute a price given pounds —
  and has no idea it is being adapted. It is unmodified third-party code.
- If `CheckoutService` were wired to `FlatRateShippingProvider` instead,
  this whole diagram collapses to a single direct call with no
  intermediate translation step — proving the adapter is invisible from
  the client's point of view, not a mandatory extra hop.
