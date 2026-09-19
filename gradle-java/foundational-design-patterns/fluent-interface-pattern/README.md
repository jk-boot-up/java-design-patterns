# Fluent Interface Pattern

```
src/main/java/com/jk/explore/fluent/
├── FluentDemo.java                  the six acts
├── Query.java                       fluent, and never changes
├── MutableQuery.java                fluent, and changes itself
├── Steps.java                       guided steps: each offers only what may come next
├── Catalog.java                     six products, and the positional find
└── Product.java
```

**Fluent interface: chain calls so that code reads like a sentence.**

This project is in [foundational-design-patterns](..). It is the reading side of [Builder](../../creational/builder-pattern), and the style of Java streams and of the [Specification](../../domain-driven-design-patterns/specification-pattern) queries.

## Run

```bash
./gradlew run
```

Six acts. Every number quoted below comes from this program's own output.

```
ONE. A long list of arguments.
  find("mugs", 2500, true, true, 10): [Blue Mug, Big Mug].
  find("mugs", 2500, false, true, 10) has the two booleans the other way round: [Blue Mug, Gift Mug, Big Mug].
  both compile. which is in stock, and which is the sort? you must count the arguments to know.
TWO. A query that reads like a sentence.
  search().category("mugs").under(2500).inStock().cheapestFirst().first(10): [Blue Mug, Big Mug].
  the same answer as the long call, and every part names itself.
THREE. Leave out what you do not need.
  category only: [Green Tea].
  under 1000, any category: [Blue Mug, Green Tea].
  the order of the optional parts does not matter: [Blue Mug, Big Mug].
FOUR. Does a call change the query?
  never changing: cheap [Blue Mug], dear [Blue Mug, Big Mug, Gift Mug], the base still [Blue Mug, Big Mug, Gift Mug, Travel Mug].
  changing itself: cheap [Blue Mug, Big Mug, Gift Mug], dear [Blue Mug, Big Mug, Gift Mug]. they are the same object: true. the cheap query was spoiled by the dear one.
FIVE. Guided steps.
  at the start, the only thing offered is: [category].
  then: [under]. then: [cheapestFirst, inStock, run].
  [Blue Mug, Big Mug]. a call out of order does not compile.
SIX. The bill.
  under(-5) was accepted. nothing complained.
  it failed at run(): "the price limit is below zero: -5". the mistake and the report are on different steps of one long line.
  a debugger cannot stop between the calls of one chain, and a stack trace names the line, not the step.
  and it is a small language that someone designed: this one has 7 methods to learn, and to keep.
```

## Test

```bash
./gradlew test
```

2 test classes, 8 test methods, offline, with nothing installed and no framework.

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
| [`docs/fluent-interface-pattern-explained.md`](docs/fluent-interface-pattern-explained.md) | The pattern, and six acts |
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

Java streams, AssertJ assertions, Spring's `WebClient` and `HttpSecurity`, and query builders such as jOOQ.

## When this is too much

For two or three obvious arguments, a plain call is shorter. A fluent API costs a class, a design and its upkeep.

## Where this sits

This project is in [`foundational-design-patterns`](..), and is meant to be read with its neighbours there.
