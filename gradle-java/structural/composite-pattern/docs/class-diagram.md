# Composite Pattern — Class Diagram

Shows the static structure: `Product` (the leaf) and `Category` (the
composite) both implement `CatalogComponent`, and a `Category` holds a list
of `CatalogComponent` children — which may themselves be more `Category`
nodes. The naive alternative is drawn alongside to show what a shared
type buys you.

![Composite pattern class diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class CatalogComponent {
        <<interface>>
        +name() String
        +totalPrice() BigDecimal
        +productCount() int
        +print(indent: String) void
    }

    class Product {
        -String name
        -BigDecimal price
        +totalPrice() BigDecimal
        +productCount() int
    }

    class Category {
        -String name
        -List~CatalogComponent~ children
        +add(child: CatalogComponent) Category
        +children() List~CatalogComponent~
        +totalPrice() BigDecimal
        +productCount() int
    }

    class NaiveProduct {
        <<the trap>>
        -String name
        -BigDecimal price
    }

    class NaiveCategory {
        <<the trap>>
        -String name
        -List~Object~ children
    }

    class NaiveCatalogPrinter {
        <<the trap>>
        +totalPrice(item: Object)$ BigDecimal
        +productCount(item: Object)$ int
    }

    class CatalogDemo {
        +main(args: String[]) void
    }

    CatalogComponent <|.. Product
    CatalogComponent <|.. Category
    Category "1" o-- "0..*" CatalogComponent : children
    NaiveCategory "1" o-- "0..*" NaiveProduct : children (as Object)
    NaiveCategory "1" o-- "0..*" NaiveCategory : children (as Object)
    NaiveCatalogPrinter ..> NaiveProduct : instanceof
    NaiveCatalogPrinter ..> NaiveCategory : instanceof
    CatalogDemo ..> Category : builds a tree
    CatalogDemo ..> NaiveCatalogPrinter : builds the naive equivalent
```

</details>

## Notes

- `CatalogComponent` is the **Component**: the one interface both leaves and
  composites implement, which is what lets `CatalogDemo` call `totalPrice()`
  on either without checking which one it has.
- `Product` is the **Leaf** — no children, so its answers are direct: its
  own price, a product count of exactly one.
- `Category` is the **Composite** — it holds `CatalogComponent` children
  (note the self-referencing association: a `Category`'s children can
  themselves be `Category` nodes) and answers every question by delegating
  to each child and combining the results.
- `NaiveCategory` has to hold `List<Object>` because `NaiveProduct` and
  `NaiveCategory` share no common type — which is exactly why
  `NaiveCatalogPrinter` needs `instanceof` checks that `Category` never
  does.
