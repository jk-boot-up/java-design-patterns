# Decorator Pattern — UML Sequence Diagram

Shows the runtime interaction: calling `cost()` on the outermost decorator
triggers a chain of delegated calls down to the plain `Product`, with each
layer adding its own fee on the way back up.

![Decorator pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    actor Client as PricingDemo
    participant Express as ExpressHandlingDecorator
    participant Insurance as InsuranceDecorator
    participant GiftWrap as GiftWrapDecorator
    participant Product as Product

    Client->>Express: cost()
    activate Express
    Express->>Insurance: wrapped.cost()
    activate Insurance
    Insurance->>GiftWrap: wrapped.cost()
    activate GiftWrap
    GiftWrap->>Product: wrapped.cost()
    activate Product
    Product-->>GiftWrap: $79.99
    deactivate Product
    GiftWrap-->>Insurance: $83.49 (+ $3.50 gift wrap fee)
    deactivate GiftWrap
    Insurance-->>Express: $85.16 (+ 2% premium of $83.49)
    deactivate Insurance
    Express-->>Client: $95.15 (+ $9.99 express fee)
    deactivate Express

    Note over Client,Product: Each layer only ever calls wrapped.cost() -- none of them know how many layers are beneath them, or whether there are any at all.
```

</details>

## Notes

- The client makes exactly **one** call, `cost()`, on the outermost
  decorator. It never calls into `Product` directly and never knows how
  many decorators are stacked underneath.
- Each decorator delegates to `wrapped.cost()` first, then adds its own
  fee on top of whatever comes back — the call travels all the way down to
  `Product` before any fee is added, and fees accumulate on the way back
  up.
- `InsuranceDecorator`'s premium is computed on `$83.49` — the gift-wrapped
  total — not on the original `$79.99`, because it calls `wrapped.cost()`
  and has no visibility into what `wrapped` actually is.
- If the decorators were stacked in a different order (insurance first,
  then gift wrap), this same diagram shape still applies, but the dollar
  amounts at each step change — see
  [`decorator-pattern-explained.md`](decorator-pattern-explained.md) for
  the side-by-side comparison.
