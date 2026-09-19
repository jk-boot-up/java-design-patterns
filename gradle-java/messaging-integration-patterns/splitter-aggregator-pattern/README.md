# Splitter and Aggregator Pattern

```
src/main/java/com/jk/explore/splitteraggregator/
├── SplitterAggregatorDemo.java      the six acts
├── Splitter.java                    one message in, one for each line out, each numbered
├── Aggregator.java                  collects by id; completes, or expires with what is missing
├── Part.java  Clock.java
```

**A splitter breaks a message up, and an aggregator puts it back, by the id each part carries.**

This is the third project in [messaging-integration-patterns](..). It follows [Content-Based Router](../content-based-router-pattern), and it is the messaging form of [Scatter-Gather](../../micro-services-design-patterns/scatter-gather-pattern) where the pieces of one thing are worked on separately.

## Run

```bash
./gradlew run
```

Six acts. Every number quoted below comes from this program's own output.

```
ONE. One message, one picker.
  an order of 3 lines is picked by one person, one line after another: 3 steps of work, in a row.
  the aisles are far apart, and the other pickers stand idle.
TWO. Split it.
  ORD-1 part 1 of 3: 2 x MUG-BLUE (aisle 3)
  ORD-1 part 2 of 3: 1 x ESP-001 (aisle 9)
  ORD-1 part 3 of 3: 5 x TEA-050 (aisle 1)
  each part carries the order's id, and its place. that is what lets it be put back.
THREE. The parts finish in any order.
  suppose the three pickers finish in the order: 3 1 2.
  nothing guarantees they come back in the order they went.
FOUR. Gather them by the id.
  part 3 arrives. waiting for the rest.
  part 1 arrives. waiting for the rest.
  part 2 arrives. complete: [2 x MUG-BLUE (aisle 3), 1 x ESP-001 (aisle 9), 5 x TEA-050 (aisle 1)].
  the order came back together, in its original line order, from parts that arrived out of order.
FIVE. A part never arrives.
  parts 1 and 3 arrive. part 2's picker has gone home. open orders: 1.
  after 29 minutes: expired 0.
  after 30 minutes the aggregator gives up: 2 of 3 lines, missing part [2], complete: false.
  without a timeout it would wait for ever, and the customer would too.
SIX. The bill.
  1000 orders each missing one part: 1000 orders held in memory, waiting.
  a part delivered twice: counted once, and 1 duplicate noted. without that, an order could complete with a line twice.
  and two orders with the same id would be mixed into one. the id that ties the parts together has to be unique.
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
| [`docs/splitter-aggregator-pattern-explained.md`](docs/splitter-aggregator-pattern-explained.md) | The pattern, and six acts |
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

Batch jobs that fan out over records, map-reduce, and any order system that sends each line to a different picker or supplier.

## When this is too much

If the parts are quick, or depend on each other, splitting is overhead. If order matters between the parts, an aggregator needs more than the parts.

## Where this sits

This project is in [`messaging-integration-patterns`](..), and is meant to be read with its neighbours there.
