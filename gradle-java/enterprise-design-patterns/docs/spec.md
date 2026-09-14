# Enterprise Application Patterns — Category Specification

The seventh category. Seven patterns in **eleven projects**, numbered 52 to 62,
on the patterns from Martin Fowler's *Patterns of Enterprise Application
Architecture* that sit between an application's objects and its database.

Seven projects build the mechanism by hand. Four more build the same pattern
inside the framework a reader actually uses, and **each of those is a separate
project** with its own README and its own video rather than a subdirectory of the
hand-built one. §2a says which four, and why not all seven.

This document fixes what each project is before any of it is written. It is the
contract; [`implementation-plan.md`](implementation-plan.md) is the schedule.

---

## 1. Scope

Seven patterns, in learning order, built by hand:

| # | Project | One line |
| --- | --- | --- |
| 52 | `data-mapper-pattern` | The object that does not know it is a row |
| 53 | `identity-map-pattern` | The same customer, loaded twice, in two states |
| 54 | `unit-of-work-pattern` | Save half an order and nothing else |
| 55 | `lazy-load-pattern` | Loading one order, and getting the whole catalogue |
| 56 | `repository-pattern` | Query the collection, not the table |
| 57 | `service-layer-pattern` | Where does "place an order" actually live? |
| 58 | `dto-pattern` | The object that crosses the boundary |

Then four framework projects, each pairing with one of the above:

| # | Project | Pairs with | One line |
| --- | --- | --- | --- |
| 59 | `identity-map-with-jpa-pattern` | §53 | The persistence context, and the same customer twice |
| 60 | `unit-of-work-with-spring-pattern` | §54 | `@Transactional`, and the flush you did not write |
| 61 | `lazy-load-with-hibernate-pattern` | §55 | `LazyInitializationException`, explained from its mechanism |
| 62 | `repository-with-spring-data-pattern` | §56 | An interface with no implementation |

The framework projects come after all seven hand-built ones, never before their
partner, and each one opens by naming the project it pairs with.

The order is Fowler's own dependency order and is not negotiable. Data Mapper is
the foundation — everything else assumes objects and rows are separate. Identity
Map solves the duplicate-instance problem Data Mapper creates. Unit of Work needs
the Identity Map to know what changed. Lazy Load is the performance escape hatch
that all three make possible. Repository sits on top of the four and hides them.
Service Layer sits above Repository. DTO is last because it is about what leaves
the building, and you must know what is inside first.

---

## 2. Why this category exists

**This is the most directly useful category in the course.** Every Java developer
who touches Spring, JPA or Hibernate is using all seven of these patterns
whether they know it or not, and most do not. The persistence context *is* an
Identity Map. `@Transactional` *is* a Unit of Work. `save()` on a Spring Data
interface *is* a Repository over a Data Mapper. `LazyInitializationException` is
what a Lazy Load does when its session has gone.

> **The category's thesis: a framework you cannot explain is a framework you
> cannot debug.**

That fixes the teaching method. Each project builds the mechanism by hand, in
plain Java, against an in-memory table — small enough to read in one sitting —
and *then* shows the same thing happening inside the framework, so the reader
recognises it. The hand-built version is not a toy standing in for the real
thing; it is the real thing with the volume turned down.

This is also why this category has the strongest case in the whole course for
building the framework version too — and for four of the seven patterns that
framework version is a project of its own. §2a says which, and why.

### What makes these teachable in one JVM

Everything here already runs in one process. Fowler's patterns are about the
boundary between objects and *storage*, not between machines, and an in-memory
map with an explicit `flush()` shows that boundary exactly. No simulation is
being strained. That is why this category is low-risk compared with the platform
one.

---

## 2a. By hand first, then in the framework — and the framework version is its own project

**The hand-built project is the primary one.** Plain Java, offline, an in-memory
table, deterministic tests under two seconds. It holds the naive version, the
pattern, the failure and the cost, and its teaching video is built entirely from
it. A reader who installs nothing gets the whole pattern.

