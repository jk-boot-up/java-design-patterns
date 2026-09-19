# Rate Limiter Pattern

```
src/main/java/com/jk/explore/ratelimiter/
├── RateLimiterDemo.java             the six acts
├── TokenBucket.java                 capacity, refill rate, exact integer arithmetic
├── RateLimiter.java                 one bucket per caller
├── SearchService.java               counts what it is given beyond its capacity
└── Clock.java                       moves only when told to
```

**A rate limiter says no early. A token bucket allows a burst, then holds callers to a steady rate.**

This project is in [micro-services-design-patterns](..). It protects a service from callers, where [Bulkhead](../bulkhead-pattern) protects callers from each other and [Circuit Breaker](../circuit-breaker-pattern) protects a caller from a service.

## Run

```bash
./gradlew run
```

Six acts. Every number quoted below comes from this program's own output.

```
ONE. No limit.
  the product search can serve 100 requests a second. a client sends 1000 in one second.
  accepted: 1000. beyond what it can serve: 900, and every other customer waits behind them.
TWO. A bucket of tokens.
  a bucket of 10 tokens, refilled at 5 a second. a burst of 20 at once: 10 allowed, 10 refused.
  one second later, another 20: 5 allowed.
  after ten quiet seconds the bucket is full again, and no more than full: 10 allowed.
THREE. A steady rate always gets through.
  5 requests a second for a minute, evenly spaced: 300 of 300 allowed.
  a burst is tolerated up to the size of the bucket. a sustained rate above the refill is not.
FOUR. One bucket for everyone, or one each.
  one shared bucket: the greedy client takes 10. the polite client's one request: refused.
  a bucket each: the greedy client gets 10 of 20. the polite client's one request: allowed.
FIVE. Say when to come back.
  the bucket is empty. the refusal says: retry after 1000 milliseconds.
  one millisecond early: refused.
  at the moment it said: allowed.
SIX. The bill.
  three servers, each with its own bucket of 10: a burst of 90 is allowed 30 times, not 10. the limit is three times looser than it says.
  10000 different callers: 10000 buckets to keep in memory.
  and a real page that loads 12 things at once gets 10 of them. the limit cannot tell a person from a script.
```

## Test

```bash
./gradlew test
```

2 test classes, 11 test methods, offline, with nothing installed and no framework.

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
| [`docs/problem-statement.md`](docs/problem-statement.md) | A search that one client can use up |
| [`docs/rate-limiter-pattern-explained.md`](docs/rate-limiter-pattern-explained.md) | The pattern, and six acts |
| [`docs/class-diagram.md`](docs/class-diagram.md) | The types |
| [`docs/architecture-diagram.md`](docs/architecture-diagram.md) | Clients, a bucket and the search |
| [`docs/data-flow-diagram.md`](docs/data-flow-diagram.md) | What a request does to the bucket |
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

Every public API you have called, GitHub, Stripe, Twitter, and every API gateway.

## When this is too much

For an internal service with one known caller, a limit is only a way to fail. It earns its place with many or unknown callers.

## Where this sits

This project is in [`micro-services-design-patterns`](..), and is meant to be read with its neighbours there.
