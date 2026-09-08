# Proxy Pattern — Class Diagram

Shows the static structure: `HighResolutionProductImage` and both proxies
implement the shared `ProductImage` interface identically. `LazyProductImage` holds
nothing but a SKU until it needs to build the real subject;
`RestrictedProductImage` holds any `ProductImage` — including another proxy —
by composition, which is what lets the two proxies stack. The naive traps
that skip each proxy are drawn alongside to show what the pattern buys you.

![Proxy pattern class diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class ProductImage {
        <<interface>>
        +render() String
        +sku() String
    }

    class HighResolutionProductImage {
        <<real subject>>
        -String sku
        +HighResolutionProductImage(sku)
        +render() String
        +sku() String
        +loadCount()$ int
    }

    class LazyProductImage {
        <<virtual proxy>>
        -String sku
        -HighResolutionProductImage realImage
        +render() String
        +sku() String
    }

    class RestrictedProductImage {
        <<protection proxy>>
        -ProductImage image
        -Role role
        +render() String
        +sku() String
    }

    class Role {
        <<enumeration>>
        SHOPPER
        CATALOG_ADMIN
    }

    class NaiveProductListing {
        <<the trap>>
        -List~HighResolutionProductImage~ images
        +renderFirst() String
    }

    class NaiveAdminImageViewer {
        <<the trap>>
        -ProductImage image
        +view(role) String
    }

    class ProductImageDemo {
        +main(args: String[]) void
    }

    ProductImage <|.. HighResolutionProductImage
    ProductImage <|.. LazyProductImage
    ProductImage <|.. RestrictedProductImage
    LazyProductImage o-- HighResolutionProductImage : lazily built
    RestrictedProductImage o-- ProductImage
    RestrictedProductImage ..> Role
    NaiveProductListing *-- HighResolutionProductImage : built eagerly
    NaiveAdminImageViewer ..> Role
    ProductImageDemo ..> LazyProductImage : builds
    ProductImageDemo ..> RestrictedProductImage : builds
    ProductImageDemo ..> NaiveProductListing : contrasts
    ProductImageDemo ..> NaiveAdminImageViewer : contrasts
```

</details>

## Notes

- `ProductImage` is the **Subject**: the interface the real image and every proxy
  implement identically. Client code depends only on this.
- `HighResolutionProductImage` is the **Real Subject**: expensive to construct,
  modelled with a static load counter rather than an actual delay.
- `LazyProductImage` is a **virtual proxy**: it holds only a SKU until
  `render()` is first called, at which point it builds and caches the
  real subject.
- `RestrictedProductImage` is a **protection proxy**: it holds *any*
  `ProductImage` — a real one or another proxy — and only delegates if the role
  check passes.
- `NaiveProductListing` and `NaiveAdminImageViewer` share no relationship
  with the proxies — each re-implements, inline, the exact concern its
  corresponding proxy was built to centralise.
