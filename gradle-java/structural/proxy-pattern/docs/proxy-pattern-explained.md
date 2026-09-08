# The Proxy Pattern

> "Provide a surrogate or placeholder for another object to control access
> to it."
> — Gang of Four, *Design Patterns*

## A Stand-In, Not an Enhancement

It is easy to confuse Proxy with Decorator — both wrap an object behind
the same interface, and both delegate to it. The difference is *intent*.
A Decorator adds new behaviour on top of what it wraps: gift-wrapping adds
a fee that was never there before. A Proxy adds no new behaviour at all —
it controls *access* to behaviour that already exists: whether the real
object gets created yet, whether the caller is allowed to reach it,
whether the call needs to cross a network first. Strip away the proxy and
the visible result should be identical; strip away a decorator and it
usually is not.

## The Bouncer Analogy

A nightclub bouncer is a proxy for the club. Standing at the door, the
bouncer implements the same promise the club makes — "you may enter" — but
decides whether to honour it before the guest ever reaches the room. The
guest never sees an alternate club; they see the same one, just reached
through a checkpoint. That checkpoint is the whole pattern: same
interface, same eventual result, an extra decision-maker in between.

## Participants

| Role | In this project | Responsibility |
| --- | --- | --- |
| Subject | `ProductImage` | The shared interface — the real object and every proxy implement it identically. |
| Real Subject | `HighResolutionProductImage` | The object that is expensive (or restricted) to use directly. |
| Proxy | `LazyProductImage` | Controls *when* the real subject is created — a **virtual proxy**. |
| Proxy | `RestrictedProductImage` | Controls *who* may reach the real subject — a **protection proxy**. |
| Client | `ProductImageDemo` | Calls `render()` without knowing, or needing to know, which kind of `ProductImage` it holds. |

## Code Walkthrough

### The shared interface

```java
public interface ProductImage {
    String render();
    String sku();
}
```

Every class in this project implements `ProductImage` identically. That is what
makes substitution invisible — a client typed to `ProductImage` cannot tell a
real image from a proxy by looking at the type.

### The virtual proxy: defer creation, then cache

```java
public final class LazyProductImage implements ProductImage {

    private final String sku;
    private HighResolutionProductImage realImage;

    public LazyProductImage(String sku) {
        this.sku = sku;
    }

    @Override
    public String render() {
        if (realImage == null) {
            realImage = new HighResolutionProductImage(sku);
        }
        return realImage.render();
    }

    @Override
    public String sku() {
        return sku;
    }
}
```

Constructing a `LazyProductImage` costs almost nothing — it just remembers a
SKU. The expensive `HighResolutionProductImage` only comes into existence
the first time `render()` is called, and after that the proxy holds onto
it, so a second `render()` call reuses the same instance instead of
loading again. `sku()` never touches the real subject at all —
useful for building a list of thumbnails or captions without paying for a
single full load.

### The protection proxy: check before delegating

```java
public final class RestrictedProductImage implements ProductImage {

    private final ProductImage image;
    private final Role role;

    public RestrictedProductImage(ProductImage image, Role role) {
        this.image = image;
        this.role = role;
    }

    @Override
    public String render() {
        if (role != Role.CATALOG_ADMIN) {
            throw new SecurityException("Only catalog admins may view " + image.sku());
        }
        return image.render();
    }

    @Override
    public String sku() {
        return image.sku();
    }
}
```

Notice the constructor takes a `ProductImage`, not a `HighResolutionProductImage`. That
one detail is what makes proxies composable: wrap an
`RestrictedProductImage` around a `LazyProductImage` and you get lazy
loading *and* access control, with neither class aware the other exists.

```java
ProductImage composed = new RestrictedProductImage(new LazyProductImage("SKU-9001"), Role.CATALOG_ADMIN);
composed.render(); // checks the role, then loads (and caches) the real image
```

If the role check fails, the wrapped `LazyProductImage` is never even asked to
load — the real subject stays untouched, which matters when "untouched"
means "never spent the loading cost at all."

## What You Gain

- **The client is oblivious.** `ProductImageDemo` calls `render()` on a
  `ProductImage` and never branches on whether it got the real thing or a proxy.
- **Expensive work happens exactly when it is needed, once.** The virtual
  proxy defers construction and then caches it — no wasted loads, no
  repeated loads.
- **Access rules live in one place.** Every caller that goes through
  `RestrictedProductImage` gets the same rule; there is nowhere else
  for the check to be forgotten.
- **Proxies compose.** Wrapping one proxy in another combines their
  concerns without either needing to know about the other.

## What to Watch Out For

- **A leaky proxy is worse than no proxy.** If `sku()` had needed
  data only the real subject holds, the proxy would have been forced to
  load early just to answer a cheap question — defeating the whole point.
  Keep the proxy's own state (here, just the SKU) enough to answer
  as much as it can without delegating.
- **Caching hides staleness.** `LazyProductImage` caches forever once loaded.
  That is correct here because the underlying file never changes mid-run,
  but a proxy over something mutable needs an invalidation strategy, or
  callers will see stale data indefinitely.
- **Don't reach for Proxy to add behaviour.** If the goal is "add a
  feature," not "control access," that is Decorator's job — see the
  comparison below.

## Proxy vs. Other Structural Patterns

| Pattern | Same interface as wrapped object? | Purpose |
| --- | --- | --- |
| **Proxy** | Yes | Controls *access* — when to create, whether to allow, where the real object lives |
| Decorator | Yes | Adds *new behaviour* on top of the wrapped object |
| Adapter | No — translates one interface to another | Makes an incompatible interface usable |
| Facade | New, simplified interface | Hides a complex subsystem behind one entry point |

Proxy and Decorator have the same UML shape — an object implementing an
interface while holding another instance of it — which is exactly why
intent is the only thing that tells them apart. Ask "does this add
something new, or just guard the way to what's already there?"

## Real-World Sightings

- **Hibernate / JPA lazy-loading proxies** — an entity reference is
  actually a proxy; the real row is fetched from the database only when a
  field is first accessed.
- **`java.rmi` remote proxies** — a local object stands in for one that
  actually lives on another machine, hiding the network call.
- **Spring's `@Transactional` proxies** — the bean you inject is a proxy
  that opens a transaction before delegating to your real method.
- **Firewalls and API gateways** — a network-level protection proxy that
  decides whether a request reaches the real service at all.

## Try It Yourself

1. Add a `LoggingLazyProductImage` that records every `render()` call (to a
   `List<String>`, say) before delegating — a **logging proxy**, another
   GoF variant, alongside virtual and protection.
2. Compose three deep: `LoggingLazyProductImage` wrapping
   `RestrictedProductImage` wrapping `LazyProductImage`. Confirm a denied
   shopper still gets logged, but the real image still never loads.
3. Give `LazyProductImage` an `invalidate()` method that clears the cached
   `realImage`, and write a test proving the next `render()` call
   increments `HighResolutionProductImage.loadCount()` again.
