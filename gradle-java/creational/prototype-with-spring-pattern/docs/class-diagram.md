# Prototype with Spring Pattern — Class Diagram

`Listing` is prototype scope. `Storefront` is a singleton that takes it two ways.

![Prototype with Spring Pattern — Class Diagram](images/class-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
classDiagram
    class Listing {
        <<@Component, prototype scope>>
        -String title
        -List images
        +copy() Listing
    }
    class Storefront {
        <<@Component, singleton>>
        -Listing injectedOnce
        -ObjectProvider listings
        +draftInjectedOnce() Listing
        +freshDraft() Listing
    }
    Storefront --> Listing : injected once
    Storefront ..> Listing : provider, each call
```

</details>
