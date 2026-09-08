# The Flyweight Pattern — Explained

## One-Line Definition

> **Flyweight** uses sharing to support large numbers of fine-grained
> objects efficiently, by factoring out state that is shared across many
> objects (intrinsic) from state that is supplied by the caller (extrinsic).
> — *Gang of Four, Design Patterns*

It is a **structural** pattern: it is about how objects are *composed to
share state*, not about how they are created (Singleton, Prototype) or how
they behave over time.

## The Two Words That Matter: Intrinsic and Extrinsic

- **Intrinsic state** lives *inside* the shared object. It does not depend
  on context — a `SALE` badge's icon, colours and artwork are the same no
  matter which listing wears it. Safe to share, because it never changes
  per caller.
- **Extrinsic state** lives *outside* the shared object, supplied by the
  caller at the moment it is needed — the listing id, an optional custom
  label. Never store this on the shared object, or it stops being shareable.

The entire pattern is this one separation, applied consistently.

## The Everyday Analogy

Think of a **rubber stamp**. The stamp itself — the carved rubber, the
handle, the ink pattern it produces — is one physical object, reused for
every impression. What changes each time is *where on the page* you press
it, and how hard. The stamp never learns anything about the page; the page
supplies its own context (position) each time it borrows the stamp.

`BadgeStyle` is the stamp. Each listing is a fresh spot on the page.

## The Participants

| Role | In this project | Job |
| --- | --- | --- |
| **Flyweight** | `BadgeStyle` | Holds intrinsic state (type, icon, colours, artwork); accepts extrinsic state as method parameters |
| **Flyweight factory** | `BadgeStyleFactory` | Caches one `BadgeStyle` per `BadgeType`; returns the shared instance instead of building a new one |
| **Context** | `CatalogBadge` | Pairs a shared `BadgeStyle` with one listing's extrinsic state (listing id, custom label) |
| **The trap** | `NaiveListingBadge` | Rebuilds all of the intrinsic state itself, per listing — no sharing |
| **Client** | `BadgeDemo` | Renders badges for several listings and compares both approaches |

## How This Project Implements It

### The flyweight holds only what can be shared

```java
public final class BadgeStyle {
    private final BadgeType type;
    private final String icon;
    private final String backgroundColor;
    private final String textColor;
    private final boolean bold;
    private final byte[] artwork;     // intrinsic — identical for every SALE badge

    public String render(String listingId, String customLabel) {
        // listingId and customLabel are extrinsic — passed in, never stored
        ...
    }
}
```

Nothing about *which listing* is on `BadgeStyle`. That is what makes one
instance safe to hand to 100,000 different callers.

### The factory is what makes sharing actually happen

```java
public final class BadgeStyleFactory {
    private static final Map<BadgeType, BadgeStyle> CACHE = new ConcurrentHashMap<>();

    public static BadgeStyle styleFor(BadgeType type) {
        return CACHE.computeIfAbsent(type, BadgeStyleFactory::build);
    }
}
```

`computeIfAbsent` is doing the entire pattern's work in one line: build once,
on first request, and hand back the cached instance on every request after
that — including from other threads, since `ConcurrentHashMap` makes that
one line safe without any extra locking.

### The context carries the part that cannot be shared

```java
public final class CatalogBadge {
    private final BadgeStyle style;      // shared
    private final String listingId;      // this listing's own
    private final String customLabel;    // this listing's own

    public CatalogBadge(BadgeType type, String listingId, String customLabel) {
        this.style = BadgeStyleFactory.styleFor(type);
        this.listingId = listingId;
        this.customLabel = customLabel;
    }

    public String render() {
        return style.render(listingId, customLabel);
    }
}
```

A `CatalogBadge` is cheap no matter how many exist, because the expensive
part — the `BadgeStyle` — is a reference, shared with every other listing of
the same type.

### The trap, for contrast

