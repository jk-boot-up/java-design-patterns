# Layered Architecture, Explained

## The pattern in one sentence

Split the program into stacked groups of classes — **layers** — where each
layer depends only on the layer directly beneath it, and enforce that rule
with a test rather than a diagram.

## The four layers, and what each one is not allowed to know

| Layer | Package | Job | Must not know |
| --- | --- | --- | --- |
| Presentation | `presentation` | Turn a request into a call, and an answer into words | How orders are stored |
| Application | `application` | Run the checkout as a fixed sequence of steps | How a screen renders, how storage works internally |
| Domain | `domain` | The nouns: `Order`, `Product`, `Money` | Everything — no dependency on any other layer, in either direction |
| Infrastructure | `infrastructure` | Where orders, products, cards and email actually live | Nothing above it exists |

`CheckoutScreen`, the presentation layer, has exactly two imports and both are
the application layer. It does not know whether orders are kept in a map, a
log, or a filing cabinet, and it must never find out — that not-finding-out is
the entire architecture. `PlaceOrderService`, the application layer, runs one
method: check stock, charge the card, reduce stock, save the order, send the
confirmation. Reading it aloud *is* the feature; there is no fifth thing it
does. `Order`, `Money` and the rest of the domain hold no reference to
anything above or below them — an order and a price are true whether or not
anybody is storing them or showing them to a customer. `ProductTable`,
`InMemoryOrderTable`, `CardNetwork` and `EmailServer`, the infrastructure
layer, are where the actual work of keeping and sending happens, and they
know nothing about a use case or a screen calling them.

## The one line that ruins it

The naive `OrderHistoryScreen` lives in `naive.presentation`, and its second
import is not the `OrderTable` interface — it is `InMemoryOrderTable`, the
concrete class, because that was what was sitting in the variable being
copied. It compiles. It works. A reviewer skimming the diff sees a small,
tidy screen and approves it.

That one import is the whole failure mode of layering as it is usually
taught. The four packages are real. The rule that presentation may not touch
infrastructure was never written down anywhere a machine could check it — so
it decayed the first time following it cost fifteen minutes more than not
following it.

## The rule, written where a build can read it

`ArchitectureTest` states three sentences, each one an ArchUnit rule over the
four real layer packages:

```java
ArchRule rule = noClasses()
        .that().resideInAPackage(PRESENTATION)
        .should().dependOnClassesThat().resideInAPackage(INFRASTRUCTURE)
        .because("a screen that reads storage directly is a screen that has "
                + "to be opened every time storage changes, and nothing "
                + "warns you");

rule.check(layers);
```

That is not a comment. It is a test, it runs in `./gradlew test`, and it
fails loudly the moment it is untrue. `ArchitectureRuleCatchesTheShortcutTest`
widens the same rule to include the `naive` package on purpose and asserts
that it goes red, with a failure message naming `OrderHistoryScreen` by name
and `InMemoryOrderTable` as the class it reached for. A green test that has
never been seen red is indistinguishable from a test asserting nothing; this
one has been seen red, deliberately, and the message is printed so you can
read it yourself.

## The forced change, performed and counted

The architecture's claim is always about a future change: *this shape makes
some future change cheap.* So this project performs one.

**Before:** orders live in `InMemoryOrderTable`, a map keyed by order id.
**After:** orders live in `AppendOnlyOrderTable`, a list that is never updated
in place, read backwards to find the newest version of an id — roughly how a
log-structured store behaves, and about as different a storage decision as
one page of code can make.

The composition root — `PlaceAnOrderDemo`, the one place in the whole project
that says `new` for a concrete storage class — changes one line:

```java
OrderTable store = new AppendOnlyOrderTable();
```

Counted from the real files on disk, at the moment the demo runs:

| | |
| --- | --- |
| Files added | 1 — `infrastructure/AppendOnlyOrderTable.java` |
| Files modified | 1 — `PlaceAnOrderDemo.java`, the composition root |
| Lines changed | 1 |
| Classes across the four layers | 17 |
| Of those, opened | 1 |
| Of those, never opened | 16 |

Sixteen classes never opened is the argument. Not the word "decoupled" — the
number.

**And the one that took the shortcut.** `naive/presentation/OrderHistoryScreen.java`
imports `InMemoryOrderTable` directly, so the swap does not compile for it.
Every screen that went through the application layer: untouched. The one
that skipped it: broken by a change it was never involved in.

## Why the order of steps inside the use case matters

`PlaceOrderService.place` charges the card **before** it writes anything
down. Reverse that order — save the order, reduce the stock, then charge —
and a declined card leaves an order in storage and stock missing from the
shelf, with no way to know that neither should have happened. Charging first
means a decline throws before a single thing has changed. This is not
incidental to the layer boundary; it is the kind of decision an application
layer exists to own, in one place, rather than have repeated — and
potentially reordered — at every call site that needed a checkout.

## The bill

Layering is not free, and a project that only shows the benefit is a sales
pitch.

**Indirection.** A field added to the checkout form touches the presentation
layer's request handling, the application layer's request object, and
possibly the domain object it fills. Four layers is four places to touch for
a change that is, underneath, one idea.

**Pass-through layers.** Some methods on `PlaceOrderService` do nothing but
forward a call and reshape its arguments. That is real, it is tedious, and
pretending otherwise does not make it less tedious.

**The bottom layer is still the database.** Notice what `PlaceOrderService`
imports: `OrderTable`, `CardNetwork`, `EmailServer` — all from
`infrastructure`. The application layer still names the concrete package
beneath it, because in a strictly layered design the interface lives with the
implementation, not with the caller. That single fact — the domain and
application layers still depend downward onto infrastructure — is exactly
what the next project in this category, Hexagonal Architecture, exists to
invert. One interface moves up into the core, storage implements it instead
of defining it, and the arrow of dependency reverses. That is the entire
difference between this project and the next one.

## When this is too much

Four layers, one architecture test, and a composition root are worth their
weight for anything with more than one caller of the same business logic, or
anything expected to outlive its first storage choice.

They are not worth it for a script that reads a file, does one calculation,
and prints a result once. A four-package skeleton around fifteen lines of
real logic is not layering, it is packaging — and the tell is the same one
this project's naive version shows in reverse: if writing the request object,
the result object and the service method for a new screen would take longer
than the screen itself is worth, the layers have stopped paying for
themselves.

## Comparison with the naive versions

| | No layers | Layers, unenforced | Layers, enforced |
| --- | --- | --- | --- |
| Can you test pricing alone? | No — one class, one constructor | Yes | Yes |
| Does a shortcut compile? | N/A | Yes, silently | Yes — and the build fails |
| Cost of the storage swap | Rewrite the one class | 1 file safe, 1 file broken silently until compiled | 1 file added, 1 line changed, break caught immediately |
| What tells you the rule was broken | Nobody, until it costs something | Nobody | `ArchitectureTest`, by name, in seconds |
