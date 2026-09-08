# Flyweight Pattern — UML Sequence Diagram

Shows the runtime interaction: two different listings ask for a `SALE`
badge, the factory builds the shared `BadgeStyle` only on the first request,
and both listings render through the same instance. The naive path is shown
alongside for contrast — no factory, no cache, no sharing.

![Flyweight pattern sequence diagram](images/uml-diagram.png)

<details>
<summary>Mermaid source</summary>

```mermaid
sequenceDiagram
    actor Client as BadgeDemo
    participant Factory as BadgeStyleFactory
    participant Style as BadgeStyle (SALE)
    participant Naive as NaiveListingBadge

    Client->>Factory: styleFor(SALE)  [for LST-1002]
    activate Factory
    Factory->>Factory: cache miss -> build(SALE)
    Factory->>Style: new BadgeStyle(SALE, ...)
    activate Style
    Factory-->>Client: shared instance
    deactivate Style
    deactivate Factory

    Client->>Style: render("LST-1002", null)
    Style-->>Client: "[SALE] ★ SALE on LST-1002 ..."

    Client->>Factory: styleFor(SALE)  [for LST-1003]
    activate Factory
    Factory->>Factory: cache hit -> no build
    Factory-->>Client: same shared instance
    deactivate Factory

    Client->>Style: render("LST-1003", "Flash Sale")
    Style-->>Client: "[SALE] ★ FLASH SALE on LST-1003 ..."

    Note over Client,Style: styleFor(SALE) == styleFor(SALE): true — one BadgeStyle, two listings

    Client->>Naive: new NaiveListingBadge(SALE, "LST-1002")
    activate Naive
    Naive->>Naive: build icon, colours, artwork from scratch
    deactivate Naive

    Client->>Naive: new NaiveListingBadge(SALE, "LST-1003")
    activate Naive
    Naive->>Naive: build icon, colours, artwork from scratch, again
    deactivate Naive

    Note over Client,Naive: naiveA == naiveB (both SALE): false — two SALE badges, two full copies
```

</details>

## Notes

- The **second** `styleFor(SALE)` call does no construction at all — the
  cache hit is the entire point of routing every lookup through
  `BadgeStyleFactory` instead of calling `new BadgeStyle(...)` directly.
- Both listings render through the *same* `BadgeStyle` object, passing their
  own `listingId` and `customLabel` as arguments — the extrinsic state never
  touches the shared instance.
- The naive path on the right has no factory step at all: every
  `NaiveListingBadge` repeats the full construction, because there is
  nowhere for a cache to intercept the call.
