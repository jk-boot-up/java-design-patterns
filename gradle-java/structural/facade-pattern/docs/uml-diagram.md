# Facade Pattern — UML Sequence Diagram

Shows the runtime interaction: the client calls the facade once, and the
facade coordinates all four subsystems in the correct order.

![Facade pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    actor Client as FacadeDemo
    participant Facade as OrderFacade
    participant Inv as InventoryService
    participant Pay as PaymentService
    participant Ship as ShippingService
    participant Notify as NotificationService

    Client->>Facade: placeOrder(OrderRequest)
    activate Facade

    Facade->>Inv: reserveStock(productId, quantity)
    activate Inv
    Inv-->>Facade: true
    deactivate Inv

    Facade->>Pay: charge(customerId, amount)
    activate Pay
    Pay-->>Facade: paymentId
    deactivate Pay

    Facade->>Ship: scheduleShipment(orderId, address)
    activate Ship
    Ship-->>Facade: trackingId
    deactivate Ship

    Facade->>Notify: sendOrderConfirmation(customerId, orderId, trackingId)
    activate Notify
    Notify-->>Facade: void
    deactivate Notify

    Facade-->>Client: OrderConfirmation(orderId, paymentId, trackingId)
    deactivate Facade
```

</details>

## Notes

- The client (`FacadeDemo`) makes a **single call** to `OrderFacade`; it
  never talks to `InventoryService`, `PaymentService`, `ShippingService`, or
  `NotificationService` directly.
- `OrderFacade` is responsible for calling the subsystems **in the right
  order** and short-circuits with an `IllegalStateException` if
  `reserveStock` returns `false` (not shown above — the happy path).
- This is the core benefit of the Facade pattern: it reduces the client's
  coupling from four subsystem APIs down to one simplified entry point.