**The framework version is the same pattern inside JPA, Hibernate or Spring
Data** — and where it is worth building, it is **a separate project**, not a
`real/` subdirectory of the hand-built one. The reason is that a project in this
repository is the unit a viewer consumes: one project, one README, one video, one
lesson. A framework demo buried inside another project is a lesson nobody is
taught, and it also drags a database and a container onto a project whose whole
promise was that it needed neither.

### Which patterns get a framework project, and which get a scene

Not all seven, because a second project has to have its own lesson. The test is
whether the framework version has **a failure mode, an artefact or a claim of its
own that the hand-built project cannot show**. Four pass that test:

| # | Framework project | What only it can show |
| --- | --- | --- |
| 59 | Identity Map with JPA | Load the same customer twice in one persistence context and `==` is true — the single best "oh, *that* is what that is" moment in the course — and then the detached-entity trap, where two contexts give you two objects again. |
| 60 | Unit of Work with Spring | `@Transactional` on a method, and the writes appearing at commit rather than where the code is. The failure of its own: a rollback triggered by an exception the reader did not expect to be a rollback trigger, and a `flush()` happening at a moment nobody wrote. |
| 61 | Lazy Load with Hibernate | A real `LazyInitializationException`, on purpose, with the session closed — the most-Googled exception in Java, explained from its mechanism rather than worked around. Then the three usual fixes and what each costs. |
| 62 | Repository with Spring Data | An interface with no implementation that works, a derived query method generated from its own name, and the leak: `findAll()` returning entities the caller then modifies outside a transaction. |

The other three patterns keep their framework material as **one scene inside the
hand-built project**, filmed from a small `real/` directory that is excluded from
`./gradlew test`, because in each case the framework adds recognition rather than
a new lesson:

| Pattern | Framework material | Why a scene rather than a project |
| --- | --- | --- |
| Data Mapper | A JPA entity and its generated SQL, logged | The SQL is worth seeing beside the hand-written mapper, but the interesting failures it leads to belong to §61 and §62. |
| Service Layer | A `@Service` and where its transaction boundary sits | Mostly annotation placement. That is a real decision, and it is one scene's worth of one. |
| DTO | Jackson serialising a record at a REST boundary | Shows why the entity must not be the thing returned. The lesson is §58's; Jackson only confirms it. |

### Rules that bind every framework project

1. **Its partner is built, finished and published first.** §59 to §62 are only
   legible to someone who has seen the mechanism by hand.
2. **It copies its partner's domain unchanged** — same `Customer`, `Product`,
   `Order`, `OrderLine`, same scenario, same numbers — so the comparison is about
   the mechanism and nothing else.
3. **It does not re-teach the pattern.** Its partner owns that. It opens by
   naming the partner, and spends its time on the one thing it adds.
4. **It explains its dependency.** Hibernate, Spring and H2 are heavy things to
   ask of a beginner, so each carries a `docs/dependencies.md` saying what the
   dependency is in plain language, why the project uses it, what to install with
   the version pinned, what it costs, and that **skipping the project loses none
   of the pattern**. The video says the same aloud before the first annotation.
5. **No framework appears in a hand-built project's build files.** Projects 52 to
   58 stay plain Java, so a reader who wants the mechanism without the framework
   gets exactly that. That separation is the reason 59 to 62 exist as projects.

---

## 3. The store, continued

Same online shop. The persistent objects are `Customer`, `Product`, `Order` and
`OrderLine`, and the relationships are the ones every reader already has in
their head: an order belongs to a customer and has many lines, each line points
at a product.

One shared scenario runs through the category and is worth naming, because six
of the seven projects turn on it:

> **A customer places an order with three lines, and the stock update for the
> third line fails.**

Data Mapper writes the rows. Identity Map decides whether the customer object in
the order is the same object the caller holds. Unit of Work decides whether the
first two lines survive. Lazy Load decides how much of the catalogue got loaded
on the way. Repository is how the code asked for the customer in the first
place. Service Layer is where that whole story is written down. One scenario,
seven views of it.

---

## 4. The eleven projects

Each project shows a naive version failing, then the pattern, then the bill.

### 4.52 Data Mapper — the object that does not know it is a row

**Scenario.** `Customer` needs to be stored and loaded.

