# Decorator Pattern — Class Diagram

Shows the static structure: `Product` and every `ProductDecorator`
subclass implement the shared `PricedItem` interface. Each concrete
decorator holds a `PricedItem` by composition and delegates to it before
adding its own fee. The naive alternative — one hardcoded class per
feature combination — is drawn alongside to show what the pattern buys you.

![Decorator pattern class diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class PricedItem {
        <<interface>>
        +cost() BigDecimal
        +description() String
    }

    class Product {
        <<component>>
        -String name
        -BigDecimal price
        +cost() BigDecimal
        +description() String
    }

    class ProductDecorator {
        <<abstract decorator>>
        #PricedItem wrapped
        +cost() BigDecimal
        +description() String
    }

    class GiftWrapDecorator {
        +cost() BigDecimal
        +description() String
    }

    class InsuranceDecorator {
        +cost() BigDecimal
        +description() String
    }

    class ExpressHandlingDecorator {
        +cost() BigDecimal
        +description() String
    }

    class NaiveGiftWrappedProduct {
        <<the trap>>
        +cost() BigDecimal
        +description() String
    }

    class NaiveInsuredProduct {
        <<the trap>>
        +cost() BigDecimal
        +description() String
    }

    class NaiveGiftWrappedInsuredProduct {
        <<the trap>>
        +cost() BigDecimal
        +description() String
    }

    class PricingDemo {
        +main(args: String[]) void
    }

    PricedItem <|.. Product
    PricedItem <|.. ProductDecorator
    ProductDecorator <|-- GiftWrapDecorator
    ProductDecorator <|-- InsuranceDecorator
    ProductDecorator <|-- ExpressHandlingDecorator
    ProductDecorator "1" o-- "1" PricedItem : wrapped
    PricingDemo ..> GiftWrapDecorator : stacks
    PricingDemo ..> InsuranceDecorator : stacks
    PricingDemo ..> ExpressHandlingDecorator : stacks
    PricingDemo ..> NaiveGiftWrappedInsuredProduct : builds the naive equivalent
    NaiveInsuredProduct ..|> NaiveGiftWrappedProduct : no shared type
```

</details>

## Notes

- `PricedItem` is the **Component**: the interface both plain and decorated
  products share. Client code only ever depends on this.
- `Product` is the **Concrete Component**: a plain item with no extras.
- `ProductDecorator` is the abstract **Decorator**: it implements
  `PricedItem` and holds a `PricedItem` reference, but adds no fee of its
  own — that is left to its subclasses.
- `GiftWrapDecorator`, `InsuranceDecorator`, and `ExpressHandlingDecorator`
  are **Concrete Decorators**: each adds exactly one fee and one
  description suffix on top of whatever it wraps.
- `NaiveGiftWrappedProduct`, `NaiveInsuredProduct`, and
  `NaiveGiftWrappedInsuredProduct` share no common supertype — each
  re-derives its own fee logic independently, which is exactly why the
  decorator stack is worth having.
