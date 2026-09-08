# Template Method Pattern — Class Diagram

Shows the static structure. `FulfilmentProcess` owns the sequence and marks
`fulfil` `final`; the three routes fill in the holes. What is worth reading
carefully is not the inheritance arrows — those are obvious — but *which
methods each route overrode*, because that is the entire design decision the
base class makes on the subclasses' behalf.

![Template Method pattern class diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    direction TB

    class FulfilmentProcess {
        <<abstract, template>>
        +fulfil(Order) FulfilmentReport
        -validate(Order, FulfilmentReport) void
        #routeName()* String
        #reserveStock(Order, FulfilmentReport)* void
        #charge(Order, FulfilmentReport)* void
        #dispatch(Order, FulfilmentReport)* void
        #pack(Order, FulfilmentReport) void
        #notifyCustomer(Order, FulfilmentReport) void
        #requiresShippingAddress() boolean
        #afterFulfilment(Order, FulfilmentReport) void
    }

    class WarehouseFulfilment {
        <<concrete route>>
        -ledger StockLedger
        -site String
        #routeName() String
        #reserveStock(..) void
        #charge(..) void
        #dispatch(..) void
    }

    class MarketplaceFulfilment {
        <<concrete route>>
        -seller SellerApi
        #routeName() String
        #reserveStock(..) void
        #charge(..) void
        #dispatch(..) void
        #pack(..) void
        #afterFulfilment(..) void
    }

    class DigitalFulfilment {
        <<concrete route>>
        #routeName() String
        #reserveStock(..) void
        #charge(..) void
        #dispatch(..) void
        #pack(..) void
        #notifyCustomer(..) void
        #requiresShippingAddress() boolean
    }

    class Order {
        <<record>>
        +id String
        +customerEmail String
        +shippingAddress String
        +lines List~OrderLine~
        +hasShippingAddress() boolean
        +itemCount() int
        +subtotal() Money
    }

    class OrderLine {
        <<record>>
        +sku String
        +unitPrice Money
        +quantity int
        +total() Money
    }

    class FulfilmentReport {
        -steps List~Step~
        -notifications List~String~
        -notes List~String~
        +stepNames() List~String~
        +charged() Money
        +dispatchReference() String
    }

    class StockLedger {
        +stock(String, int) StockLedger
        +available(String) int
        +reserve(String, int) void
    }

    class SellerApi {
        +sellerName() String
        +confirm(String, int) boolean
    }

    class NaiveFulfilment {
        <<the trap>>
        +fulfilFromWarehouse(Order) FulfilmentReport
        +fulfilFromMarketplace(Order) FulfilmentReport
        +fulfilDigital(Order) FulfilmentReport
    }

    FulfilmentProcess <|-- WarehouseFulfilment
    FulfilmentProcess <|-- MarketplaceFulfilment
    FulfilmentProcess <|-- DigitalFulfilment

    FulfilmentProcess ..> Order : reads
    FulfilmentProcess ..> FulfilmentReport : fills in
    Order *-- "1..*" OrderLine
    WarehouseFulfilment --> StockLedger : reserves against
    MarketplaceFulfilment --> SellerApi : asks

    NaiveFulfilment ..> FulfilmentReport : fills in, three times over
    NaiveFulfilment --> StockLedger
    NaiveFulfilment --> SellerApi

    note for FulfilmentProcess "fulfil is final. validate is private. A route may say how a step behaves, never when it runs."
    note for NaiveFulfilment "Three copies of the sequence. Two have already drifted."
```

</details>

## Notes

**`fulfil` is the only public method on the base class, and it is `final`.**
Everything else is `protected` or `private`. That is the pattern stated in
access modifiers: the outside world gets one entry point, subclasses get a
set of holes, and nobody gets to change the order.

**Three kinds of hole, and the diagram distinguishes them.** The abstract
steps are marked with `*` — `routeName`, `reserveStock`, `charge`,
`dispatch`. `pack` and `notifyCustomer` are concrete steps with a working
default. `requiresShippingAddress` and `afterFulfilment` are hooks: one
answers a question validation asks, the other is empty. Deciding which of
the three a given step should be is most of the work of using this pattern.

**Count the overrides in each route.** `WarehouseFulfilment` overrides only
the four required steps, because the defaults were written with it in mind.
`MarketplaceFulfilment` adds two. `DigitalFulfilment` adds three, and it is
the reason the hooks exist at all — an order with no address, nothing to
reserve and nothing to pack would be impossible to express otherwise without
weakening the base class for everybody.

**`validate` is private, not protected, and that is deliberate.** It is the
one part of the sequence a subclass genuinely must not be able to replace.
The only influence a route has over it is answering
`requiresShippingAddress()` — a much narrower permission than "override
validate", and the difference between a base class that guarantees something
and one that merely asks nicely.

**No arrow runs from `FulfilmentProcess` to `StockLedger` or `SellerApi`.**
The base class knows about orders and reports and nothing else. Warehouses
and marketplaces are entirely the subclasses' business, which is why a
fourth route can be added — as `FulfilmentDemo` does with click-and-collect
— without the base class learning a new word.

**`NaiveFulfilment` has three arrows where the pattern has one.** It reaches
the same report, three separate times, through three method bodies that each
have to remember the sequence for themselves.

See [`uml-diagram.md`](uml-diagram.md) for one call to `fulfil` in sequence,
which is where the fixed order and the subclass callbacks become visible.
