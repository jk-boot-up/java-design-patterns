# Prototype Pattern — UML Sequence Diagram

Shows the runtime flow: an existing, fully-assembled listing produces an
independent copy, which is then tweaked without touching the original.

![Prototype pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    actor Client as ProductListingDemo
    participant Master as master:ProductListing
    participant Copy as whiteVariant:ProductListing

    Note over Client,Master: master is already fully assembled — sku, images, attributes, shipping

    Client->>Master: copy()
    activate Master
    Master->>Copy: new ProductListing(sku, title, ..., images, attributes, shippingProfile, ...)
    activate Copy
    Note right of Copy: constructor deep-copies images and attributes<br/>into fresh List/Map — shippingProfile is passed through unchanged
    Copy-->>Master: instance
    deactivate Copy
    Master-->>Client: whiteVariant
    deactivate Master

    Client->>Copy: setSku("EARBUD-WHT")
    Client->>Copy: setTitle("Wireless Earbuds (White)")
    Client->>Copy: attributes().put("color", "White")
    Client->>Copy: images().clear() / images().add(...)

    Note over Client,Master: master.images() and master.attributes() are untouched —<br/>they were never the same List/Map as whiteVariant's

    Client->>Master: shippingProfile()
    Client->>Copy: shippingProfile()
    Note over Client,Copy: both calls return the exact same ShippingProfile instance —<br/>safe because it is immutable
```

</details>

## Notes

- The interesting work happens inside the `copy()` call, before it even
  returns — the constructor it delegates to is what decides, field by
  field, whether to deep-copy or share.
- Every mutation the client makes happens *after* `copy()` returns, on the
  copy alone. `master` is never touched again once it exists.
- Compare with
  [`../../builder-pattern/docs/uml-diagram.md`](../../builder-pattern/docs/uml-diagram.md).
  There, several small calls accumulate state before a final `build()`
  produces the first and only instance. Here, one call produces a second,
  independent instance from state that already existed.
