# Hexagonal Architecture Pattern — Class Diagram

The single most important thing on this diagram is which arrows point
**into** the core box and which point **out of** it. Every arrow from
`adapter` lands on an interface in `core.port`. Not one arrow leaves `core`
for `adapter` — except in the dashed naive box, where the direction is
reversed on purpose.

![Hexagonal Architecture pattern class diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class PlaceOrderService {
        <<core>>
        -ProductCatalog catalog
        -OrderStore orders
        -PaymentGateway payments
        -Notifier notifier
        +place(request, contact) PlaceOrderResult
    }

    class OrderStore {
        <<interface, core.port>>
        +save(order)
        +find(orderId) Optional~Order~
        +describe() String
    }

    class PaymentGateway {
        <<interface, core.port>>
        +charge(customerId, amount)
    }

    class ProductCatalog {
        <<interface, core.port>>
        +find(sku) Optional~Product~
        +reduceStock(sku, qty)
    }

    class Notifier {
        <<interface, core.port>>
        +send(to, body)
    }

    class InMemoryOrderStore {
        <<adapter.persistence, driven>>
    }
    class AppendOnlyOrderStore {
        <<adapter.persistence, driven — the forced change>>
    }
    class InMemoryPaymentGateway {
        <<adapter.payment, driven>>
    }
    class InMemoryNotifier {
        <<adapter.notification, driven>>
    }

    class HttpCheckoutAdapter {
        <<adapter.driving.http>>
        +post(jsonBody) String
    }
    class CliCheckoutAdapter {
        <<adapter.driving.cli — the forced change>>
        +run(commandLine) String
    }

    class NaivePlaceOrderService {
        <<naive.core — the shortcut>>
        -InMemoryOrderStore orders
        -InMemoryProductCatalog catalog
        -InMemoryPaymentGateway payments
    }

    PlaceOrderService --> OrderStore : calls, never names an implementation
    PlaceOrderService --> PaymentGateway
    PlaceOrderService --> ProductCatalog
    PlaceOrderService --> Notifier

    OrderStore <|.. InMemoryOrderStore
    OrderStore <|.. AppendOnlyOrderStore
    PaymentGateway <|.. InMemoryPaymentGateway
    Notifier <|.. InMemoryNotifier

    HttpCheckoutAdapter --> PlaceOrderService : calls in
    CliCheckoutAdapter --> PlaceOrderService : calls in

    NaivePlaceOrderService --> InMemoryOrderStore : names the adapter directly
    NaivePlaceOrderService --> InMemoryPaymentGateway
```

</details>

## Reading The Diagram

**`PlaceOrderService` has four outgoing arrows, and all four land on
interfaces in `core.port`.** Not one lands on `InMemoryOrderStore`,
`InMemoryPaymentGateway`, or any other concrete adapter — it cannot, because
it never imports one.

**Driven adapters point up, at a port, with a hollow triangle — implements,
not extends.** `InMemoryOrderStore` and `AppendOnlyOrderStore` both point at
`OrderStore` and never at each other or at `PlaceOrderService`.

**Driving adapters point at `PlaceOrderService` directly**, and that arrow
is correct — a driving adapter's whole job is to call the core. The
asymmetry is the point: driving adapters may name the core; the core may
never name an adapter, driving or driven.

**`NaivePlaceOrderService` is the only class on this diagram with an arrow
to a concrete adapter from something calling itself a use case.** That
single misdirected arrow is the shortcut `ArchitectureRuleCatchesTheShortcutTest`
exists to catch.
