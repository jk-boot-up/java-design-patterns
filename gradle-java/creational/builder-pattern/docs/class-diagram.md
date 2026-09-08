# Builder Pattern — Class Diagram

## The structure

![Builder pattern class diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    direction TB

    class PurchaseOrderDemo {
        +main(String[]) void
    }

    class PurchaseOrderPresets {
        <<Director>>
        +giftOrder(...)$ PurchaseOrder
        +standardOrder(...)$ PurchaseOrder
        +expressOrder(...)$ PurchaseOrder
    }

    class PurchaseOrder {
        -orderId String
        -customerId String
        -items List~LineItem~
        -shippingAddress Address
        -giftWrapped boolean
        -giftMessage String
        -couponCode String
        -priority boolean
        -notes String
        -PurchaseOrder(Builder)
        +builder(String, String)$ Builder
        +subtotal() Money
        +total() Money
    }

    class Builder {
        <<static nested>>
        -items List~LineItem~
        -shippingAddress Address
        +addItem(LineItem) Builder
        +shippingAddress(Address) Builder
        +giftWrap() Builder
        +giftMessage(String) Builder
        +couponCode(String) Builder
        +priority() Builder
        +notes(String) Builder
        +build() PurchaseOrder
    }

    class LineItem {
        <<record>>
        +sku String
        +unitPrice Money
        +quantity int
        +total() Money
    }

    class Address {
        <<record>>
        +line1 String
        +city String
    }

    class Money {
        -Money(long)
        +pounds(double)$ Money
        +pence(long)$ Money
    }

    PurchaseOrderDemo ..> PurchaseOrder : uses directly
    PurchaseOrderDemo ..> PurchaseOrderPresets : uses for fixed recipes
    PurchaseOrderPresets ..> Builder : drives through its public methods
    PurchaseOrder *-- Builder : builds
    PurchaseOrder o-- LineItem
    PurchaseOrder o-- Address
    Builder o-- LineItem : accumulates
    Builder o-- Address
    LineItem *-- Money
    PurchaseOrder ..> Money : computes totals in
```

</details>

The arrow to notice is `PurchaseOrderPresets ..> Builder`. It never points
at `PurchaseOrder` directly — the Director-equivalent only ever talks to
the builder's public methods, never to the product's constructor or its
fields. That is what lets `PurchaseOrder` change its private representation
without a single preset needing to change.

## What the caller can see

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TB
    subgraph outside["Calling code"]
        caller["PurchaseOrder.builder(id, customer)<br/>.addItem(...).shippingAddress(...).build()"]
        preset["PurchaseOrderPresets.giftOrder(...)"]
    end

    subgraph inside["com.jk.explore.builder"]
        b["PurchaseOrder.Builder<br/><b>public static nested class</b><br/>one chainable method per piece"]
        p["PurchaseOrder<br/><b>public, immutable</b><br/>private constructor"]
        d["PurchaseOrderPresets<br/><b>public, static methods only</b><br/>fixed recipes over Builder"]
    end

    caller -->|"the only way to a fresh Builder"| b
    preset --> d
    d -->|"drives"| b
    b -->|"build()"| p

    style b fill:#dbeafe,stroke:#1d4ed8,stroke-width:2px
    style p fill:#fef3c7,stroke:#b45309,stroke-dasharray: 5 5
    style d fill:#f1f5f9,stroke:#475569
```

</details>

`PurchaseOrder`'s constructor is private. There is exactly one door in —
`PurchaseOrder.builder(orderId, customerId)` — and everything downstream of
that door, however many optional pieces get chained on, ends at the same
`build()`.

## Notes

- `LineItem` and `Address` are plain records — two or three required
  fields, nothing to decide, so a constructor is the right tool for them.
  The contrast with `PurchaseOrder`, which has the same kind of required
  data plus five independent optional pieces, is deliberate.
- Compare with
  [`../../abstract-factory-pattern/docs/class-diagram.md`](../../abstract-factory-pattern/docs/class-diagram.md).
  There, one choice produces a *family* of different objects. Here, one
  sequence of choices produces *one* object with many possible shapes.
