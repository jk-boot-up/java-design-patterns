# Abstract Factory Pattern — UML Sequence Diagram

Shows the runtime interaction: the client is handed one factory, collects the
three products from it once, and then talks only to interfaces for the rest of
the run.

![Abstract Factory pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    actor Client as AbstractFactoryDemo
    participant Checkout as CheckoutService
    participant Factory as UkMarketFactory
    participant Tax as TaxCalculator
    participant Money as CurrencyFormatter
    participant Address as AddressValidator

    Client->>Checkout: new CheckoutService(ukFactory)
    activate Checkout

    Checkout->>Factory: createTaxCalculator()
    activate Factory
    Factory-->>Checkout: UkVatCalculator
    deactivate Factory

    Checkout->>Factory: createCurrencyFormatter()
    activate Factory
    Factory-->>Checkout: PoundFormatter
    deactivate Factory

    Checkout->>Factory: createAddressValidator()
    activate Factory
    Factory-->>Checkout: UkPostcodeValidator
    deactivate Factory

    Note over Checkout,Address: the family is fixed now — the factory is never consulted again

    Client->>Checkout: quote(order)

    Checkout->>Address: isValid("EH1 1YZ")
    activate Address
    Address-->>Checkout: true
    deactivate Address

    Checkout->>Tax: taxOn(120.00)
    activate Tax
    Tax-->>Checkout: 24.00
    deactivate Tax

    Checkout->>Money: format(144.00)
    activate Money
    Money-->>Checkout: "£144.00"
    deactivate Money

    Checkout-->>Client: Quote
    deactivate Checkout
```

</details>

## Notes

- The three creation calls happen once, in the constructor. After that the
  factory has done its job and drops out of the picture entirely — everything
  below the note is interface-to-interface conversation.
- Swap `UkMarketFactory` for `UsMarketFactory` in the very first line and every
  other arrow in this diagram stays exactly as it is. Different objects turn up
  to have the same conversation, and the answers change: `10.65` instead of
  `24.00`, `$130.65` instead of `£144.00`.
- The validator, the calculator and the formatter never talk to each other, yet
  they always agree, because they arrived together. That agreement is the
  guarantee the pattern buys you.
- The address check runs first and throws before anything is printed. The
  message it throws — "not a valid United States ZIP code" — is assembled from
  the products themselves, so it is correct in every market without a single
  branch.
- Compare with `../../factory-method-pattern/docs/uml-diagram.md`. There, one
  creation call happened in the middle of a workflow, each time it ran. Here,
  three creation calls happen up front and set up a consistent world the rest
  of the code lives in.
