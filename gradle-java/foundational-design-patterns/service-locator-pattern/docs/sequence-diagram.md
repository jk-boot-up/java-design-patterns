# Service Locator Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The checkout asks the locator for the discount policy, and gets it. It asks for the payment gateway and charges the customer. Then it asks for the notifier, and the locator has no recipe for it, because somebody forgot to configure it. The locator throws. The customer has already been charged. Nothing in the checkout's constructor or in the build could have warned anyone.

![Service Locator pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as LocatorCheckout
    participant L as ServiceLocator
    participant G as PaymentGateway
    C->>L: find(DiscountPolicy)
    L-->>C: policy
    C->>L: find(PaymentGateway)
    L-->>C: gateway
    C->>G: charge(9000), money moves
    C->>L: find(Notifier)
    L-->>C: IllegalStateException, no recipe
```

</details>

The load-bearing sentence: **the failure arrived in production, after the money moved, not in the build.**
