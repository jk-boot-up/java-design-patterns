# Observer Pattern — Class Diagram

Shows the static structure. `Order` holds a list of `OrderListener` and knows
nothing else about the four things on it — search the class for "email" and it
is not there. The four listeners are peers: none of them knows the others
exist. `NaiveOrderService` is drawn alongside with its four named fields, which
is exactly what the pattern is buying its way out of.

![Observer pattern class diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    direction TB

    class OrderListener {
        <<interface, observer>>
        +name() String
        +onStatusChanged(OrderEvent) void
    }

    class Order {
        <<subject>>
        -id String
        -status OrderStatus
        -listeners List~OrderListener~
        +addListener(OrderListener) void
        +removeListener(OrderListener) boolean
        +moveTo(OrderStatus) List~ListenerFailure~
    }

    class InventoryListener {
        <<concrete observer>>
        -released int
        -restocked int
        +onStatusChanged(OrderEvent) void
    }

    class EmailListener {
        <<concrete observer>>
        -customerEmail String
        -sent int
        +onStatusChanged(OrderEvent) void
    }

    class AnalyticsListener {
        <<concrete observer>>
        -counts Map~OrderStatus,Integer~
        +onStatusChanged(OrderEvent) void
    }

    class WarehouseFeedListener {
        <<concrete observer>>
        -feed List~String~
        +onStatusChanged(OrderEvent) void
    }

    class OrderEvent {
        <<record>>
        +orderId String
        +from OrderStatus
        +to OrderStatus
        +describe() String
    }

    class ListenerFailure {
        <<record>>
        +listenerName String
        +message String
    }

    class OrderStatus {
        <<enumeration>>
        PLACED
        PAID
        SHIPPED
        DELIVERED
        CANCELLED
    }

    class NaiveOrderService {
        <<the trap>>
        -inventory InventoryListener
        -email EmailListener
        -analytics AnalyticsListener
        -warehouseFeed WarehouseFeedListener
        +markShipped(String, OrderStatus) void
    }

    OrderListener <|.. InventoryListener
    OrderListener <|.. EmailListener
    OrderListener <|.. AnalyticsListener
    OrderListener <|.. WarehouseFeedListener

    Order o-- "0..*" OrderListener : notifies, knows nothing else about
    Order ..> OrderEvent : creates
    Order ..> ListenerFailure : reports
    Order --> OrderStatus : holds
    OrderListener ..> OrderEvent : receives

    NaiveOrderService --> InventoryListener : hard-wired
    NaiveOrderService --> EmailListener : hard-wired
    NaiveOrderService --> AnalyticsListener : hard-wired
    NaiveOrderService --> WarehouseFeedListener : hard-wired

    note for Order "Search this class for the word `email`. It is not here."
    note for NaiveOrderService "Four named fields. A fifth reaction edits this file."
```

</details>

## Notes

**The aggregation from `Order` to `OrderListener` is the pattern.** It is
`0..*`, and the multiplicity matters in both directions: zero listeners is a
perfectly good order, and adding the thousandth changes no code in `Order`.

**The four listeners have no relationship to each other.** There is no arrow
between them because there is no dependency between them, and that is the
property the design exists to protect. A listener that needed to run after
another one would need an arrow, and at that point they are one listener.

**`OrderEvent` flows one way.** `Order` creates it and every listener receives
it; nothing hands a listener a reference back to the `Order`. That is the GoF
*push* model, chosen so that a listener cannot change the subject halfway
through a notification.

**`ListenerFailure` is returned, not thrown.** It is the visible half of the
decision that a broken listener must not stop the ones after it.

**The four `hard-wired` arrows out of `NaiveOrderService` are the cost.** Each
is a compile-time dependency on a concrete class, and a fifth reaction adds a
fifth arrow — plus an edit to `markShipped`, plus a re-test of everything that
called it.

See [`uml-diagram.md`](uml-diagram.md) for the sequence, which is where the
failure-isolation behaviour actually becomes visible.