**The naive version.** Active Record: the object saves itself. `customer.save()`.
The demo shows it working, and it works well — the project must be fair to it,
because for a simple application it is the right answer and saying otherwise is
dishonest teaching.

Then the cost arrives. `Customer` now knows about tables, columns and SQL. A
change to the schema changes the domain object. Testing the domain needs a
database. And the demo shows the moment it really breaks: one object mapped
across two tables, and one table feeding two objects — the shape Active Record
has no answer for.

**The pattern.** A mapper class that moves data between the object and the row.
`Customer` has no persistence code at all, and the demo prints the class to
prove it: fields, behaviour, nothing else.

**The bill.** A second class per entity, and the mapping is written by hand and
easy to get subtly wrong — the demo shows a field that silently does not
round-trip. Loading an object graph means deciding how far to go, which is §55's
problem. And you have built an indirection that must be understood before
anything can be debugged.

### 4.53 Identity Map — the same customer, twice

**Scenario.** An order is loaded. Its customer is loaded. Separately, the caller
loads the same customer by id.

**The naive version.** Two loads, two objects. The demo shows the bug this
causes in a way nobody forgets: change the address on one, save both, and one
change silently disappears. Two objects claim to be customer 7, they disagree,
and the last writer wins. `equals()` is a partial fix and the demo shows why it
is not enough — the objects are equal and still separately mutable.

**The pattern.** A map, scoped to the session, from id to loaded object. Ask for
customer 7 twice and get the *same object* both times — `==`, not just
`equals`. The demo prints the identity check.

**The bill.** The map is a cache, so it can be stale: another process changed
the row and this session cannot see it. It holds references, so a long session
leaks memory — the demo shows the map growing through a bulk load. And its scope
is now a decision with consequences: per request, per session, or per
application, each wrong in a different way.

**The framework moment.** This is the JPA persistence context. Tier 2 loads the
same entity twice in one transaction and shows `==` being true, and a reader who
has fought that behaviour without understanding it finally sees the mechanism.

### 4.54 Unit of Work — save half an order

**Scenario.** Placing an order writes an order row, three line rows, and three
stock decrements. The third stock update fails.

**The naive version.** Each object saves itself as it changes. The demo runs it
and prints the wreckage: an order exists with two lines, stock is wrong for two
products, and nothing in the system knows it is broken. There is no way to undo
it because the writes have already happened.

The second naive version is the one experienced readers reach for — wrap it in a
transaction — and the project must be honest that this mostly works. Its cost is
that the transaction is open for the whole computation, including the slow
parts, and the demo shows lock contention growing with the duration.

**The pattern.** Register what changed — new, dirty, removed — and write it all
at commit, in one go. Nothing touches the database until the unit of work
commits, so the failure happens before any write and rolls back to nothing.

**The bill.** Order of writes matters and the unit of work has to work it out —
insert the order before the lines, or the foreign key fails. It must know what
is dirty, which means either checking every field or being told. In-memory state
now disagrees with the database until commit, which surprises people. And the
whole change set lives in memory, so a bulk update is a memory problem.

### 4.55 Lazy Load — loading one order, getting everything

**Scenario.** Load one order to show it on a page.

**The naive version.** Eager loading everything reachable. The demo counts the
objects: one order pulls its customer, the customer's other orders, their lines,
their products, and the products' categories. The count is printed, and it is
absurd, and it comes from an object graph with no cycle in it and no obvious
mistake.

**The pattern.** Load the order; load the rest when it is asked for. The demo
shows four variants honestly — lazy initialisation, virtual proxy, value holder,
ghost — because a reader will meet all four in real code.

**The bill, which is heavy and must not be softened.** You have replaced one
large query with many small ones, and the demo shows **N+1** happening: a list
of 20 orders, 21 queries, and a page that is slower than the eager version it
replaced. You have made a field access into I/O, which means it can now be slow
and it can now fail. Threading breaks: the object is passed somewhere its
session no longer exists, and the load fails at the point of use rather than at
the point of loading.

**The framework moment.** That last failure has a name, and Tier 2 produces it
on purpose: `LazyInitializationException`. It is one of the most-searched Java
errors there is, and the project explains it from the mechanism rather than
offering the usual workaround.

