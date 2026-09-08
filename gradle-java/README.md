# Design Patterns in Java — A Worked Course

Twenty-five Gang of Four design patterns, each a self-contained Gradle Java 21
project with runnable code, JUnit 5 tests, written notes, diagrams, an animated
walkthrough, and a narrated video.

**Every pattern is taught through the same worked domain: an online store.**
Not a photo gallery, not shapes on a canvas — checkout, catalog, orders,
shipping, payments. The projects are meant to be worked through in sequence, so
a learner who has already met orders, carts and couriers in the previous
project spends none of their attention re-learning the setting and all of it on
the structure being introduced.

Start with [`creational/simple-factory-pattern`](creational/simple-factory-pattern)
and follow the order below.

---

## Creational — making objects

| # | Pattern | What it buys you |
| --- | --- | --- |
| 1 | [Simple Factory](creational/simple-factory-pattern) | Let data choose the class — payment methods |
| 2 | [Static Factory](creational/static-factory-pattern) | Give the constructor a name — discounts |
| 3 | [Factory Method](creational/factory-method-pattern) | One step, left to the subclass — delivery tiers |
| 4 | [Abstract Factory](creational/abstract-factory-pattern) | Choose the whole family at once — regional checkout |
| 5 | [Builder](creational/builder-pattern) | Decide it a piece at a time — purchase orders |
| 6 | [Prototype](creational/prototype-pattern) | Copy the one you already have — product listings |
| 7 | [Singleton](creational/singleton-pattern) | Exactly one, actually enforced — order numbers |

Simple Factory and Static Factory are not in the Gang of Four book. They are
here because they are the idioms everyone actually meets first, and because
Factory Method and Abstract Factory both grow out of them.

## Structural — arranging objects

| # | Pattern | What it buys you |
| --- | --- | --- |
| 8 | [Adapter](structural/adapter-pattern) | One class translates, not every caller — a shipping SDK |
| 9 | [Bridge](structural/bridge-pattern) | Two hierarchies varying independently — notifications × channels |
| 10 | [Composite](structural/composite-pattern) | One tree, one interface, zero `instanceof` — the catalog |
| 11 | [Decorator](structural/decorator-pattern) | Wrap it, don't subclass it — gift wrap and insurance |
| 12 | [Facade](structural/facade-pattern) | One door in front of many — placing an order |
| 13 | [Flyweight](structural/flyweight-pattern) | Stop paying for the same data twice — catalog badges |
| 14 | [Proxy](structural/proxy-pattern) | Same interface, it controls the door — product images |

## Behavioural — how objects decide and talk

**In progress.** The category is specified and planned; the projects are being
built in the order below. See
[`behavioural/docs/spec.md`](behavioural/docs/spec.md) for the scenario each
pattern is taught through and why, and
[`behavioural/docs/implementation-plan.md`](behavioural/docs/implementation-plan.md)
for the build order.

| # | Pattern | Scenario |
| --- | --- | --- |
| 15 | [Strategy](behavioural/strategy-pattern) | Swap the rule, not the code — shipping cost rules |
| 16 | [Observer](behavioural/observer-pattern) | Tell everyone, know no one — order status events |
| 17 | [Command](behavioural/command-pattern) | Make the action an object — undoable cart edits |
| 18 | [Template Method](behavioural/template-method-pattern) | Fix the steps, vary the how — the fulfilment workflow |
| 19 | [State](behavioural/state-pattern) | Behaviour follows the state — the order lifecycle |
| 20 | [Chain of Responsibility](behavioural/chain-of-responsibility-pattern) | Each link answers or passes it on — checkout screening |
| 21 | Iterator | Hide how the walk really works — paging the catalog |
| 22 | Mediator | Components talk through one hub — the checkout page |
| 23 | Memento | Snapshot it, restore it, safely — restoring a saved cart |
| 24 | [Visitor](behavioural/visitor-pattern) | New reports, untouched model — catalog reports |
| 25 | Interpreter | Turn a rule into a tree — promotion rules |

---

## What each project contains

| Path | Content |
| --- | --- |
| `src/` | The pattern applied, plus the naive alternative it replaces |
| `docs/problem-statement.md` | The problem, and why the naive approach hurts |
| `docs/{pattern}-pattern-explained.md` | The pattern, the code, pitfalls, comparisons |
| `docs/class-diagram.md`, `docs/uml-diagram.md` | Structure and runtime call flow |
| `docs/animation.html` | Step-by-step walkthrough — open in a browser |
| `docs/session.md` | A 60-minute guided teaching session |
| `docs/spec.md` | That project's specification and quality bar |
| `video/` | A narrated 1080p video, plus the script and build pipeline |

Each project also carries the naive version of its problem — the code a
competent developer would write without the pattern. The comparison is the
point; a pattern shown without the thing it replaces is just structure.

## Running one

```bash
cd creational/simple-factory-pattern
./gradlew run
./gradlew test
```

Java 21 and no third-party runtime dependencies. JUnit 5 for tests only.

## The standards these are built to

| Document | Covers |
| --- | --- |
| [`docs/video-and-publishing-spec.md`](docs/video-and-publishing-spec.md) | The domain rule, narration, audio and video pipeline, poster and thumbnail, publishing |
| [`docs/implementation-plan.md`](docs/implementation-plan.md) | How the first fourteen were brought up to that standard |
| [`behavioural/docs/spec.md`](behavioural/docs/spec.md) | The behavioural category's scenarios and extra conformance items |

The generators in `docs/` — `make_specs.py`, `make_youtube_docs.py`,
`make_thumbnails.py` — produce the per-project specification, publishing
document and thumbnail from each project's own files, so those cannot drift
from the code they describe.

---

Built by Jayasekhar Konduru.