`NaiveListingBadge` builds its own `icon`, `backgroundColor`, `textColor`,
`bold` and `artwork` fields inline, from the same `switch` on `BadgeType`,
every single time it is constructed. It renders identical output to the
flyweight version — `BadgeDemo` proves that directly — but two
`NaiveListingBadge` instances of the same type are never `==`, and each one
pays the full construction and memory cost again.

## What You Gain

- **Memory that scales with distinct designs, not with object count.** Four
  `BadgeStyle` instances, however many listings exist.
- **Construction cost paid once per type.** `BadgeStyleFactory.build` runs
  exactly as many times as there are distinct `BadgeType` values.
- **Thread-safe sharing for free.** `ConcurrentHashMap.computeIfAbsent`
  gives every caller the same instance without a lock the client has to
  remember to take.
- **The trap and the fix render identically.** The pattern changes *how
  many objects exist*, not what the objects produce.

## What to Watch Out For

- **Getting intrinsic and extrinsic backwards is the whole risk.** If
  `listingId` were accidentally stored on `BadgeStyle` instead of passed to
  `render()`, the "shared" object would actually belong to one listing, and
  every other listing sharing it would see the wrong id. The discipline is:
  if it varies per caller, it is a parameter, never a field.
- **Only worth it at scale.** For a page with five listings, `BadgeStyle`
  and `NaiveListingBadge` cost about the same. The pattern earns its keep
  specifically when the number of *distinct* variations is small and the
  number of *instances* is large.
- **Mutable flyweights are a bug waiting to happen.** Because one instance
  is shared everywhere, mutating it after construction would corrupt every
  caller at once. `BadgeStyle` has no setters and no mutable fields for
  exactly this reason.
- **The factory's cache lives for the life of the JVM here.** That is fine
  for four fixed badge types. A flyweight keyed by unbounded input (say, one
  per distinct search query) would need an eviction policy, or the cache
  itself becomes the memory leak the pattern was meant to prevent.

## Flyweight vs. Similar Patterns

| Pattern | Intent | Key difference |
| --- | --- | --- |
| **Flyweight** | Share intrinsic state across many fine-grained objects | Many contexts point at *few* shared instances; sharing is the point |
| **Singleton** | Guarantee exactly one instance, globally | One instance total, not one-per-category shared by many contexts |
| **Prototype** | Cheaply produce a near-duplicate of an existing object | Each caller gets its *own independent* copy — the opposite of sharing |
| **Facade** | Simplify a complex subsystem behind one entry point | About hiding many collaborators, not about instance count |

The shortest way to remember it: **Prototype hands out copies. Flyweight
hands out the same instance, again and again.**

## Where You Have Already Seen It

- `Integer.valueOf(-128..127)` — the JVM caches and shares boxed integers in
  that range instead of allocating a new `Integer` every time
- String interning (`String.intern()`) — identical string contents share one
  backing object
- Font glyph caches in text-rendering engines — one glyph bitmap per
  character, reused across every occurrence of that character on the page
- Game engines sharing one mesh/texture across thousands of on-screen tree
  or rock instances, each with its own position (the extrinsic state)

## Try It Yourself

1. Run `./gradlew run` and read the memory arithmetic at the end — it is
   computed from `BadgeStyle.artworkBytes()`, not a hardcoded number.
2. Add a fifth `BadgeType` and confirm `BadgeStyleFactory.instancesCreated()`
   only grows to five, no matter how many `CatalogBadge`s use it.
3. Comment out the `ConcurrentHashMap` in `BadgeStyleFactory` in favour of a
   plain `HashMap`, then run
   `concurrentLookupsForTheSameTypeAllReceiveTheSameInstance` a few times.
   `HashMap` is not safe for concurrent `computeIfAbsent` calls — this is
   the closest this project gets to a flaky test, which is exactly why the
   real implementation does not use one.

## See Also

- [`problem-statement.md`](problem-statement.md) — the problem this solves
- [`class-diagram.md`](class-diagram.md) — static structure
- [`uml-diagram.md`](uml-diagram.md) — runtime call flow
- [`animation.html`](animation.html) — animated walkthrough
