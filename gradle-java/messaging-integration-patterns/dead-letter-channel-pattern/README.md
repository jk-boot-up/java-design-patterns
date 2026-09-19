# Dead Letter Channel Pattern

```
src/main/java/com/jk/explore/deadletter/
├── DeadLetterDemo.java              the six acts
├── Worker.java                      retries up to a limit, then moves the message aside
├── DeadLetter.java  Message.java
```

**A dead letter channel takes a message that cannot succeed out of the way, and keeps it for a person.**

This is the fourth project in [messaging-integration-patterns](..). It is what [Retry](../../micro-services-design-patterns/retry-pattern) needs at the end of its attempts, and it makes [Idempotent Consumer](../../micro-services-design-patterns/idempotent-consumer-pattern) matter, because a replayed message may already have done part of its work.

## Run

```bash
./gradlew run
```

Six acts. Every number quoted below comes from this program's own output.

```
ONE. A message that can never succeed.
  four orders, one garbled. handled: [ORD-1]. still waiting: 3. attempts made: 11.
  the garbled order is at the head of the line and will never succeed. orders 3 and 4 are stuck behind it.
TWO. A dead letter channel.
  after 3 attempts the garbled order is moved aside. handled: [ORD-1, ORD-3, ORD-4]. waiting: 0. dead letters: 1.
  orders 3 and 4 went through.
THREE. It says why.
  ORD-2: 3 attempts, last error 'cannot read the body of ORD-2', from channel orders.
  the original message is kept exactly, so it can be looked at, and put back.
FOUR. A slow day is not a dead letter.
  ORD-3 failed once, on a timeout, and succeeded on the second attempt. handled: [ORD-1, ORD-3, ORD-4].
  only ORD-2, which fails every time, is a dead letter: [ORD-2].
  retrying is for the first kind of failure, and the dead letter channel is for the second.
FIVE. Fix it, and replay.
  before the fix: handled [ORD-1, ORD-3, ORD-4], dead 1.
  the parser is fixed and 1 dead letter is replayed. handled: [ORD-1, ORD-3, ORD-4, ORD-2], dead 0.
  note the order: ORD-2 was handled after ORD-3 and ORD-4. replay does not restore the order.
SIX. The bill: nobody is looking.
  40 orders, half of them garbled: 20 dead letters, and every one of those orders was accepted from a customer.
  the main channel looks perfectly healthy: 0 waiting. the dead letter channel is where the loss is, and nothing tells anyone to look.
  a dead letter channel needs an alert on its depth, an owner, and a limit on how long a message may stay. each keeps a copy of customer data.
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
| [`docs/dead-letter-channel-pattern-explained.md`](docs/dead-letter-channel-pattern-explained.md) | The pattern, and six acts |
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

Every managed queue service has one, and every operations team has a story about one that filled up unnoticed.

## When this is too much

For a channel where failure is impossible, or where losing a message is fine, a dead letter channel is more to run. Where a message can be poison, its absence is the outage.

## Where this sits

This project is in [`messaging-integration-patterns`](..), and is meant to be read with its neighbours there.
