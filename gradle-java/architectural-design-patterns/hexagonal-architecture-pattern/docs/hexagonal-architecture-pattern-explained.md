# Hexagonal Architecture, Explained

## The pattern in one sentence

The core defines **ports** — interfaces, in its own language, for whatever
it needs — and **adapters** outside it implement those ports or call
through them, so that every dependency between the core and the outside
world points **inward**, into the core, never out of it.

## Ports and adapters, and the one move that separates this project from the last one

`OrderStore`, `PaymentGateway`, `ProductCatalog` and `Notifier` are all
declared in `core.port` — inside the core. `InMemoryOrderStore`,
`InMemoryPaymentGateway` and the rest live in `adapter`, outside the core,
and implement those interfaces. Compare this with the Layered Architecture
project: there, the equivalent interface — `OrderTable` — lived in
`infrastructure`, the bottom layer, and the application layer reached
*down* to name it. Here the interface lives in the core, and the adapter
reaches *up* to be one.

That is the entire difference between the two projects. The methods on
`OrderStore` are the same three methods `OrderTable` had. Only the package
the interface lives in — and therefore the direction the import points —
changed.

## Two kinds of adapter, and why both matter

**Driven adapters** are called by the core, through a port it declared:
`InMemoryOrderStore`, `InMemoryPaymentGateway`, `InMemoryNotifier`,
`InMemoryProductCatalog`. The core calls them; they never call the core.

**Driving adapters** call *into* the core: `HttpCheckoutAdapter`, simulating
a JSON request; `CliCheckoutAdapter`, simulating a command line. Both hold a
reference to `PlaceOrderService` and call `place` on it. This is the half
most treatments of hexagonal architecture skip, because "swap the database"
is the more familiar demonstration — but a core that only shows the driven
side has only proven half its claim. If the core can really be called from
anywhere, it has to be shown being called from somewhere genuinely
different, not just persisted somewhere different.

## The rule, written where a build can read it

```java
ArchRule rule = noClasses()
    .that().resideInAPackage(CORE + "..")
    .should().dependOnClassesThat()
        .resideInAPackage(ADAPTER + "..");
```

No class in `core`, at any depth, may depend on any class in `adapter`, at
any depth. That single sentence covers both kinds of adapter at once — a
driven adapter the core might have been tempted to name directly, and a
driving adapter that might have been tempted to let the core call back into
it. `ArchitectureRuleCatchesTheShortcutTest` widens the same rule to
`naive.core` and asserts the failure names `NaivePlaceOrderService` and the
adapter it reached for.

## The forced change, performed twice at once

**Driven side.** `InMemoryOrderStore`, a map, is swapped for
`AppendOnlyOrderStore`, an append-only log read backwards — the same swap
Layered Architecture performed, reused here because the point is not the
swap itself but that `PlaceOrderService.java` needs **zero lines changed**
to accept it.

**Driving side, at the same time.** The same `PlaceOrderService` instance
shape is handed to `CliCheckoutAdapter` instead of `HttpCheckoutAdapter`.
Same zero lines changed.

```
files added     : 2   AppendOnlyOrderStore.java, CliCheckoutAdapter.java
files modified  : 1   PlaceAnOrderDemo.java (the composition root)
lines changed   : 4
classes in the core : 14
of those, opened    : 0
of those, never opened : 14
```

Fourteen core classes, not one of them opened, for two simultaneous
swaps — one on each side of the hexagon.

## The bill

**Interfaces for things with exactly one implementation.** `Notifier` has
one adapter in this project. Writing an interface for a class you will
never swap is ceremony, and this project has some of it, in the name of
demonstrating the shape.

**Mapping.** `HttpCheckoutAdapter` translates a `Map<String,Object>` into a
`PlaceOrderRequest`, and translates the result back into a JSON-shaped
string. That translation is real work, done twice — once per driving
adapter — and it is the cost every adapter boundary charges.

**The honest question this project must not dodge.** For an application
that will only ever have one database and one way of being called, is any
of this worth it? Often, no. The value is not in having built the ports —
it is in the core being provably unable to depend on anything outside
itself, which only pays for itself once there is a real second adapter, on
either side, worth having.

## When this is too much

Worth it when a core genuinely needs to be called from more than one place,
persisted in more than one way, or tested without any of its real
infrastructure existing yet. Not worth it for an application that will only
ever have one caller and one store — building three interfaces for classes
that will only ever have one implementation each is indirection with
nothing to show for it beyond the diagram.

## Comparison with the naive version

| | Naive (core imports adapters) | Hexagonal (ports in, adapters out) |
| --- | --- | --- |
| Can the core be unit-tested without an adapter class? | No — its own field types are adapters | Yes — everything it depends on is a port |
| Cost of swapping storage | Edit the core's constructor | Zero core changes |
| Cost of adding a new driving caller | Edit the core to expose whatever that caller needs | Zero core changes — write a new adapter |
| What tells you the core reached into an adapter | Nobody | `ArchitectureTest`, by name, in seconds |
