# Onion Architecture Pattern

```
src/main/java/com/jk/explore/onion/
├── OnionDemo.java                   the six acts
├── DependencyRule.java              checks that no class refers outward
│
├── domain/model/                    ring 0: Order, OrderLine, OrderRepository
├── domain/service/                  ring 1: PricingService
├── application/                     ring 2: PlaceOrderService
├── infrastructure/                  ring 3: two storages, a database
├── ui/                              ring 3: ConsoleApi
│
└── naive/
    └── NaiveOrder.java              a core class that reaches outward
```

**Onion architecture: business rules at the centre, and every dependency pointing inward.**

This project is in [architectural-design-patterns](..). It sits with [Hexagonal Architecture](../hexagonal-architecture-pattern) and [Clean Architecture](../clean-architecture-pattern) as one of three ways to say the same rule, and it is the shape behind [Repository](../../enterprise-design-patterns/repository-pattern) and [Dependency Injection](../../foundational-design-patterns/dependency-injection-pattern).

## Run

```bash
./gradlew run
```

Six acts. Every number quoted below comes from this program's own output.

```
ONE. The core reaches outward.
  the order saved itself with a SQL statement. statements run: 1.
  to change the storage, the order class, at the centre, must be edited.
TWO. Rings, and one rule.
  ring 0: order, order line, the repository idea. ring 1: pricing rules. ring 2: use cases. ring 3: storage and screens.
  the rule: a class may refer to its own ring, or to a ring further in. never outward.
  violations among the 8 classes of the onion: 0.
THREE. Checking the rule.
  the naive order: [NaiveOrder (ring 0) refers to SqlDatabase (ring 3)].
  the checker reads the fields, constructors and methods of each class, so the rule is tested, not just hoped for.
FOUR. Swap the outside.
  in memory: total 10800. as a text record: total 10800. the record: ORD-1|MUG:2:6000|discount:1200.
  the use case, the rules and the order were not touched.
FIVE. The inside, on its own.
  small order total: 950. big order total: 10800 (10% off 12000).
  no storage, no screen, no framework was used to check the rules.
  through the outside, the same order: ORD-3 total 10800.
SIX. The bill.
  one order saved and read back through the outer ring: conversions 2. every trip across a ring may copy the order into another shape.
  and to place one order there are 4 classes in 3 rings, plus the repository idea. for a small program, that is a lot of ceremony.
  the repository idea lives in the centre, so the centre knows that storage exists, though not how.
```

## Test

```bash
./gradlew test
```

2 test classes, 7 test methods, offline, with nothing installed and no framework.

## Technologies and versions

| What | Version | Why it is here |
| --- | --- | --- |
| Java | 21 | The repository standard, via the Gradle toolchain block |
| Gradle | 9.2.1 | The wrapper in this directory; no separate install needed |
| JUnit 5 | 5.10.2 | Test runner |

No framework. A hand-built project stays plain Java so the mechanism is the whole lesson.

## Learning Material

| Document | What it covers |
| --- | --- |
| [`docs/problem-statement.md`](docs/problem-statement.md) | The scenario, and the problem |
| [`docs/onion-architecture-pattern-explained.md`](docs/onion-architecture-pattern-explained.md) | The pattern, and six acts |
| [`docs/class-diagram.md`](docs/class-diagram.md) | The types |
| [`docs/architecture-diagram.md`](docs/architecture-diagram.md) | The parts and how they connect |
| [`docs/data-flow-diagram.md`](docs/data-flow-diagram.md) | What happens to one request |
| [`docs/sequence-diagram.md`](docs/sequence-diagram.md) | Written for a listener with the screen off |
| [`docs/uml-diagram.md`](docs/uml-diagram.md) | Four sequences |
| [`docs/animation.html`](docs/animation.html) | The six acts in a browser |
| [`docs/prerequisites.md`](docs/prerequisites.md) | What you need to know |
| [`docs/session.md`](docs/session.md) | A one-hour taught session |
| [`docs/spec.md`](docs/spec.md) | The generated specification |
| [`docs/youtube.md`](docs/youtube.md) | Title, description and chapters |

### The pattern in one picture

![Class diagram](docs/images/class-diagram.png)

### Where each piece sits

![Architecture diagram](docs/images/architecture-diagram.png)

### How one request moves

![Data flow diagram](docs/images/data-flow-diagram.png)

### Who calls whom, in order

![Sequence diagram](docs/images/sequence-diagram.png)

### All four sequences

![Sequence one](docs/images/uml-diagram.png)

![Sequence two](docs/images/uml-diagram-2.png)

![Sequence three](docs/images/uml-diagram-3.png)

![Sequence four](docs/images/uml-diagram-4.png)

### Video

Built from [`video/scenes.py`](video/scenes.py) by
[`video/build_video.sh`](video/build_video.sh). The rendered file is not
committed; see the repository README for why.

## Where you have already met this

Domain-driven design projects, Jeffrey Palermo's original onion write-up, and most well-kept Spring codebases that keep the domain free of JPA.

## When this is too much

For a small tool with one fixed storage and few rules, rings are heavier than the problem. They pay off when rules are rich and the outside changes.

## Where this sits

This project is in [`architectural-design-patterns`](..), and is meant to be read with its neighbours there.
