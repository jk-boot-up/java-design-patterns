# Microkernel Pattern

```
src/main/java/com/jk/explore/microkernel/
├── MicrokernelDemo.java             the six acts
├── Kernel.java                      keeps plugins, starts, stops and runs them
├── Plugin.java                      the only thing the core knows
├── BasePlugin.java
├── PercentOff.java                  a plugin
├── Fee.java                         a plugin
├── BrokenPlugin.java                a plugin that throws
│
└── MonolithCheckout.java            every feature inside
```

**Microkernel: a small core that keeps and runs plugins, with every feature in a plugin.**

This project is in [architectural-design-patterns](..). It is [Strategy](../../behavioural/strategy-pattern) and [Chain of Responsibility](../../behavioural/chain-of-responsibility-pattern) raised to the level of a whole application, and the shape of IDEs and browsers.

## Run

```bash
./gradlew run
```

Six acts. Every number quoted below comes from this program's own output.

```
ONE. Every feature inside.
  gift wrap asked for. supported: false. total: 10000, unchanged.
  to add it, edit the checkout, test all of it again, and release all of it.
TWO. A core and plugins.
  plugins: [member-discount, shipping-fee]. total of 10000: 9500.
  the core knows one interface, Plugin, and nothing about discounts or fees.
THREE. A new feature, no change to the core.
  gift wrap registered while running. plugins: [member-discount, shipping-fee, gift-wrap]. total: 9800. started: true.
  and taken away again. stopped: true. total: 9500.
FOUR. A plugin that breaks.
  total: 9500, so the other plugins still ran.
  recorded: [loyalty-points: loyalty-points lost its connection].
FIVE. Order matters.
  discount then fee: 9500. fee then discount: 9450.
  the same two plugins, a different price. the core cannot know which is right.
SIX. The bill.
  the interface offers one thing: adjust a total. wanted by plugins: [adjust a total, read the customer's country, add a line to the receipt].
  a plugin that needs the country cannot get it. either the interface grows, and every plugin feels it, or plugins reach round the core.
  and a customer's total is now decided by whichever plugins happen to be installed, in some order.
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
| [`docs/microkernel-pattern-explained.md`](docs/microkernel-pattern-explained.md) | The pattern, and six acts |
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

Eclipse and IntelliJ, VS Code extensions, Maven and Gradle plugins, and the Linux kernel's loadable modules.

## When this is too much

If the features are few and fixed, plain classes are simpler. A plugin system costs an interface, a lifecycle and a way to order things, and pays off only when the set of features truly varies.

## Where this sits

This project is in [`architectural-design-patterns`](..), and is meant to be read with its neighbours there.
