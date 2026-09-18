# Prerequisites

This is the first project in the architectural category, and it is chosen to go
first because it is the architecture most readers already have. If you have ever
organised a codebase into `controller`, `service` and `repository` packages, you
already have the folders this project starts from — what it adds is a test that
notices when somebody reaches past them.

## Knowledge Prerequisites

### Required

- **Java basics** — interfaces, packages, and what it means for one class to
  *import* another.
- **Records** — Java 16's `record`. Every value type in this project (`Money`,
  `Order`, `Product`) is one. If you have not met them, the primer below covers
  everything this project uses.
- **`Optional`** — `orElseThrow`, `map`. Used by the storage interface to say
  "no such order" without a null.
- **What a unit test is**, in general terms — you do not need to have written
  one, but the video assumes you know that a build can run automated checks.

### Helpful, but explained as we go

- **JUnit 5** — `@Test`, `@DisplayName`, `assertThrows`. If this is new, the
  two test classes in this project are short enough to read as the
  introduction.
- **The idea of a dependency rule** — "X may not import Y" — is explained from
  first principles in the pattern-explained document, so nothing here is
  assumed.

### Explicitly NOT required

- **No ArchUnit experience.** This project is many people's first contact with
  it. `ArchitectureTest` is thirty lines and every line is explained.
- **No Spring, no database, no web framework.** The whole project runs offline
  with nothing but a JDK. "Presentation" is a class with a `checkout` method
  that returns a `String`; there is no HTTP anywhere in this category until
  §67.
- **No prior architectural patterns.** This is the category's first project.
  Everything after it is a small step from what is built here, and each later
  project's document says which step.

## A 60-Second "Layers" Primer

A **layered architecture** splits a program into stacked groups of classes,
each group allowed to depend only on the group directly beneath it.

This project has four: **presentation** at the top, turning what a customer
typed into a call and turning the answer into words; **application**, which
runs the checkout as a fixed sequence of steps; **domain**, the nouns of the
business — an order, a price, a product — with no dependency on anything
above or below; and **infrastructure** at the bottom, where the products and
orders are actually kept, the card is actually charged, and the email is
actually sent.

The promise of the arrangement is that a change to one layer should not force
a change to the layers above it. The risk — and this project's whole point —
is that the promise is only as good as whatever enforces it. Draw four boxes
on a whiteboard and nothing stops a developer, on a busy Tuesday, from adding
one import that skips a box. This project shows that happening, shows what it
costs, and then shows the one line that turns "the layers are not supposed to
be skipped" from a sentence into a test.

## A 60-Second "Dependency Rule" Primer

A **dependency rule** is a sentence about imports, stated so precisely that a
program can check it: *no class in package X may depend on a class in
package Y.*

Written on a whiteboard, that sentence is a promise a team makes to itself and
gradually stops keeping. Written as an **ArchUnit** test, it is thirty lines
that read almost exactly like the English sentence, run every time
`./gradlew test` runs, and fail — naming the offending class — the day
somebody breaks it. This project's central scene is watching that failure
happen on purpose.

## Software Prerequisites

| Need | Version | Why |
| --- | --- | --- |
| JDK | 21 or later | Records, the Gradle toolchain |
| Gradle | none to install | The wrapper (`./gradlew`) fetches what it needs |

Nothing else. No Spring, no container runtime, no database.

### Verify Your Setup

```bash
java -version          # expect 21 or later
cd architectural-design-patterns/layered-architecture-pattern
./gradlew test         # expect BUILD SUCCESSFUL, 18 tests
./gradlew -q run       # expect five acts of output, then ACCEPTANCE
```

If `java -version` reports something older than 21, the Gradle toolchain will
try to download a suitable JDK on the first build, which needs a network
connection once.

## Troubleshooting

**`./gradlew: Permission denied`** — `chmod +x gradlew`.

**The demo's "classes in the four layers" count reads 0** — the forced change
in act five counts `.java` files on disk under `src/main/java/.../layered/`,
relative to the working directory. Run `./gradlew run` from the project root,
not from `video/` or anywhere else.

**`£` characters appear as mojibake** — your terminal is not reading UTF-8.
Try `JAVA_TOOL_OPTIONS=-Dfile.encoding=UTF-8 ./gradlew -q run`.

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — the four layers, and the
   one call that ruins them
2. Run `./gradlew -q run` and read all five acts of output
3. [`layered-architecture-pattern-explained.md`](layered-architecture-pattern-explained.md)
   — the pattern, the rule as a test, and the bill
4. [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md)
5. [`animation.html`](animation.html) — step through the five acts in a browser
6. The source, starting with `PlaceAnOrderDemo` and then `PlaceOrderService`
7. `ArchitectureTest` and `ArchitectureRuleCatchesTheShortcutTest` — the same
   rule, passing on the real project and failing on the naive one
