# CQRS — Sequence Diagrams

Five acts, as sequences. Only the first is rendered to an image; the rest are here as
mermaid source, because what makes them different is the words on the arrows rather
than the shapes.

![CQRS sequence diagram](images/uml-diagram.png)

## Act One — Composing The Page On Every View

```mermaid
sequenceDiagram
    autonumber
    participant User as Customer
    participant Comp as ComposingOrderHistory
    participant Ord as OrdersQueryApi
    participant Cat as CatalogService

    User->>Comp: view the order history page
    Comp->>Ord: ordersFor("cust-7")
    Ord-->>Comp: order lines, no names (30ms)
    Comp->>Cat: namesFor([SKU-KETTLE, SKU-MUG])
    Cat-->>Comp: 2 names, one batched call (60ms)
    Comp-->>User: the page (90ms)

    Note over User,Cat: and again, and again. 3 views cost 270ms<br/>and 6 service calls, for a page that never changed.
```

## Act Two — The Page Kept Ready By The Events

```mermaid
sequenceDiagram
    autonumber
    participant Write as OrderWriteService
    participant Bus as EventBus
    participant RM as OrderHistoryReadModel
    participant Cat as CatalogService
    participant User as Customer

    Write->>Bus: OrderPlaced(ord-5001)
    Bus->>RM: deliver
    RM->>Cat: namesFor([...]) — ONCE, at write time
    Cat-->>RM: 2 names
    Note over RM: the finished rows are kept

    User->>RM: view the page
    RM-->>User: 2 rows (5ms, 0 services called)
    User->>RM: view it again
    RM-->>User: 2 rows (5ms, 0 services called)

    Note over Write,User: the work did not vanish — it moved to write time,<br/>paid once per order instead of once per view.
```

## Act Three — Eventually Consistent, Shown Honestly

```mermaid
sequenceDiagram
    autonumber
    participant User as Customer
    participant Write as OrderWriteService
    participant Bus as EventBus
    participant RM as OrderHistoryReadModel

    User->>Write: place ord-5001
    Write-->>User: placed, paid for, final
    Write->>Bus: 3 events
    Note over Bus: held — still in flight

    User->>RM: view the order history page
    RM-->>User: 0 rows

    Note over User,RM: the order is real and the money has moved,<br/>and the page does not have it on.

    Bus->>RM: deliver
    User->>RM: view it again
    RM-->>User: 2 rows

    Note over User,RM: the window is however long delivery takes,<br/>and it closes by itself.
```

## Act Four — The Cache That Cannot Know It Is Wrong

```mermaid
sequenceDiagram
    autonumber
    participant Cat as CatalogService
    participant Bus as EventBus
    participant RM as OrderHistoryReadModel
    participant Cache as CachedOrderHistory
    participant Clock as SimulatedClock

    Cat->>Bus: ProductRenamed(SKU-KETTLE, "Brushed Steel Kettle")
    Bus->>RM: deliver
    Note over RM: corrected by the same event<br/>that made it wrong

    Bus--xCache: there is no arrow here
    Note over Cache: still says "Stainless Steel Kettle"

    Clock->>Cache: 300 seconds elapse
    Note over Cache: only now does it stop being wrong

    Note over Cat,Clock: a cache is a copy that cannot know it is wrong.<br/>Its only correction is a timer.
```

## Act Five — The Last Kettle

```mermaid
sequenceDiagram
    autonumber
    participant Shopper as Second shopper
    participant RM as OrderHistoryReadModel
    participant Write as OrderWriteService
    participant Ledger as StockLedger

    Shopper->>RM: is a kettle available?
    RM-->>Shopper: stockOnDisplay = 1
    Note over RM: stale, and it has no way to know

    Shopper->>Write: buy it
    Write->>Ledger: reserve(SKU-KETTLE, 1)
    Ledger--xWrite: cannot reserve 1 of SKU-KETTLE, only 0 left
    Write--xShopper: refused

    Note over Shopper,Ledger: the write side saved the shop, because the sale<br/>was decided there. Show a read model's stock number.<br/>Never sell against it.
```

## Notes On Reading These

**Act one and act two are the same page.** That is what makes the comparison fair:
ninety milliseconds and two service calls against five milliseconds and none. Both
numbers come from `CallLog`, and both are asserted —`composingPaysEveryTime` and
`aReadCostsOneLookup`.

**The zero in act two is the bigger number.** Five milliseconds against ninety is
latency, and latency is the headline. Zero service calls is availability:
`readsSurviveAnOutage` takes Orders down and the page still renders, which the
composing version could never do.

**The arrow in act two goes only one way.** The write side announces; the read side
listens. There is no route back from the projection to the write side, and that is
deliberate — the moment a decision starts flowing back the other way, you have
rebuilt the problem act five is about.

**Act four's most important arrow is the one marked as not existing.** A cache cannot
subscribe. It is not a matter of configuration, and no expiry setting fixes it —
`thereIsNoFreeSetting` closes that door on purpose.

**Act five is the rule that has to survive production.** The read model is allowed to
be wrong about stock, because nothing is decided by it. Everything that costs a
customer money happens on the write side, against the ledger that holds the actual
number.

**Nothing here sleeps.** `SimulatedClock` advances thirty milliseconds for an Orders
call, sixty for Catalog and five for a read-model lookup, so every timing above is
exact, repeatable on any machine, and free.
