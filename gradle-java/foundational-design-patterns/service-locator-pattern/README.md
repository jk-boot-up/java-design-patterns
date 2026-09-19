# Service Locator Pattern

```
src/main/java/com/jk/explore/servicelocator/
├── LocatorDemo.java                 composition root — the six acts
│
├── domain/                          ← the same three collaborators as the neighbouring projects
│   ├── DiscountPolicy.java  LoyaltyPolicy.java
│   ├── PaymentGateway.java  RecordingGateway.java
│   └── Notifier.java  RecordingNotifier.java
├── pattern/                         ← the real thing
│   ├── ServiceLocator.java           finds or creates; singleton or prototype
│   ├── LocatorCheckout.java          asks the locator; its constructor takes nothing
│   └── ReceiptPrinter.java  Auditor.java   two more classes that ask
└── plugin/                          ← where the pattern is still right
    ├── PaymentMethod.java  CardPayment.java  BankTransferPayment.java
    └── (registered in src/main/resources/META-INF/services, found by java.util.ServiceLoader)
```

**A service locator is a middleman that knows how to find or create what you ask for. It is widely regarded as an anti-pattern, and this project shows why with evidence, and where it is still right.**

This is the fourth project in [foundational-design-patterns](..), and the second of three that answer one question about the same three collaborators. [Registry](../registry-pattern) is a bag of things someone remembered to put in. Service Locator is a middleman that can find or create them. [Dependency Injection](../dependency-injection-pattern) stops the class asking at all. This project makes the case against itself honestly: Service Locator was a reasonable answer to a real problem.

## Run

```bash
./gradlew run
```

Six acts. The same three collaborators as Registry and Dependency Injection, so all three can be compared directly.

```
SERVICE LOCATOR — ask a middleman for what you need

ONE. The advance over a registry: it creates, and decides how long things live.
  nothing has been asked for yet: gateways made 0, notifiers made 0
  three finds of each: gateways made 1 (a singleton), notifiers made 3 (a new one each time).
  created lazily, with a lifetime for each. a registry cannot do either.

TWO. The other advance: it can be swapped for a test.
  the checkout charged the fake we configured: [9000]
  no change to LocatorCheckout. that is a genuine step forward from a registry.

THREE. The bill: the compiler says nothing while a dependency is missing.
  production is configured, and somebody forgot the notifier.
  new LocatorCheckout() compiled, and constructed. the build was green.
  then, at run time, on a real order: no service is configured for Notifier
  and the customer was already charged: [9000] pence.
  the failure arrived in production, after the money moved, not in the build.

FOUR. The bill: every class now depends on the locator.
  classes that call ServiceLocator: [Auditor, LocatorCheckout, ReceiptPrinter]
  each is otherwise pure domain logic, now coupled to infrastructure.
  and a unit test of any of them must configure the locator first, or: no service is configured for DiscountPolicy
  a unit test that needs global set-up is never quite a unit test.

FIVE. Where it is still right: what is available is not known until run time.
  java.util.ServiceLoader found these payment plug-ins, listed in META-INF/services: [card, bank transfer]
  the application could not know them when it was compiled. asking is the whole point.
  ServiceLoader is this pattern in the standard library, and it is nobody's mistake.

SIX. The verdict.
  prefer the alternative. for business logic, do not ask; be given: that is the next project.
  keep a locator for plug-in systems, and for the composition root of a small application.
  the whole difficulty is the word ask. the class asks, so nobody outside it knows what it needs.
  where you have met this: ServiceLoader, JNDI lookups, and Spring's ApplicationContext.getBean().
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
| [`docs/problem-statement.md`](docs/problem-statement.md) | The registry's problems, and what a locator adds |
| [`docs/service-locator-pattern-explained.md`](docs/service-locator-pattern-explained.md) | The evidence against, where it is still right, and the verdict |
| [`docs/class-diagram.md`](docs/class-diagram.md) | The types |
| [`docs/architecture-diagram.md`](docs/architecture-diagram.md) | Classes that ask, and the recipes they ask |
| [`docs/data-flow-diagram.md`](docs/data-flow-diagram.md) | One find: made, reused, or a surprise |
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

Spring's `ApplicationContext.getBean()`, called from a class Spring created, is a locator inside a container. `ServiceLoader` and JNDI lookups are the same idea.

## When this is too much

For business logic. It is right for plug-ins, and for the composition root of a small application.

## Where this sits

This is the fourth of five projects in [`foundational-design-patterns`](..). It follows [Registry](../registry-pattern) and leads to [Dependency Injection](../dependency-injection-pattern).

## Also available with a framework

[Service Locator with Consul Pattern](../service-locator-with-consul-pattern) reruns this idea on a real framework, and shows what the framework adds and where it can undo the pattern. Watch this project first.