### 4.56 Repository — query the collection, not the table

**Scenario.** Find customers in London who have ordered in the last month.

**The naive version.** SQL in the service class. The demo shows the drift: the
same query written slightly differently in three places, one of them wrong, and
a schema change that requires finding every string in the codebase that mentions
a column.

**The pattern.** An interface that looks like an in-memory collection of domain
objects. The service asks for customers; it does not know a database exists. The
demo swaps the backing store from the in-memory table to a different one **with
no change to the calling code**, and that swap is the project's strongest
moment — it must be shown as a real diff, not asserted.

**The bill.** Every real repository grows query methods until it is a query
language with worse ergonomics —
`findByCityAndOrderDateAfterAndStatusIn` — and the demo shows that name being
reached honestly. Specifications fix it and cost a concept. The abstraction
leaks the moment performance matters, because the caller cannot express a join
hint. And "it lets you swap the database" is a benefit that is claimed far more
often than it is used, which the project should say.

### 4.57 Service Layer — where does "place an order" live?

**Scenario.** Placing an order: validate the cart, check stock, take payment,
write the order, send an email.

**The naive version.** In the controller. The demo then adds a second entry
point — a CLI for support staff — and the logic is copied. It drifts. A bug is
fixed in one and not the other, and the demo shows a customer getting different
behaviour depending on which door they came through.

The alternative naive version deserves equal time: put it all in the domain
objects. `Order.place()`. The demo shows where that ends — the domain object
needing a payment gateway, an email service and a stock service, and the reader
can see it is no longer a domain object.

**The pattern.** A service layer defining the application's operations. One
`placeOrder`, called by both the web controller and the CLI. It owns the
transaction boundary and the orchestration; the domain objects own the rules.

**The bill, and it is the one that needs naming.** The Anemic Domain Model: push
too much into services and the domain objects become bags of getters with no
behaviour, which is the most common shape in enterprise Java and is widely
considered an anti-pattern. The project must give the honest dividing line —
business rules in the domain, orchestration in the service — and admit that the
line is genuinely hard to draw and that reasonable teams draw it differently.

### 4.58 DTO — the object that crosses the boundary

**Scenario.** A REST endpoint returns a customer.

**The naive version.** Return the domain object. The demo prints the JSON and
the problems are all visible at once: the password hash is in it, the whole
order history is in it (because serialisation touched a lazy collection), it is
enormous, and the field name the client depends on is now the name of a private
field nobody may rename.

**The pattern.** A separate object shaped for the boundary. A Java `record`,
flat, carrying exactly what the client needs. The domain object stays inside.
The demo prints both payloads and their sizes.

**The bill.** Mapping code, everywhere, and it is tedious. Near-duplicate
classes that drift. And the failure mode worth naming: DTOs multiply until there
is a `CustomerDto`, a `CustomerSummaryDto`, a `CustomerDetailDto` and a
`CustomerListItemDto`, at which point the mapping layer is larger than the
domain it protects.

**Its relationship to two other projects.** This is Backends for Frontends
(§40) at the object level rather than the deployment level, and the projects
link to each other. And a DTO is not a domain model — the project must show one
of each, because conflating them is how anemic domains start.

### 4.59 Identity Map with JPA — the persistence context is the map

**What it is.** §53's scenario, unchanged, run through JPA and Hibernate over an
in-memory H2. The same customer, loaded twice.

**The moment.** Load customer 7 twice in one transaction and assert `first ==
second`. It passes, and nobody told Hibernate to do that. The reader has just
built that map by hand, so the assertion lands as recognition rather than magic:
the persistence context is an Identity Map with a different name.

**The failure that is this project's own.** Close the transaction, open a second
one, load customer 7 again — and now `==` is false, because there are two maps.
That is the detached-entity problem, it is where a great deal of real confusion
about JPA lives, and the hand-built project cannot show it because it has only
ever had one map.

**The bill.** An identity map you did not write is an identity map you cannot see.
Its lifetime is the transaction's, which means object identity in your application
now depends on a boundary drawn somewhere else — often by an annotation on a
method you are not looking at.

