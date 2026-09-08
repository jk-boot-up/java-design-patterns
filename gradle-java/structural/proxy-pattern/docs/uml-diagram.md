# Proxy Pattern — UML Sequence Diagram

Shows the runtime interaction for the composed case: an
`RestrictedProductImage` wrapping a `LazyProductImage` wrapping the real
`HighResolutionProductImage`. The role check happens first, and the expensive
load only happens if it passes — and only on the first call.

![Proxy pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    actor Client as ProductImageDemo
    participant Guard as RestrictedProductImage
    participant Lazy as LazyProductImage
    participant Real as HighResolutionProductImage

    Client->>Guard: render()
    activate Guard
    Guard->>Guard: role == CATALOG_ADMIN?
    alt role is CATALOG_ADMIN
        Guard->>Lazy: image.render()
        activate Lazy
        Lazy->>Lazy: realImage == null?
        Lazy->>Real: new HighResolutionProductImage(sku)
        activate Real
        Real-->>Lazy: instance (loadCount + 1)
        deactivate Real
        Lazy->>Real: render()
        activate Real
        Real-->>Lazy: "Rendering SKU-9001 hero image (1920x1080)"
        deactivate Real
        Lazy-->>Guard: "Rendering SKU-9001 hero image (1920x1080)"
        deactivate Lazy
        Guard-->>Client: "Rendering SKU-9001 hero image (1920x1080)"
    else role is SHOPPER
        Guard-->>Client: throws SecurityException
        Note over Guard,Real: Lazy is never even asked -- the real image\nstays unbuilt, loadCount stays unchanged.
    end
    deactivate Guard

    Client->>Guard: render() again
    activate Guard
    Guard->>Lazy: image.render()
    activate Lazy
    Lazy->>Lazy: realImage == null? No -- reuse cached instance
    Lazy-->>Guard: "Rendering SKU-9001 hero image (1920x1080)"
    deactivate Lazy
    Guard-->>Client: "Rendering SKU-9001 hero image (1920x1080)"
    deactivate Guard
```

</details>

## Notes

- The client makes exactly **one** call, `render()`, on the outermost
  proxy. It never touches `LazyProductImage` or `HighResolutionProductImage` directly.
- `RestrictedProductImage` checks the role *before* delegating —
  if the check fails, the call never reaches `LazyProductImage`, so the
  expensive real subject is never built, however many times a denied
  shopper tries.
- `LazyProductImage` checks `realImage == null` on every `render()` call. The
  first call builds and caches the real subject; every call after that
  reuses it, with no further construction cost.
- Two independent decisions — "is this allowed?" and "has this been built
  yet?" — happen in two independent classes, each unaware the other
  exists. That is what makes the composition possible without either
  proxy special-casing the other.
