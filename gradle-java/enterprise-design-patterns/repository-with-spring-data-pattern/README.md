# Repository with Spring Data Pattern

```
src/main/java/com/jk/explore/repositoryspringdata/
├── CustomerApplication.java         the Spring Boot entry point and the six acts
│
├── domain/                          ← the partner's customers and orders, as entities
│   ├── Customer.java
│   └── CustomerOrder.java
├── repository/
│   └── CustomerRepository.java       an interface, and no class implements it
└── service/
    ├── MarketingService.java         the partner's caller, its body unchanged
    ├── Seeder.java                   the six customers, and a statement counter
    └── LeakDemo.java                 the managed entity that leaks, and N+1
```

**An interface with no implementation, that works: Spring Data generates the class, and writes each query from its method's own name.**

This project is the framework version of [Repository](../repository-pattern). That project built two implementations by hand behind one interface. This one has none: the interface is enough, and Spring Data supplies the rest. It does not re-teach the pattern. It shows an interface with no implementation, a query generated from a name, and the leak that comes with it: a managed entity handed to a caller.

## Run

```bash
./gradlew run
```

Six acts. The partner project, Repository, built two implementations by hand. Here there are none: the interface is enough. Every statement count comes from Hibernate's statistics.

```
REPOSITORY WITH SPRING DATA — an interface with no implementation

ONE. An interface with no implementation.
  CustomerRepository is an interface, and this project has no class that implements it.
  the object Spring injected is a generated proxy
  save, findById, findAll, delete: all there, and none of them written.

TWO. A query generated from the method's own name.
  findDistinctByCityAndOrdersDayGreaterThan("London", 70): [Ada, Grace]
  statements issued: 1. no query was written by hand.
  the partner's MarketingService, unchanged, gives: [Ada, Grace]
  the partner had two implementation classes. this project has none, and the application runs.

THREE. The bill — a method per question, and a name that can be wrong.
    findAllWithOrders
    findByCityAndOrderedAfter
    findDistinctByCityAndOrdersDayGreaterThan
    findDistinctByCityAndOrdersDayGreaterThanAndOrdersStatusIn
  a typo in a method name, findByCiity, is caught only when Spring reads it:
  PropertyReferenceException: No property 'ciity' found for type 'Customer'; Did you mean 'c...
  the compiler cannot check a name.

FOUR. The abstraction leaks when performance matters.
  counting every customer's orders, lazily: 7 orders, 7 statements.
  with @EntityGraph on the repository method: 7 orders, 1 statement.
  the interface can say 'join', but only by carrying a persistence hint.

FIVE. The managed entity that leaks.
  a caller inside a transaction changed a customer from findAll(), and never called save.
  Ada's city in the database now: Manchester
  the same change with no transaction around it. Ada's city in the database: London
  written with no save in one case, lost with no error in the other.

SIX. Where you have already met this.
  this is Repository, with the framework supplying the implementation.
  and 'you can swap the database' is still claimed far more often than it is used.
```

## Test

```bash
./gradlew test
```

2 test classes, 8 test methods, offline, each Spring context started inside the test, over in-memory H2.

## Technologies and versions

| What | Version | Why it is here |
| --- | --- | --- |
| Java | 21 | The repository standard, via the Gradle toolchain block |
| Gradle | 9.2.1 | The wrapper in this directory; no separate install needed |
| Spring Boot | 4.1.1 | The container: it wires the beans and generates the repository |
| Spring Data JPA | from Spring Boot 4.1.1 | The repository interface and its generated implementation |
| Hibernate ORM | from Spring Boot 4.1.1 | The JPA implementation underneath |
| H2 | from Spring Boot 4.1.1 | An in-memory database, so nothing is installed |
| JUnit 5 | 5.10.2 | Test runner |

No web starter. This project is about the repository interface, not HTTP. See [`docs/dependencies.md`](docs/dependencies.md).

## Learning Material

| Document | What it covers |
| --- | --- |
| [`docs/problem-statement.md`](docs/problem-statement.md) | The partner's question, and what is new |
| [`docs/repository-with-spring-data-pattern-explained.md`](docs/repository-with-spring-data-pattern-explained.md) | What Spring Data adds, and the leak |
| [`docs/class-diagram.md`](docs/class-diagram.md) | The types |
| [`docs/architecture-diagram.md`](docs/architecture-diagram.md) | The generated class between interface and database |
| [`docs/data-flow-diagram.md`](docs/data-flow-diagram.md) | One call, to managed entities |
| [`docs/sequence-diagram.md`](docs/sequence-diagram.md) | Written for a listener with the screen off |
| [`docs/uml-diagram.md`](docs/uml-diagram.md) | Four sequences |
| [`docs/animation.html`](docs/animation.html) | The six acts in a browser |
| [`docs/prerequisites.md`](docs/prerequisites.md) | What you need to know |
| [`docs/session.md`](docs/session.md) | A one-hour taught session |
| [`docs/spec.md`](docs/spec.md) | The generated specification |
| [`docs/youtube.md`](docs/youtube.md) | Title, description and chapters |
| [`docs/dependencies.md`](docs/dependencies.md) | What Spring Data, Hibernate and H2 are, what they cost, and that skipping this project loses none of the pattern |

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

This is Repository with the framework supplying the implementation. Every `JpaRepository` is one.

## When this is too much

For a handful of queries in one place, Spring Data still saves you two classes. The cost is the leak, which needs to be known about.

## Where this sits

This project pairs with [Repository](../repository-pattern), and is the last of four framework projects in [`enterprise-design-patterns`](..).
