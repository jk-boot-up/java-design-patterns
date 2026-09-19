# Pipe and Filter Architecture Pattern

```
src/main/java/com/jk/explore/pipefilterarch/
├── PipeFilterArchDemo.java          the six acts
├── Line.java                        stages joined by waiting lines; one tick at a time
├── Stage.java                       a waiting line, some workers, a cost in ticks
```

**Pipe and filter architecture: stages that run together, joined by waiting lines you can size and limit.**

This project is in [architectural-design-patterns](..). It is the whole-system side of [Pipes and Filters](../../micro-services-design-patterns/pipes-and-filters-pattern), which shows the steps; this one shows how they run together, and what a bottleneck and a full line do.

## Run

```bash
./gradlew run
```

Six acts. Every number quoted below comes from this program's own output.

```
ONE. One big step.
  parse 1 tick, price 3, pack 1: 5 ticks for each order, one at a time. an order arrives every tick.
  after 30 ticks, orders done: 5.
TWO. Stages joined by waiting lines.
  the same work in three stages, each working while the others do. after 30 ticks, orders done: 8.
  the parse stage takes a new order while price is still on the last one.
THREE. The slowest stage sets the pace.
  waiting in front of each stage: parse 1, price 19, pack 0.
  price takes 3 ticks, so one order leaves every 3 ticks however fast parse and pack are. orders pile up in front of it.
FOUR. Widen only the slow stage.
  three price workers. after 30 ticks, orders done: 22. waiting: parse 1, price 1, pack 1.
  parse and pack were not touched. now they take one order a tick, and that is the new limit.
FIVE. A limit on each waiting line.
  no limit: most orders waiting in one line 19, refused at the door 0.
  limit of 3: most orders waiting in one line 3, refused at the door 14. orders done: 8, the same as without a limit.
  a full line makes the stage before it hold its order, and so on back to the door. that push-back is called backpressure.
SIX. The bill.
  the price stage crashes. orders it was holding, waiting or working on: 20. they were accepted from customers and are gone, unless the lines are kept somewhere that survives.
  and an order now passes through 3 stages and 2 waiting lines, so a single order takes longer than the 5 ticks of work, whenever it has to wait.
```

## Test

```bash
./gradlew test
```

2 test classes, 6 test methods, offline, with nothing installed and no framework.

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
| [`docs/pipe-and-filter-architecture-pattern-explained.md`](docs/pipe-and-filter-architecture-pattern-explained.md) | The pattern, and six acts |
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

Unix pipelines, video and image processing chains, ETL systems, and build systems that run stages in parallel.

## When this is too much

If the work is short, or the stages are about equally fast, a single step is simpler, and the queues only add delay. Stages pay off when parts differ in speed, or need separate scaling.

## Where this sits

This project is in [`architectural-design-patterns`](..), and is meant to be read with its neighbours there.
