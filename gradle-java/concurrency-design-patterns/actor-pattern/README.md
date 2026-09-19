# Actor Pattern

```
src/main/java/com/jk/explore/actorpattern/
├── ActorDemo.java                   the six acts
├── Actor.java                       a mailbox, one thread, tell, ask, and restart on failure
├── InventoryActor.java              owns the stock; answers Reserve, Restock, StockOf
├── Messages.java                    the messages, as records
└── SharedStock.java                 the shared map that loses an update
```

**An actor owns its state and its thread. The only way in is a message.**

This project is in [concurrency-design-patterns](..). It generalises [Active Object](../active-object-pattern) to a whole system of objects that only talk by messages, and it adds what Active Object leaves out: replies as messages, and a supervisor.

## Run

```bash
./gradlew run
```

Six acts. Every number quoted below comes from this program's own output.

```
ONE. State that many threads can reach.
  10 in stock. two orders, for 3 and for 4, read the stock at the same moment. it should be 3 left. it is 3 left: false. one of the two reservations was lost.
  every method looked correct. the state was open to anyone.
TWO. State that one actor owns.
  4 threads each send 1000 reservations of 1 mug to an inventory of 4000. stock left: 0.
  no lock in the inventory. the actor handled one message at a time, so none was lost.
THREE. Ask, and be answered by a message.
  reserve 3: Reserved[sku=MUG-BLUE, quantity=3].
  reserve 3 more: OutOfStock[sku=MUG-BLUE, wanted=3, left=2].
  the answer is a message too, and it can be a refusal. no exception crossed between the two.
FOUR. Nobody can reach in.
  the inventory actor has a public method that returns its stock: false.
  the only way to learn the stock is to ask, and the answer is a copy: 5.
FIVE. Let it crash.
  after reserving 2, stock is: 3.
  a message the actor cannot handle: the sender is told, 'a message this actor cannot handle'.
  the actor was restarted: restarts 1. the next message is handled: Reserved[sku=MUG-BLUE, quantity=1].
  one bad message did not stop the actor, or the others.
  the stock after the restart: 4 (it started at 5, and was back to 5 before that last reservation).
SIX. The bill.
  two actors each ask the other, and wait for the answer before doing anything else: no answer.
  no locks, and still a deadlock: each is waiting for a message the other can never send.
  and a restart forgets: an actor's state is gone unless it was written somewhere else. messages are copied, mailboxes can grow, and finding where a message went takes tools.
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
| [`docs/actor-pattern-explained.md`](docs/actor-pattern-explained.md) | The pattern, and six acts |
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

Akka and Pekko, Erlang and Elixir systems, and Vert.x verticles, which follow the same idea.

## When this is too much

For a counter, an `AtomicInteger` is simpler. Actors earn their place when the state is more than one number, and many parts of the system need to change it.

## Where this sits

This project is in [`concurrency-design-patterns`](..), and is meant to be read with its neighbours there.
