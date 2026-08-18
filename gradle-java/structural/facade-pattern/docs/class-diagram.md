# Facade Pattern — Class Diagram

Shows the static structure: `OrderFacade` composes the four subsystem
services and exchanges data with the client through the `OrderRequest` /
`OrderConfirmation` value objects.

![Facade pattern class diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class FacadeDemo {
        +main(args: String[]) void
    }

    class OrderFacade {
        -InventoryService inventoryService
        -PaymentService paymentService
        -ShippingService shippingService
        -NotificationService notificationService
        +placeOrder(request: OrderRequest) OrderConfirmation
    }

    class InventoryService {
        +reserveStock(productId: String, quantity: int) boolean
    }

    class PaymentService {
        +charge(customerId: String, amount: double) String
    }

    class ShippingService {
        +scheduleShipment(orderId: String, address: String) String
    }

    class NotificationService {
        +sendOrderConfirmation(customerId: String, orderId: String, trackingId: String) void
    }

    class OrderRequest {
        <<record>>
        +String customerId
        +String productId
        +int quantity
        +double amount
        +String shippingAddress
    }

    class OrderConfirmation {
        <<record>>
        +String orderId
        +String paymentId
        +String trackingId
    }

    FacadeDemo ..> OrderFacade : uses
    FacadeDemo ..> OrderRequest : creates
    OrderFacade ..> OrderRequest : reads
    OrderFacade ..> OrderConfirmation : creates
    OrderFacade o-- InventoryService
    OrderFacade o-- PaymentService
    OrderFacade o-- ShippingService
    OrderFacade o-- NotificationService
```

</details>

## Notes

- `OrderFacade` is the **Facade**: it owns the subsystem instances
  (composition, `o--`) and exposes one coarse-grained operation,
  `placeOrder(...)`, instead of letting the client talk to each subsystem
  directly.
- The subsystem classes (`InventoryService`, `PaymentService`,
  `ShippingService`, `NotificationService`) have no knowledge of the facade
  or of each other — they remain independently usable and testable.
- `OrderRequest` and `OrderConfirmation` are immutable `record` value
  objects used purely to pass data across the facade boundary.
