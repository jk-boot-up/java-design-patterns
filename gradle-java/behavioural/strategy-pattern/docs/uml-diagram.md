# Strategy Pattern — UML Sequence Diagram

Shows the runtime interaction: the rule is chosen once, before checkout
exists, and after that every quote is the same three messages regardless of
which rule was picked. The second half of the diagram repeats the identical
exchange with a different rule to make the point that nothing on the
`CheckoutService` side changes.

![Strategy pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    actor Client as ShippingCostDemo
    participant Registry as ShippingRules
    participant Checkout as CheckoutService
    participant Weight as WeightBandedRule
    participant Campaign as FreeOverThresholdRule

    Note over Client,Registry: Selection happens once, at the edge.
    Client->>Registry: byName("weight")
    activate Registry
    Registry-->>Client: WeightBandedRule
    deactivate Registry
    Client->>Checkout: new CheckoutService(rule)

    Note over Checkout,Weight: Every quote from here on is the same three messages.
    Client->>Checkout: quote(Cardiff, 6.5kg, 180mi, £64.00)
    activate Checkout
    Checkout->>Weight: costFor(shipment)
    activate Weight
    Weight-->>Checkout: £12.00
    deactivate Weight
    Checkout->>Weight: name()
    activate Weight
    Weight-->>Checkout: "Weight banded"
    deactivate Weight
    Checkout-->>Client: Quote(£64.00 + £12.00 = £76.00)
    deactivate Checkout

    Note over Client,Campaign: Swap the rule. The messages below are identical.
    Client->>Registry: byName("campaign")
    activate Registry
    Registry-->>Client: FreeOverThresholdRule
    deactivate Registry
    Client->>Checkout: new CheckoutService(rule)
    Client->>Checkout: quote(Cardiff, 6.5kg, 180mi, £64.00)
    activate Checkout
    Checkout->>Campaign: costFor(shipment)
    activate Campaign
    Campaign-->>Checkout: £0.00
    deactivate Campaign
    Checkout->>Campaign: name()
    activate Campaign
    Campaign-->>Checkout: "Free over £50.00"
    deactivate Campaign
    Checkout-->>Client: Quote(£64.00 + £0.00 = £64.00)
    deactivate Checkout

    Note over Client,Campaign: CheckoutService never asked which rule it was holding -- there is no message on this diagram where it could have.
```

</details>

## Notes

- **Selection is a separate episode from use.** The first two messages
  happen once, when the shop is configured; everything after that repeats
  per order. In the naive design those two concerns were the same line of
  code, executed on every quote.
- **`costFor` is called exactly once per quote.** That is asserted by a
  test, not just intended: a rule called twice would double-charge the day
  somebody writes one that is not free of side effects.
- **`name()` is a second message, not part of the price.** It exists so the
  receipt can say which rule applied without `CheckoutService` owning a
  table of display names — which would be the deleted `switch` growing back
  in a new place.
- **The two halves of the diagram are the same shape.** Different
  participant, different numbers, identical message sequence. If you
  covered the participant names you could not tell which rule was in force,
  and neither can `CheckoutService`.
- **Nothing returns to the rule.** `costFor` takes a `Shipment` and returns
  a `Money`; the rule holds no reference to the checkout and no state
  between calls, which is what lets one instance be shared by every
  concurrent order.
- Compare this with the Decorator project's sequence diagram: there, one
  call cascaded through a stack of objects that all implemented the same
  interface. Here there is exactly one implementation involved per quote.
  Same interface shape, entirely different runtime story — see
  [`strategy-pattern-explained.md`](strategy-pattern-explained.md).
