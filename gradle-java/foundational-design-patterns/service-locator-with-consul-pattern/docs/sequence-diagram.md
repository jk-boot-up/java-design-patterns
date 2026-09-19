# Service Locator with Consul Pattern — Sequence Diagram

Written for a listener with the screen off.

Say it in words. The checkout wants to charge a customer. It asks the locator for a payment gateway, by name. The locator asks Consul for the instances whose health checks are passing, and Consul names two. The locator hands back the next one in turn, and the checkout calls it over HTTP. Then the checkout asks for the notifier, and Consul knows of none healthy. The locator throws, and the customer has already been charged.

![Service Locator with Consul pattern sequence diagram](images/sequence-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant C as LocatorCheckout
    participant L as ConsulLocator
    participant K as Consul
    participant G as gateway instance
    C->>L: find("payment-gateway")
    L->>K: healthy instances?
    K-->>L: gateway-1, gateway-2
    L-->>C: gateway-2, the next in turn
    C->>G: charge 9000
    C->>L: find("notifier")
    L->>K: healthy instances?
    K-->>L: none
    L-->>C: NoHealthyInstance
```

</details>

The load-bearing sentence: **the failure arrived after the money moved, not in the build.**
