# Prerequisites

## Knowledge Prerequisites

### Required

- **Java basics** — interfaces, packages.
- **Records** — Java 16's `record`.
- **[`../hexagonal-architecture-pattern`](../hexagonal-architecture-pattern)** —
  strongly recommended first. This project generalises exactly its
  inversion, and the explained document assumes you already know what a
  port is and who is allowed to name whom.

### Explicitly NOT required

- **No dependency injection framework.** Wiring is done by hand, in
  `main()`, on purpose — see [`clean-architecture-with-spring-pattern`](../clean-architecture-with-spring-pattern)
  for the same graph assembled by a container.
- **No real HTTP, no real file system.** Every adapter in this project is
  in-memory.

## A 60-Second "Dependency Inversion" Primer

Ordinarily, if class A calls a method on class B, A depends on B — A needs
B to exist, typed, on its classpath, to compile.

**Dependency inversion** breaks that: A calls a method on an *interface*
that A itself declares, and B, elsewhere, implements that interface. A
still depends on something — but on an interface it owns, not on B. B now
depends on A's interface, to implement it.

Control still flows the same way it always did: A's call still ends up
running B's code. What changed is which way the *source code dependency*
points. That is the whole idea, and this project's central scene is
watching it happen with a real class, printed to the console rather than
left as a diagram.

## Software Prerequisites

| Need | Version | Why |
| --- | --- | --- |
| JDK | 21 or later | Records, the Gradle toolchain |
| Gradle | none to install | The wrapper (`./gradlew`) fetches what it needs |

### Verify Your Setup

```bash
java -version
cd architectural-design-patterns/clean-architecture-pattern
./gradlew test         # expect BUILD SUCCESSFUL, 16 tests
./gradlew -q run       # expect five acts of output, then ACCEPTANCE
```

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md)
2. Run `./gradlew -q run` and read all five acts, especially act three
3. [`clean-architecture-pattern-explained.md`](clean-architecture-pattern-explained.md)
4. [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md)
5. [`animation.html`](animation.html)
6. The source, starting with `usecases/OrderRepository.java`, then `usecases/PlaceOrderInteractor.java`
7. `ArchitectureRuleCatchesTheShortcutTest` and `BothAddedAtOnceTest`