### 4.60 Unit of Work with Spring — the flush you did not write

**What it is.** §54's half-written order, run under `@Transactional`.

**The moment.** The method body reads like plain code — save, save, save — and
nothing reaches the database until the method returns. The demo prints the SQL
with timestamps so the reader hears that all three inserts happened after the
last line of the method ran.

**The failures that are this project's own.** Two, and both are things teams meet
in production. First, the rollback that did not happen: throw a checked exception
and Spring commits by default, which surprises almost everyone the first time.
Second, the flush nobody wrote: a query issued mid-method forces earlier writes
out early, so the order of SQL is not the order of the code.

**The bill.** The transaction boundary is now a property of a method signature.
Moving code between methods moves the boundary, and calling a `@Transactional`
method from inside the same class may not start one at all — which is the
proxy-based cost of the convenience, and the project shows it happening.

### 4.61 Lazy Load with Hibernate — the exception everybody has met

**What it is.** §55's order and catalogue, mapped with Hibernate, with one
association left lazy.

**The moment.** Produce a real `LazyInitializationException` on purpose: fetch an
order, close the session, then touch its lines. It is probably the most-Googled
exception in Java, and a reader who has just written a lazy-loading proxy by hand
knows exactly what went wrong — the proxy went to fetch and found no session.
Explained from its mechanism, it stops being a mystery to be worked around.

**Then the three fixes, with their costs.** A join fetch, which loads more than
you needed. An open session in the view, which keeps a database resource open for
the length of a web request. A DTO projection, which is §58 arriving as the
answer. The project recommends the third and says why.

**The N+1 half.** Twenty orders on a page, twenty-one queries logged, and the
count spoken aloud rather than pointed at. Then the same page with a fetch join,
and one query.

**The bill.** Laziness moves a decision from write time to read time, and the
reader loses the ability to tell by looking at a method whether it hits the
database.

### 4.62 Repository with Spring Data — an interface with no implementation

**What it is.** §56's repository, replaced by a Spring Data interface.

**The moment.** Delete the implementation. Leave `interface CustomerRepository
extends JpaRepository<Customer, Long>` with nothing in it, and the application
still runs. Having written the implementation by hand an hour ago, the reader can
say precisely what was generated for them, which is the difference between using
Spring Data and trusting it.

**Then the derived query.** Add `findByEmail(String email)` — no body, no SQL —
and watch the log show the query Spring built from the method name. Then add a
method name with a typo and watch the application fail at startup with a message
naming the property it could not find, which is the honest cost of names as code.

**The leak that is this project's own.** `findAll()` hands back managed entities.
Modify one outside a transaction and nothing is saved; modify one inside a
transaction you did not know you were in, and it is saved without a `save()` call.
A repository that returns live objects is not the collection abstraction §56
promised, and the project says so plainly.

**The bill.** Enormous convenience and a real loss of control: the queries are
generated, the entities are managed, and the abstraction leaks at exactly the
points where performance problems live. The project ends by naming when to drop to
a query you wrote yourself.

---

## 5. Relationships to the existing projects

| Project | Depends on | Why |
| --- | --- | --- |
| Data Mapper | Adapter (§10), Database per Service (§32) | It adapts between two representations; §32 is why each service owns its own. |
| Identity Map | Flyweight (§13), Singleton (§4) | Both are "one instance for one identity", for different reasons — the contrast is instructive. |
| Unit of Work | Saga (§35), Transactional Outbox (§36) | The local transaction those two do not have; §36 writes through this. |
| Lazy Load | Proxy (§14) | The virtual proxy variant *is* Proxy. |
| Repository | CQRS (§34), Facade (§12) | CQRS splits the repository in two; Repository is a Facade over mappers. |
| Service Layer | Facade (§12), Command (§17) | The classic Facade; each operation is close to a Command. |
| DTO | Backends for Frontends (§40), Builder (§2) | The same shaping decision, one layer down. |
| Identity Map with JPA (§59) | Identity Map (§53) | The same mechanism, inside the persistence context. Depends on §53 being published first. |
| Unit of Work with Spring (§60) | Unit of Work (§54) | The same boundary, drawn by `@Transactional`. Depends on §54. |
| Lazy Load with Hibernate (§61) | Lazy Load (§55), Proxy (§14) | Hibernate's proxy is §14, and its failure is the exception everyone has met. Depends on §55. |
| Repository with Spring Data (§62) | Repository (§56) | An interface with no implementation, once the implementation is understood. Depends on §56. |

