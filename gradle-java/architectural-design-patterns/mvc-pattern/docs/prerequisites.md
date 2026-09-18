# Prerequisites

## Knowledge Prerequisites

### Required

- **Java basics** — interfaces, packages, and what it means for one class to
  import another.
- **Records** — Java 16's `record`, used throughout for `Money`, `Order`,
  and the model itself.
- **What a unit test is**, in general terms.

### Helpful, but explained as we go

- **JUnit 5** — `@Test`, `@DisplayName`, `assertThrows`.
- **[`../layered-architecture-pattern`](../layered-architecture-pattern)** —
  not required, but this project assumes the four-layer vocabulary
  (presentation, application, domain, infrastructure) from the category's
  first project and reuses most of its application and infrastructure code
  unchanged. Watching that one first is not necessary, but it will make this
  one faster.

### Explicitly NOT required

- **No UI toolkit, no web framework.** Every view in this project produces a
  `String`; there is no HTML, no templating engine, and no Swing or JavaFX
  anywhere. The lesson is the separation, not the rendering technology.
- **No prior MVC experience.** If you have only ever used MVC through a web
  framework's annotations, this project's classic-versus-web distinction is
  written for you specifically.

## A 60-Second "MVC" Primer

Three roles. A **Model** holds data and does the one calculation that
matters — here, an order's total. A **View** turns that data into text or
pixels and does no calculation of its own. A **Controller** takes an input
(a click, a request, a command-line call) and turns it into a call on the
model, then tells a view to render.

The property worth remembering above all others: **if two views can ever
show different numbers for the same underlying fact, the model has not
actually been separated from the view — a calculation has just been copied
into two places that happen to look tidy.**

## Software Prerequisites

| Need | Version | Why |
| --- | --- | --- |
| JDK | 21 or later | Records, the Gradle toolchain |
| Gradle | none to install | The wrapper (`./gradlew`) fetches what it needs |

### Verify Your Setup

```bash
java -version          # expect 21 or later
cd architectural-design-patterns/mvc-pattern
./gradlew test         # expect BUILD SUCCESSFUL, 19 tests
./gradlew -q run       # expect five acts of output, then ACCEPTANCE
```

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — one order, two views, two
   different totals
2. Run `./gradlew -q run` and read all five acts
3. [`mvc-pattern-explained.md`](mvc-pattern-explained.md) — the pattern,
   classic versus web MVC, and the bill
4. [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md)
5. [`animation.html`](animation.html)
6. The source, starting with `OrderSummaryModel` and `OrderSummaryView`
7. `ViewsAgreementTest` — the test that proves both the guarantee and the bug
