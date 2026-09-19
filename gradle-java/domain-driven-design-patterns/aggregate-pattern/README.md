# Aggregate Pattern

```
src/main/java/com/jk/explore/aggregate/
├── AggregateDemo.java               the six acts
│
├── domain/
│   ├── Order.java                    the aggregate root: the only door, and every rule
│   ├── OrderLine.java                no public constructor
│   ├── Money.java  OrderId.java  CustomerId.java
│   └── InvariantViolated.java        names the rule that was broken
│
├── infrastructure/
│   ├── VersionedStore.java           whole aggregates, each with a version
│   └── Loaded.java  ConcurrentModification.java
│
└── naive/
    ├── LooseOrder.java               public fields, a public list
    ├── EagerOrder.java  CustomerRecord.java   holds the whole customer
    └── CustomerWithOrders.java       an aggregate drawn too big
```

**An aggregate is one unit with one root. Every change goes through the root, so every rule is enforced in one place.**

This is the second project in [domain-driven-design-patterns](..). It builds on [Value Object](../value-object-pattern): `Money` is one, and an aggregate is made of them. It is the pattern that decides where a rule lives, and what is saved together.

## Run

```bash
./gradlew run
```

Six acts. Every number quoted below comes from this program's own output.

```
ONE. A loose order.
  a line of -3 mugs: in. the same machine on two lines: in. total: £5988.50, past the £1000 limit: in.
  a line added to an order already placed: in.
  every rule is true in the head of the person who wrote the caller.
TWO. The root guards the rules.
  0 mugs:            refused, a line has between 1 and 10 of an item
  11 mugs:           refused, a line has between 1 and 10 of an item
  6 mugs:            accepted. 5 more of the same: refused, a line has between 1 and 10 of an item
  two more machines: refused, the order total may not pass £1000.00.
  after place():     refused, a placed order cannot change
  an empty order:    refused, an order cannot be placed empty
THREE. There is only one door.
  order.lines().clear(): UnsupportedOperationException.
  an OrderLine has no public constructor, so none can exist that the order has not checked.
  lines seen from outside: 1, total £16.00.
FOUR. Other aggregates by id.
  three orders that hold the whole customer: 3 customer loads.
  three orders that hold only a CustomerId: 0 customer loads.
FIVE. Saved whole, or not at all.
  clerk A adds beans and saves: accepted.
  clerk B adds tea and saves: ORD-5 was changed by someone else since it was read.
  the order was read whole, changed whole and saved whole, so a half-updated order cannot exist.
SIX. An aggregate drawn too big.
  one aggregate holding the customer and all their orders. two clerks change two different orders.
  the second save: refused, changed by someone else.
  one aggregate per order: both saves accepted.
  the boundary is a choice, and a boundary drawn too wide costs you false conflicts.
```

## Test

```bash
./gradlew test
```

3 test classes, 13 test methods, offline, with nothing installed and no framework.

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
| [`docs/problem-statement.md`](docs/problem-statement.md) | The order, and who enforces its rules |
| [`docs/aggregate-pattern-explained.md`](docs/aggregate-pattern-explained.md) | The pattern, and six acts |
| [`docs/class-diagram.md`](docs/class-diagram.md) | The types |
| [`docs/architecture-diagram.md`](docs/architecture-diagram.md) | A root, its lines, and other aggregates by id |
| [`docs/data-flow-diagram.md`](docs/data-flow-diagram.md) | How a change reaches an order |
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

Every well-designed `Order` class. Frameworks name it too: Axon's `@Aggregate`, and Spring Data's `@AggregateRoot`, for one.

## When this is too much

For a plain record with no rules across its parts, a single class is enough. An aggregate earns its place when rules span several objects.

## Where this sits

This is the second project in [`domain-driven-design-patterns`](..). It uses [Value Object](../value-object-pattern), and the next project, [Domain Event](../domain-event-pattern), is how an aggregate tells the rest of the system what happened.
