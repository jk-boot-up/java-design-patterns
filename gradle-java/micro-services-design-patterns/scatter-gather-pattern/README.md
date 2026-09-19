# Scatter-Gather Pattern

```
src/main/java/com/jk/explore/scattergather/
├── ScatterGatherDemo.java           the six acts
├── ScatterGather.java               asks all at once, gathers up to a deadline
├── Supplier.java                    a price source: quick, held, or failing
├── Quote.java  Gate.java
└── Latencies.java                   the latency arithmetic, as numbers
```

**Scatter-gather asks many at once and waits for a deadline, not for the slowest.**

This project is in [micro-services-design-patterns](..). It is built on [Timeout](../timeout-pattern), which is its deadline, and it is the composing partner of [API Composition](../api-composition-pattern), which combines answers from different services instead of the same question to many.

## Run

```bash
./gradlew run
```

Six acts. Every number quoted below comes from this program's own output.

```
ONE. Ask them one after another.
  four suppliers answer in [80, 120, 200, 900] milliseconds. asked in turn, the page waits 1300.
TWO. Ask them all at once.
  the same four, asked together: the page waits for the slowest, 900 milliseconds.
THREE. Do not wait for the slowest.
  four suppliers held at once, all being asked together: 4 at the same moment.
  a deadline of 500 ms. quotes gathered: [Quote[supplier=Acme, pence=1250], Quote[supplier=Beta, pence=1190], Quote[supplier=Cargo, pence=1340]].
  missing: [Delta (too slow)]. best price shown: Beta at 1190.
  with the deadline, the page waits 500 ms, not 900.
FOUR. Say what was left out.
  the page shows: best of 2 of 3 suppliers, 1190 from Beta.
  the one that did not answer, Delta, would have been 990. a partial answer is honest only if it says it is partial.
FIVE. A supplier that fails.
  Beta is down. quotes: [Quote[supplier=Acme, pence=1250], Quote[supplier=Cargo, pence=1340]]. missing: [Beta (Beta is down)].
  one failure did not fail the page.
SIX. The bill.
  one page view is now 4 supplier calls. 1000 page views: 4000 calls, to suppliers who see only the traffic, not the pages.
  if each supplier is quick 99 times in 100, asking 1 and waiting for all means 99.0 in 100 pages are quick.
  if each supplier is quick 99 times in 100, asking 4 and waiting for all means 96.1 in 100 pages are quick.
  if each supplier is quick 99 times in 100, asking 10 and waiting for all means 90.4 in 100 pages are quick.
  the more you ask, the more often the slowest one sets the pace. a deadline is what stops it.
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
| [`docs/problem-statement.md`](docs/problem-statement.md) | One question, four suppliers |
| [`docs/scatter-gather-pattern-explained.md`](docs/scatter-gather-pattern-explained.md) | The pattern, and six acts |
| [`docs/class-diagram.md`](docs/class-diagram.md) | The types |
| [`docs/architecture-diagram.md`](docs/architecture-diagram.md) | A page, a gatherer and four suppliers |
| [`docs/data-flow-diagram.md`](docs/data-flow-diagram.md) | What the gatherer does |
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

Price comparison and travel sites, search engines across shards, and any API that fans out to several backends.

## When this is too much

With one source, or when you need every answer without exception, scatter-gather has nothing to gather. With a very large fan-out, the deadline decides more than the data.

## Where this sits

This project is in [`micro-services-design-patterns`](..), and is meant to be read with its neighbours there.