---

## 6. Deliverables per project

Identical to the microservices category — the same committed file set and the
same generators, per [`../../micro-services-design-patterns/docs/ai-build-spec.md`](../../micro-services-design-patterns/docs/ai-build-spec.md).

Three additions specific to this category:

- A **"Where you have already met this"** section in the explainer, naming the
  framework feature the pattern lives inside — the persistence context,
  `@Transactional`, `JpaRepository` — so a reader connects the hand-built thing
  to the annotated thing they use at work.
- **The demo prints the SQL it would issue**, or the operations against the
  in-memory table. Query counts are this category's equivalent of timings, and
  the N+1 demo is meaningless without them.
- The three patterns whose framework material is a scene rather than a project —
  Data Mapper, Service Layer and DTO — add a small `real/` subdirectory with its
  own README, pinned versions and one command to run it, excluded from the root
  `settings.gradle` so `./gradlew test` never reaches it.
- The four framework projects (§59 to §62) are ordinary projects with the full
  file set, plus a `docs/dependencies.md` written for someone who has never used
  Hibernate or Spring.

---

## 7. Video, poster and publishing

Unchanged: 14 to 16 scenes, `Samantha` at 145 wpm, −16 LUFS, a poster that does
not strike out its message, an outro naming no successor, and the required
four-step opening. Target length eleven to thirteen minutes.

The explanations must work with the listener's eyes closed, which here means
speaking the *counts* — *"twenty orders on the page; twenty-one queries went to
the database"* — rather than pointing at a log.

---

## 8. Deliberately not included

| Pattern | Why not |
| --- | --- |
| Active Record | Taught as the naive version in §52, fairly and without contempt. A project of its own would be the same content twice. |
| Table Module, Transaction Script | Alternative domain-logic organisations from the same book. Genuinely interesting, but they belong in a discussion of domain logic styles rather than as projects; §57 names them. |
| Optimistic and Pessimistic Offline Lock | Concurrency across requests. It needs the concurrency category's harness and would be better placed there if it is ever built. |
| Front Controller, Page Controller, Template View | Web-layer patterns largely absorbed by frameworks. What survives is MVC, which is §64 in the architectural category. |
| Money, Special Case, Range | Base patterns. Special Case is Null Object, which is §68. |
| Metadata Mapping | How ORMs read annotations. It is framework construction, not application design. |

An eighth *pattern* requires editing this section first. Splitting one of the
seven into a further project requires editing §2a first.

---

## 9. Conformance

Every item from the microservices category's §9 applies, plus nine:

- [ ] The explainer has its **"Where you have already met this"** section naming
      the framework feature, and the video says it aloud.
- [ ] **The naive version is treated fairly.** Active Record, SQL in the
      service and logic in the controller are all reasonable in some contexts,
      and the project says when, rather than setting up a straw man.
- [ ] **The demo prints query counts or table operations**, and every count
      quoted anywhere comes from that output.
- [ ] Tier 1 runs offline with only a JDK, and `./gradlew test` passes with no
      database installed and no network.
- [ ] Any `real/` directory pins its framework versions, and its README gives
      one command to run it.
- [ ] Every dependency the project declares has a row in the plan's framework
      register.
- [ ] The project links to the Gang of Four pattern it is built from (§5) and
      does not re-teach it.
- [ ] **No framework appears in the build files of projects 52 to 58.** A reader
      who wants the mechanism without Hibernate, Spring or H2 gets exactly that.
- [ ] **Each framework project (§59 to §62) stands on its own** — its own README,
      documents, poster, thumbnail and video — names its hand-built partner in its
      first paragraph and in its opening scene, uses that partner's domain
      unchanged, does not re-teach the pattern, and carries a
      `docs/dependencies.md` saying what to install, what it costs and that
      skipping it loses none of the pattern.
