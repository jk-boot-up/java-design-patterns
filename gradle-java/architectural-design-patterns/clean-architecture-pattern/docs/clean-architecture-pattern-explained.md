# Clean Architecture, Explained

## The pattern in one sentence

Concentric circles — entities, use cases, interface adapters, frameworks
and drivers — with one rule, stated once and never relaxed: **source code
dependencies point only inward.**

## This is not Hexagonal Architecture again

It is a close relative, and it deserves to be named as one honestly rather
than pretended into something unrecognisable. Both put the business logic
at the centre and both forbid the centre from depending outward. Four
things are genuinely different here, and all four are load-bearing rather
than decorative.

**The concentric rule is one sentence, stated once, rather than a
core-versus-adapter split.** Hexagonal Architecture drew one boundary: core
inside, adapter outside. This project draws three rings — entities, use
cases, interface adapters — because the translation work between a use
case's own data shapes and the outside world's is itself a distinct
responsibility, worth its own ring, not folded into "adapter" as one
undifferentiated outside.

**The dependency-inversion moment is shown in code, explicitly, as two
directions disagreeing.** Act three of the demo prints it in words: control
flows out, to `orders.save(order)`; the dependency points in, at the
interface `orders` is typed as. Most treatments of this idea show the
picture and never say the sentence. This project says the sentence.

**The forced change adds two things at once, rather than swapping one.**
Hexagonal Architecture swapped an existing adapter for a different one on
each side. This project adds a `BatchOrderController` — a second delivery
mechanism — and a `FileBackedOrderRepository` — a second data source —
*alongside* the originals, both still working, proving the architecture
scales by addition and not only by substitution.

**It is honest about being the most over-appliable pattern in the
category.** See "The bill", below.

## The four circles

| Circle | Package | Job |
| --- | --- | --- |
| Entities | `entities` | `Order`, `Money`, `Product` — true regardless of anything outside them |
| Use cases | `usecases` | `PlaceOrderInteractor` and the boundary interfaces it declares |
| Interface adapters | `adapters` | Controllers (external request → use case input), gateways (use case boundary → real storage) |
| Frameworks & drivers | — | `PlaceAnOrderDemo`, the composition root, outside every circle |

## The dependency-inversion moment, in the actual code

```java
payments.charge(order.customerId(), order.total());
...
orders.save(order);
```

`orders` is typed `usecases.OrderRepository` — an interface, declared in
this same package. `InMemoryOrderRepository`, the class that really keeps a
map, lives two circles further out, in `adapters.gateway`, and implements
that interface. When `PlaceOrderInteractor.execute` runs, **control** flows
outward — the call actually lands in `InMemoryOrderRepository.save`. But
the **source code dependency** — the fact that `PlaceOrderInteractor.java`
must have `OrderRepository` on its classpath to compile — points inward, at
an interface the inner circle owns. An annotation-driven container would
make this invisible; wiring it by hand in `main()`, reaching into the
outermost circle for a concrete class and handing it to an interactor that
only ever names an interface, is this project's central scene.

## The rule, as ArchUnit's own layered-architecture API

```java
Architectures.layeredArchitecture()
    .layer("Entities").definedBy("com.jk.explore.clean.entities..")
    .layer("UseCases").definedBy("com.jk.explore.clean.usecases..")
    .layer("Adapters").definedBy("com.jk.explore.clean.adapters..")
    .whereLayer("Entities").mayOnlyBeAccessedByLayers("UseCases", "Adapters")
    .whereLayer("UseCases").mayOnlyBeAccessedByLayers("Adapters")
    .check(classes);
```

Unlike the `noClasses().should().dependOnClassesThat()` rule the earlier
two projects used, this is ArchUnit's dedicated API for exactly this shape
— named layers, and a single sentence for what each one may be reached by.
`ArchitectureRuleCatchesTheShortcutTest` widens an equivalent rule to
`naive.usecases` and asserts it fails, naming `NaivePlaceOrderInteractor`.

## The forced change, performed

**A new delivery mechanism**, added beside the existing one:
`BatchOrderController`, reading CSV-shaped rows the way a nightly import
would. **A new data source**, added at the same time:
`FileBackedOrderRepository`, a structurally different way of keeping an
order than a map ever was. Both depend on exactly what
`CheckoutController` and `InMemoryOrderRepository` already depended on —
`PlaceOrderInputBoundary` and `OrderRepository` — and neither addition
touches a single file in `entities` or `usecases`.

```
files added     : 2   BatchOrderController.java, FileBackedOrderRepository.java
files modified  : 1   PlaceAnOrderDemo.java (the composition root)
lines changed   : 5
classes in entities + use cases : 15
of those, never opened           : 15
```

## The bill, and this must be the most honest project in the category

**Clean Architecture is the most over-applied pattern here, and a project
that only showed its benefit would be a sales pitch.** Look at the file
count for one feature: two entities-adjacent DTOs, four boundary
interfaces, one interactor, two controllers, four gateways — fourteen
files for a single checkout. A CRUD screen built this way has more
interfaces than behaviour.

**It costs real files, real indirection, and a team that must all
understand the rule together**, or it decays into folders with impressive
names and no test enforcing anything. The ArchUnit rule catches an import
violation; it cannot catch a controller that quietly grows business logic
because that was easier than adding a fifth boundary interface.

**When it pays:** long-lived systems, more than one delivery mechanism,
more than one data source, a domain genuinely worth protecting from the
framework of the week. **When it does not:** almost everything smaller
than that. The next project in this category, Clean Architecture with
Spring, is this same graph again — because the version most readers will
actually be handed at work assembles it with a container, and that
comparison is only honest if both sides are real.

## Comparison with the naive version

| | Naive (use case imports gateways) | Clean (use case declares boundaries) |
| --- | --- | --- |
| Testable without a gateway class? | No | Yes |
| Cost of adding a new delivery mechanism | Edit the use case | Zero use-case changes |
| Cost of adding a new data source, alongside the old one | Edit the use case | Zero use-case changes |
| What tells you the use case reached into adapters | Nobody | `ArchitectureTest`, by name, in seconds |
