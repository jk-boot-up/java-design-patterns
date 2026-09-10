# Mediator Pattern

Demonstrates the Behavioural **Mediator** design pattern using an online shop's
checkout page as an example. Five controls affect one another; the pattern is
what stops each of them having to know about the other four.

- `CheckoutMediator` — the mediator interface, and it really is this small:
  one method, `changed(FormWidget source)`. A control announces that something
  about it changed, and stops.
- `CheckoutForm` — the concrete mediator, and the only class that knows the
  rules of the page: which couriers a country offers, that gift wrapping is
  domestic-only, what the total is made of, and when Place Order may be
  pressed. Read `changed()` and you have read the whole page.
- `FormWidget` — the colleague base class. Two fields: a name and a mediator.
  The field it deliberately does not have — a reference to another widget — is
  what makes the tangle unrepresentable rather than merely absent.
- `CountrySelector`, `ShippingSelector`, `GiftWrapCheckbox`, `TotalLabel`,
  `PlaceOrderButton` — the five colleagues. Each holds a value and tells the
  mediator when it changes.
- `NaiveCheckoutForm` — the trap, kept for contrast. The same five controls
  wired to each other: nine references, two of them mutual, gathered into one
  file so the tangle can be read at a glance. It charges £2 for gift wrapping
  it has already withdrawn, and leaves Place Order enabled with no courier
  chosen.
- `CheckoutFormDemo` — runnable entry point putting the same shopper through
  both forms.

## Run

```bash
./gradlew run
```

Which prints:

```text
=== Checkout form: every widget wired to every other ===

UK, Express, gift wrapped
  Total: £48   place order: enabled
shopper changes the country to US
  shipping options : [International]
  shipping chosen  : (none)
  gift wrap        : offered=false, ticked=true   <-- still ticked
  Total: £42   <-- £2 for wrapping that will not happen
  place order      : enabled   <-- no courier chosen, and it will let them through

=== Checkout form: every widget wired to the mediator ===

UK, Express, gift wrapped
  Total: £48   place order: enabled
shopper changes the country to US
  shipping options : [International]
  shipping chosen  : (none)
  gift wrap        : offered=false, ticked=false   <-- withdrawn and cleared together
  Total: £40   <-- basket only, nothing chosen yet
  place order      : disabled   <-- the form re-checked itself
shopper picks International shipping
  Total: £52   place order: enabled
```

## Test

```bash
./gradlew test
```

14 tests across 3 classes. `CheckoutFormTest` covers what the page promises: a
country reshapes the courier list, the total follows shipping and gift wrap,
withdrawing gift wrap clears the tick, and the button tracks both choices.
`WidgetIsolationTest` asserts the *structure* by reflection — no widget may
hold a field of a widget type — so the constraint the pattern rests on is
enforced by the build rather than promised by a comment.
`NaiveCheckoutFormTest` pins the tangled form's two wrong answers in place
rather than fixing them, so the "before" picture is something you can run.

## Learning Material

Start here if you are new to the pattern — the docs are ordered as a
learning path.

| Document | What it covers |
| --- | --- |
| [`docs/prerequisites.md`](docs/prerequisites.md) | What to know and install before you start |
| [`docs/problem-statement.md`](docs/problem-statement.md) | The problem the pattern solves, and why the naive approach hurts |
| [`docs/mediator-pattern-explained.md`](docs/mediator-pattern-explained.md) | The pattern itself, the code walked through, pitfalls, and comparisons |
| [`docs/class-diagram.md`](docs/class-diagram.md) | Static structure |
| [`docs/uml-diagram.md`](docs/uml-diagram.md) | Runtime call flow |
| [`docs/animation.html`](docs/animation.html) | Animated, step-by-step walkthrough — open in a browser. Optional narration via the **Narration** button |
| [`docs/session.md`](docs/session.md) | A 60-minute guided session plan for teaching it |
| [`docs/youtube.md`](docs/youtube.md) | Title, description, chapters and thumbnail for publishing the video |
| [`docs/thumbnail.png`](docs/thumbnail.png) | The 1280×720 image to upload as the YouTube thumbnail |
| [`docs/spec.md`](docs/spec.md) | The project specification — problem, code, video and publishing quality bar. Also as [`spec.html`](docs/spec.html) |
| [`video/`](video/) | A narrated video, plus the script and build pipeline |

### The pattern in one picture

![Mediator pattern class diagram](docs/images/class-diagram.png)

### Video

`video/mediator-pattern-explained.mp4` — 1080p, narrated. An audio-only
version is alongside it. See [`video/README.md`](video/README.md) to
rebuild or re-record it.
