# Static Factory Method — Class Diagram

Two pictures. The first is the static structure: who implements what, and who
holds whom. The second is the one that actually explains the pattern — what a
caller outside the package is allowed to see.

## The structure

![Static factory method class diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    direction TB

    class StaticFactoryDemo {
        +main(String[]) void
    }

    class CheckoutService {
        +checkout(Order, Discount) Receipt
    }

    class Discount {
        <<interface>>
        +appliedTo(Order) Money
        +describe() String
        +none()$ Discount
        +percentage(int)$ Discount
        +amountOff(Money)$ Discount
        +freeShipping()$ Discount
        +bestOf(Discount, Discount)$ Discount
        +forCoupon(String)$ Discount
    }

    class NoDiscount {
        -NoDiscount()
        ~INSTANCE NoDiscount
    }

    class PercentageDiscount {
        -percent int
    }

    class AmountOffDiscount {
        -amount Money
    }

    class FreeShippingDiscount {
        -FreeShippingDiscount()
        ~INSTANCE FreeShippingDiscount
    }

    class BestOfDiscount {
        -first Discount
        -second Discount
    }

    class Money {
        -Money(long)
        -pence long
        +zero()$ Money
        +pounds(double)$ Money
        +pence(long)$ Money
        +parse(String)$ Money
    }

    class Order {
        <<record>>
        +subtotal Money
        +shipping Money
    }

    class Receipt {
        <<record>>
        +discountLabel String
        +total Money
    }

    StaticFactoryDemo ..> CheckoutService : uses
    StaticFactoryDemo ..> Discount : asks for one
    CheckoutService ..> Discount : applies
    CheckoutService ..> Order
    CheckoutService ..> Receipt

    Discount <|.. NoDiscount
    Discount <|.. PercentageDiscount
    Discount <|.. AmountOffDiscount
    Discount <|.. FreeShippingDiscount
    Discount <|.. BestOfDiscount

    Discount ..> NoDiscount : creates
    Discount ..> PercentageDiscount : creates
    Discount ..> AmountOffDiscount : creates
    Discount ..> FreeShippingDiscount : creates
    Discount ..> BestOfDiscount : creates

    Order *-- Money
    Receipt *-- Money
```

</details>

Look at where the `creates` arrows start. They leave `Discount` — the
interface itself. In every other factory pattern the arrows leave a separate
factory object. Here the type is its own factory, and that is the whole idea.

## What the caller can see

![The package boundary](images/boundary.png)

<details>
<summary>Mermaid source</summary>

```mermaid
flowchart TB
    subgraph outside["Any other package"]
        caller["your code<br/><i>Discount.percentage(10)</i>"]
    end

    subgraph inside["com.jk.explore.staticfactory"]
        door["Discount<br/><b>public interface</b><br/>6 static factory methods"]
        subgraph hidden["package-private — invisible outside"]
            n["NoDiscount"]
            p["PercentageDiscount"]
            a["AmountOffDiscount"]
            f["FreeShippingDiscount"]
            b["BestOfDiscount"]
        end
    end

    caller -->|"the only way in"| door
    door --> n
    door --> p
    door --> a
    door --> f
    door --> b

    style door fill:#dbeafe,stroke:#1d4ed8,stroke-width:2px
    style hidden fill:#fef3c7,stroke:#b45309,stroke-dasharray: 5 5
    style caller fill:#f1f5f9,stroke:#475569
```

</details>

Five classes implement `Discount`, and not one of them is public. Your code
cannot name them, cannot `new` them, and never finds out how many there are.
That is not a rule anyone has to remember — the compiler enforces it.

The practical consequence: any of those five can be renamed, merged, split or
deleted tomorrow without touching a single caller.

## The public surface, in full

| You write | You get back | Notes |
| --- | --- | --- |
| `Discount.none()` | `NoDiscount` | Always the same instance |
| `Discount.percentage(10)` | `PercentageDiscount` | `percentage(0)` returns `none()` instead |
| `Discount.amountOff(Money.pounds(5))` | `AmountOffDiscount` | `amountOff(zero)` returns `none()` instead |
| `Discount.freeShipping()` | `FreeShippingDiscount` | Always the same instance |
| `Discount.bestOf(a, b)` | `BestOfDiscount` | Compares the two per order |
| `Discount.forCoupon("SAVE10")` | any of the above | The class depends on the string |

Six ways in, one type out. The right-hand column is information the caller
never has and never needs.

## Notes

- `Money` tells the same story in miniature. Its constructor is private and
  takes a `long`; `Money.pounds(2.50)` and `Money.pence(250)` are the same
  amount reached two ways, and neither could have been a constructor without
  the other one becoming impossible.
- `Order` and `Receipt` are plain records. Not everything needs a factory —
  they carry data, they have nothing to choose, so a constructor is right.
- Compare with [`../../simple-factory-pattern/docs/class-diagram.md`](../../simple-factory-pattern/docs/class-diagram.md).
  There, a separate `PaymentMethodFactory` class sits beside the product
  hierarchy. Here there is no separate class at all — delete the factory and
  you delete the type.
