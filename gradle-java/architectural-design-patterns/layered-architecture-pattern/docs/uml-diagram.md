# Layered Architecture Pattern — UML Sequence Diagrams

Four sequences. The first is the pattern working exactly as intended, and the
one rendered as this document's image. The next three are the shortcut, the
forced change, and a refusal — the three moments the video and the README
both point back to.

## 1. One Order, Through All Four Layers

The call travels straight down — presentation to application to
infrastructure, with domain objects built along the way — and never sideways.

![Layered Architecture pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Ada as Customer
    participant Screen as CheckoutScreen
    participant Service as PlaceOrderService
    participant Products as ProductTable
    participant Cards as CardNetwork
    participant Orders as OrderTable
    participant Email as EmailServer

    Ada->>Screen: checkout(3 lines)
    Screen->>Service: place(request, email)
    Service->>Products: find and stockOf, each SKU
    Products-->>Service: prices and stock levels
    Note over Service: three lines price to £382.50
    Service->>Cards: charge(cust-8801, £382.50)
    Cards-->>Service: charged
    Service->>Products: reduceStock, each SKU
    Service->>Orders: save(order ord-1001)
    Service->>Email: send(ada@example.com, confirmation)
    Service-->>Screen: placed, ord-1001, £382.50
    Screen-->>Ada: "Order ord-1001 placed. Total £382.50."
```

</details>

Read step 6 before step 9. The card is charged before the order is written
down anywhere. Reverse that order and a declined card would leave stock
reduced and an order half-recorded with nothing to say either should not have
happened; charging first means a refusal throws before anything has changed.

## 2. The Shortcut — A Screen That Skips The Application Layer

The naive `OrderHistoryScreen` reaches straight into storage. It works, and
that is the problem this project exists to fix.

![The shortcut — a screen that skips the application layer](images/uml-diagram-2.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Ada as Customer
    participant History as OrderHistoryScreen «naive»
    participant Store as InMemoryOrderTable

    Ada->>History: history(cust-8801)
    History->>Store: all()
    Note over History: filters by customerId itself —<br/>PlaceOrderService is never called
    Store-->>History: every order ever placed
    History-->>Ada: "ord-1001  £382.50"
```

</details>

Compare this with sequence 1. There is no `PlaceOrderService` box on this
diagram at all — the application layer is not merely bypassed, it is absent
from the call entirely. `ArchitectureRuleCatchesTheShortcutTest` is what
turns this picture into a build failure rather than a code-review question.

## 3. The Forced Change — Storage Is Replaced, Nothing Above Notices

Everything above `infrastructure` is called exactly as before; only the box
at the bottom is a different class.

![The forced change — storage is replaced, nothing above notices](images/uml-diagram-3.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Root as PlaceAnOrderDemo «composition root»
    participant Screen as CheckoutScreen
    participant Service as PlaceOrderService
    participant Old as InMemoryOrderTable
    participant New as AppendOnlyOrderTable

    Note over Root: the forced change is this one line —<br/>new AppendOnlyOrderTable() instead of new InMemoryOrderTable()
    Root->>Service: wire OrderTable = new AppendOnlyOrderTable()
    Note over Old: never constructed again — 0 references from here on
    Root->>Screen: checkout(same request as before)
    Screen->>Service: place(request, email)
    Service->>New: save(order)
    Note over Service,Screen: identical calls to identical signatures —<br/>PlaceOrderService and CheckoutScreen are byte-for-byte unchanged
    New-->>Service: (the append-only log now holds the order)
```

</details>

Sixteen of the project's seventeen classes across the four layers make no
appearance in this diagram at all, because the change did not reach them.
That is the number the forced-change report prints, and this is what it looks
like as a sequence rather than a count.

## 4. A Refusal — Not Enough Stock

A refusal is a returned value, not a crash, and it never reaches the card
network.

![A refusal — not enough stock](images/uml-diagram-4.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    autonumber
    participant Ada as Customer
    participant Screen as CheckoutScreen
    participant Service as PlaceOrderService
    participant Products as ProductTable

    Ada->>Screen: checkout(3× GRD-014, only 2 in stock)
    Screen->>Service: place(request, email)
    Service->>Products: stockOf(GRD-014)
    Products-->>Service: 2
    Note over Service: 2 < 3 — CheckoutRefusedException,<br/>caught inside place(), never thrown past it
    Service-->>Screen: refused, "only 2 of GRD-014 left"
    Screen-->>Ada: "Sorry — only 2 of GRD-014 left."
```

</details>

Notice what never appears on this diagram: `CardNetwork`. The stock check
happens first, inside `priceEveryLine`, before the method reaches the line
that charges a card. Nothing is refunded here, because nothing was ever
taken.
