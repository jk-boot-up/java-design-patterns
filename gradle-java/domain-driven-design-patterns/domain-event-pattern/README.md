# Domain Event Pattern

```
src/main/java/com/jk/explore/domainevent/
├── DomainEventDemo.java             the six acts
│
├── domain/
│   ├── Order.java                    records events, calls nobody
│   ├── DomainEvent.java              a sealed interface
│   └── OrderPlaced.java  OrderCancelled.java   records: facts, in the past tense
│
├── infrastructure/
│   ├── OrderRepository.java          saves the order and its events together; a relay delivers them
│   ├── EventHandler.java  Handlers.java   stock, email, analytics
│   └── Journal.java
│
└── naive/
    └── NaivePlaceOrder.java          calls stock, email and analytics itself
```

**A domain event is a fact in the past tense. The thing that happened says so, and whoever cares reacts.**

This is the third project in [domain-driven-design-patterns](..). It builds on [Aggregate](../aggregate-pattern), which is what raises the events, and on [Value Object](../value-object-pattern), which is what they are made of. Its bill leads straight to the [Transactional Outbox](../../micro-services-design-patterns/transactional-outbox-pattern).

## Run

```bash
./gradlew run
```

Six acts. Every number quoted below comes from this program's own output.

```
ONE. The order calls everyone.
  the mail server is down. the caller gets: mail server timed out.
  order saved: true. what happened: [stock: reserved for ORD-1].
  saved and reserved, the customer told they failed, analytics never counted it.
TWO. The order says what happened.
  events recorded by place(): [OrderPlaced[orderId=ORD-2, customerId=ada, totalPence=4999]].
  the order called nobody. asked again: [].
THREE. Delivered after the save.
  saved. events waiting: 1. reactions so far: 0.
  stock: reserved for ORD-3
  email: confirmed ORD-3 to ada
  analytics: counted ORD-3 for 4999 pence
  events waiting now: 0.
FOUR. A failing reaction does not undo the order.
  the mail server is down. failures: [email failed on OrderPlaced for ORD-4: mail server timed out].
  the others still ran: [stock: reserved for ORD-4, analytics: counted ORD-4 for 4999 pence].
  events still waiting: 1.
  the mail server is back. a second relay: [] failures, waiting: 0.
  the email went out once: 1, and stock was not reserved twice: 1.
FIVE. Events are facts.
  place then cancel: [OrderPlaced, OrderCancelled], in that order.
  each event is a record: it carries the order id and the data, not the order.
  a handler that receives one cannot reach back and change the order.
SIX. The bill: the gap between saving and telling.
  the process stops after the save and before the relay. reactions: 0. events kept: 1.
  after a restart the relay runs. reactions: 3. nothing was lost, because the events were saved with the order.
  publishing straight after the save, with no outbox, would have lost all three.
```

## Test

```bash
./gradlew test
```

3 test classes, 11 test methods, offline, with nothing installed and no framework.

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
| [`docs/problem-statement.md`](docs/problem-statement.md) | The order, and who it must call |
| [`docs/domain-event-pattern-explained.md`](docs/domain-event-pattern-explained.md) | The pattern, and six acts |
| [`docs/class-diagram.md`](docs/class-diagram.md) | The types |
| [`docs/architecture-diagram.md`](docs/architecture-diagram.md) | An order, an outbox and three reactions |
| [`docs/data-flow-diagram.md`](docs/data-flow-diagram.md) | From a change to a reaction |
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

`ApplicationEvent` in Spring, `@DomainEvents` in Spring Data, and every place a system says something happened and let others decide what to do.

## When this is too much

When there is one reaction and the caller needs its answer, a plain call is clearer. An event is for reactions that may come and go, and may happen later.

## Where this sits

This is the third project in [`domain-driven-design-patterns`](..). It follows [Aggregate](../aggregate-pattern), which raises the events, and its bill is the reason for the [Transactional Outbox](../../micro-services-design-patterns/transactional-outbox-pattern).
