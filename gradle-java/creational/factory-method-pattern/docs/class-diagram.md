# Factory Method Pattern — Class Diagram

Shows the static structure: `DeliveryService` runs the whole shipping
workflow while knowing nothing but the `Courier` interface. Each subclass
answers one question — which courier — by overriding `createCourier()`.

![Factory Method pattern class diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class FactoryMethodDemo {
        +main(args: String[]) void
    }

    class DeliveryService {
        <<abstract>>
        #createCourier()* Courier
        +tier()* String
        +ship(order: Order) Shipment
    }

    class StandardDelivery {
        #createCourier() Courier
        +tier() String
    }

    class ExpressDelivery {
        #createCourier() Courier
        +tier() String
    }

    class SameDayDelivery {
        #createCourier() Courier
        +tier() String
    }

    class InternationalDelivery {
        #createCourier() Courier
        +tier() String
    }

    class Courier {
        <<interface>>
        +name() String
        +dispatch(order: Order) Shipment
    }

    class PostalCourier {
        +name() String
        +dispatch(order: Order) Shipment
    }

    class AirCourier {
        +name() String
        +dispatch(order: Order) Shipment
    }

    class BikeCourier {
        +name() String
        +dispatch(order: Order) Shipment
    }

    class GlobalCourier {
        +name() String
        +dispatch(order: Order) Shipment
    }

    class Order {
        <<record>>
        +String orderId
        +String customerId
        +String destination
        +double weightKg
    }

    class Shipment {
        <<record>>
        +String trackingId
        +String carrier
        +int etaDays
        +double cost
    }

    FactoryMethodDemo ..> DeliveryService : uses
    DeliveryService <|-- StandardDelivery
    DeliveryService <|-- ExpressDelivery
    DeliveryService <|-- SameDayDelivery
    DeliveryService <|-- InternationalDelivery
    DeliveryService ..> Courier : uses
    StandardDelivery ..> PostalCourier : creates
    ExpressDelivery ..> AirCourier : creates
    SameDayDelivery ..> BikeCourier : creates
    InternationalDelivery ..> GlobalCourier : creates
    Courier <|.. PostalCourier
    Courier <|.. AirCourier
    Courier <|.. BikeCourier
    Courier <|.. GlobalCourier
    DeliveryService ..> Order : takes
    DeliveryService ..> Shipment : returns
```

</details>

## Notes

- `DeliveryService` is the **creator**. It owns `ship(...)`, the workflow every
  tier shares, and declares `createCourier()` as an abstract hole in the middle
  of that workflow. It never names a concrete courier class.
- `createCourier()` is the **factory method** itself — one abstract method, not
  a class. That is the whole pattern.
- `StandardDelivery`, `ExpressDelivery`, `SameDayDelivery` and
  `InternationalDelivery` are the **concrete creators**. Each is a handful of
  lines: pick a courier, name the tier. Nothing else.
- `Courier` is the **product interface** and the four courier classes are the
  **concrete products**. Unlike the sibling Simple Factory project, `Courier` is
  deliberately *not* `sealed`: this pattern exists so new products can arrive
  from anywhere, including other packages and other jars.
- Look for a `switch` in this diagram and you will not find one. Compare the
  arrows with `../../simple-factory-pattern/docs/class-diagram.md`: there, every
  `creates` arrow leaves one central factory class; here they leave four
  independent subclasses. That difference is why adding a fifth tier means
  adding a file rather than editing one.
- `ship(...)` is `final`. Subclasses change *which* courier is used, never the
  steps around it — the guard, the log lines, the order of operations.
- `Order` and `Shipment` are immutable `record` value objects passed to and
  returned from a courier.
