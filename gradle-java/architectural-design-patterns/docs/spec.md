# Architectural Patterns — Category Specification

The eighth category. Four patterns in **five projects**, numbered 63 to 67, on
the patterns that decide the shape of a whole application rather than the shape
of a few classes.

The fifth project exists because Clean Architecture is taught twice — once wired
by hand and once wired by Spring — and **each version is a separate project**
with its own README and its own video. See §4.66 and §4.67.

This document fixes what each project is before any of it is written. It is the
contract; [`implementation-plan.md`](implementation-plan.md) is the schedule.

---

## 1. Scope

Four patterns in five projects, in learning order:

| # | Project | One line |
| --- | --- | --- |
| 63 | `layered-architecture-pattern` | Four layers, and the one call that ruins them |
| 64 | `mvc-pattern` | The view that knew too much |
| 65 | `hexagonal-architecture-pattern` | The application that does not know it has a database |
| 66 | `clean-architecture-pattern` | Which way does the arrow point? |
| 67 | `clean-architecture-with-spring-pattern` | The same graph, wired by a container |

The order is a dependency order. Layered is the architecture nearly every reader
already has, so it goes first and is the baseline the others are measured
against. MVC is the same separation applied at the user-facing edge. Hexagonal
inverts the bottom layer. Clean generalises the inversion and adds the concentric
rule. Each is a small step from the one before, and the projects must be explicit
about which step, because a reader who thinks these are four unrelated
architectures has learned four things instead of one.

---

## 2. The problem with this category, stated first

**This is the category most likely to be vague, and the risk is named here
before anything is built.**

Architecture is taught almost everywhere with diagrams and adjectives.
Boxes, arrows, and words like *decoupled*, *maintainable*, *flexible* — none of
which a reader can run, test or check. Four videos of concentric circles would
be worth nothing, and would be worse than nothing because they would sound
authoritative.

Three rules answer that, and they are what this category is actually built on.

### Rule 1 — One feature, built four times

Every project implements **the same feature**: placing an order. Same
requirements, same domain, same tests where possible. The only thing that
changes is the shape. A reader can therefore diff the projects against each
other, and the comparison is concrete rather than rhetorical.

### Rule 2 — Every architecture is judged by a forced change

An architecture's claim is always about change: *this shape makes some future
change cheap*. So each project **makes that change, on camera, and counts the
cost in files touched and lines changed.** Not described — performed.

| Project | The forced change | What it exposes |
| --- | --- | --- |
| Layered | Replace the storage layer | Whether the upper layers really were independent of it |
| MVC | Add a second view over the same model | Whether logic had leaked into the first view |
| Hexagonal | Swap the database for an in-memory adapter **and** drive the same core from a CLI instead of HTTP | Whether the core is genuinely unaware of either |
| Clean | Add an entirely new delivery mechanism and a new data source at once | Whether the dependency rule held under pressure |

The number of files touched is printed. That number is the argument.

### Rule 3 — The architecture is a test that fails

This is the strongest anti-vagueness device available and every project uses it.
A dependency rule is not a diagram; it is an **assertion**:

> *No class in the domain package may reference anything in the infrastructure
> package.*

That is executable. Each project ships an architecture test that **fails when
the rule is broken**, and each demo breaks the rule on purpose to show the test
going red. A reader leaves knowing that "the domain does not depend on the
database" is something a build can enforce, not something a team promises at a
whiteboard and forgets within a month.

> **If a claim in this category cannot be expressed as a failing test or a
> counted diff, it does not go in the video.**

---

## 3. The store, continued

Same online shop, same feature throughout: **a customer places an order with
three lines; stock is checked; payment is taken; a confirmation is sent.**

That feature is deliberately the same one the Service Layer project (§57) uses,
and the same checkout the Saga (§35) orchestrates and the Strangler Fig (§47)
replaces. A reader arriving here already knows what placing an order involves,
so all their attention goes to the shape.

Each project is small — this category resists size, because an architecture
demonstrated across forty classes cannot be read. One feature, four or five
classes per layer, and the structure visible in a directory listing.

---

## 4. The five projects

### 4.63 Layered Architecture — four layers and the one call that ruins them

**Scenario.** Presentation, application, domain, infrastructure. Everyone has
drawn this.

**The naive version.** No layers: one `OrderService` class doing validation,
SQL, pricing and email. The demo shows what that costs — you cannot test pricing
without a database, and you cannot read the class in one screen.

Then the second naive version, and it is the one that matters, because it is
what most real "layered" codebases actually are: the layers exist as packages,
and the presentation layer calls the repository directly because it was quicker
that day. The demo shows that single call, and shows that **nothing in the build
objects to it**. That is the whole problem with layering as it is usually
practised: it is a convention, and conventions decay silently.

**The pattern.** Each layer depends only on the one beneath it. Dependencies
point downward and nowhere else. And the rule is enforced by a test, which is
the project's key moment: the demo adds the shortcut call again and the build
goes red with a message naming the offending class.

**The bill.** Layers cost indirection — a field added to a form touches four
layers, and the demo counts them. Pass-through layers that only forward calls
are real and the project should admit they are tedious. And the bottom layer is
still the database: the domain depends on infrastructure, which is exactly what
§65 exists to invert.

### 4.64 MVC — the view that knew too much

**Scenario.** An order summary screen: items, totals, delivery estimate.

**The naive version.** The rendering code computes the totals. The demo then
adds a second output — a plain-text order confirmation email — and the totals
are computed a second time, slightly differently, and the two disagree. A
customer is shown £42.50 on screen and charged £42.49 in the email. That
discrepancy is the project's anchor, because it is a bug a reader can feel
rather than an abstraction.

**The pattern.** The model owns state and rules. The view renders. The
controller turns input into calls on the model. Both outputs read the same
model, and the demo shows the same total in both because there is only one
calculation.

**The bill, and it must be honest.** MVC is the most-argued-about pattern in
this course and the project must say why: nearly everyone who says "MVC" means
something different. Classic Smalltalk MVC has the view observing the model
directly. Web MVC does not — the controller assembles a model for the view, and
there is no observation at all. MVP and MVVM are the same separation with the
arrows moved. The project shows the classic version, then says plainly what a
web framework actually does, because a reader who learns only the textbook
version will be confused by their first Spring controller.

Then the practical costs: controllers that grow until they are the application,
and views that quietly acquire logic because it was one line.

### 4.65 Hexagonal Architecture — the application that does not know it has a database

**Scenario.** Place an order. The core needs to load a product, save an order
and send a confirmation.

**The naive version.** The layered version from §63, honestly described: it
works, and its domain still imports the persistence package. The demo shows the
import, and shows what it costs — you cannot unit-test the domain without a
database, and the demo times a suite that needs one against a suite that does
not.

**The pattern.** The core defines **ports** — interfaces it needs, written in
its own language: `OrderStore`, `PaymentGateway`, `Notifier`. **Adapters** on
the outside implement them. Dependencies point inward, always. The core has no
import of anything outside itself, and the architecture test enforces it.

The demo makes the point twice, in the two directions people forget are
symmetric. On the **driven** side, the database adapter is swapped for an
in-memory one with no change to the core. On the **driving** side, the same core
is driven by a CLI instead of an HTTP handler — also with no change. Hexagonal
is usually taught as being about databases; it is equally about who calls you,
and that is the half most treatments skip.

**The bill.** Interfaces for things with exactly one implementation, which feels
like ceremony and sometimes is. Mapping between domain objects and adapter
representations — the same cost §58 charges. And the question the project must
answer rather than dodge: for an application that will only ever have one
database, is this worth it? The honest answer is often no, and saying so is what
makes the yes credible.

### 4.66 Clean Architecture — which way does the arrow point?

**Scenario.** The same order placement, once more.

**The naive version.** The hexagonal version from §65 — which is good, and the
project says so. Clean Architecture is not a correction of it; it is a
generalisation, and pretending otherwise would be dishonest.

**The pattern.** Concentric layers — entities, use cases, interface adapters,
frameworks — with one rule: **source code dependencies point only inward.**
Entities know nothing. Use cases know entities. Everything else knows them and
is known by nothing.

The project's single most valuable contribution is the **dependency inversion
moment**, and it must be shown in code rather than described. Control flows
outward — the use case needs to save an order, and the database is outside — yet
the dependency points inward, because the interface belongs to the use case and
the database implements it. Control and dependency travel in opposite
directions. That is the whole trick, most readers have never seen it stated
plainly, and the demo shows the arrow flipping while the call still goes where
it always went.

**The forced change is the biggest in the category.** Add a new delivery
mechanism and a new data source at once, then print the files touched: the
entities and use cases are untouched, and the number proves it.

**The wiring is by hand, and that is this project's core scene.** Twenty lines of
constructor calls in a `main` method assemble the whole graph, and watching them
is where dependency inversion stops being a diagram: the `main` method reaches
into the outermost circle for a database class and hands it to a use case that
only knows an interface. An annotation that did this invisibly could not teach
it, so no container appears anywhere in this project.

**Spring's version of the same graph is §67**, a separate project, and this one
links to it in its closing scene without depending on it.

**The bill, and this project must be the most honest in the category.** Clean
Architecture is over-applied, and a CRUD application built this way has more
interfaces than behaviour. The demo shows that: the same trivial feature in both
shapes, with file counts. It costs a lot of files, real indirection, and a team
that must all understand the rule or it decays into folders with impressive
names. The project ends by naming when it pays — long-lived systems, multiple
delivery mechanisms, a domain worth protecting — and when it does not.

### 4.67 Clean Architecture with Spring — the same graph, wired by a container

**What it is.** §66 again, byte-for-byte identical in its entities, use cases and
adapters, with one thing changed: the object graph is assembled by Spring instead
of by a `main` method. Same feature, same architecture tests, same forced change.

**Why it is a project and not a scene.** Because it is the version the reader
will actually be handed at work, and because the comparison only works if both
sides are real. A single scene could show an annotation; a whole project can show
the same acceptance tests passing over a container-assembled graph, the same
architecture test still failing when the dependency rule is broken, and the
startup log listing beans that are exactly the twenty lines §66 wrote by hand.
The lesson is **recognition**: `@Component` is not magic, it is those twenty
lines, and a reader who has seen both stops treating the container as weather.

**The comparison it must make, as output rather than prose.** Put the two
assemblies side by side and count: §66's dependency list is one file you can read
top to bottom; §67's is distributed across annotations and discovered at startup.
One is easier to write, the other is easier to see. The demo makes that concrete
by breaking the graph — remove a bean §66 would have failed to compile without,
and watch §67 start successfully and fail at runtime instead. **Hand-wiring fails
at compile time; container wiring fails at startup.** That single contrast is the
project's most valuable twenty seconds, and it is the honest cost of the
convenience.

**Spring must be explained, not assumed.** The project carries a
`docs/dependencies.md` answering the standing five questions — what Spring is in
plain language, why this project uses it, what to install with the version
pinned, what it costs in concepts and startup magic, and that **§66 teaches Clean
Architecture completely on its own**, so skipping this project loses none of the
architecture. The video says the same aloud before the first annotation appears.

**What this project must not do.** It must not re-teach Clean Architecture, and
it must not become a Spring tutorial. §66 owns the pattern; this project owns one
question — what changes when a container does the assembling — and it should
answer that and stop. Its dependency order is also fixed: **§66 is built and
published first**, always, because this project is only legible to someone who
has seen the hand-wiring.

**The bill.** A framework in the outermost circle, which is where Clean
Architecture says it belongs — and the project should note that this is the
architecture's own prediction coming true: Spring is a detail, the graph did not
change, and that is the point. Against that, a reader now needs to know Spring to
run the project at all, startup is slower, and a wiring mistake surfaces at run
time rather than at compile time.

---

## 5. Relationships to the existing projects

| Project | Depends on | Why |
| --- | --- | --- |
| Layered | Service Layer (§57), Facade (§12) | The application layer is §57; each layer's entry point is a Facade. |
| MVC | Observer (§16), Strategy (§20), Composite (§9) | Classic MVC's view observes the model; views are composite. |
| Hexagonal | Adapter (§10), Strategy (§20), Repository (§56) | Adapters are literally §10; a port is §56 generalised. |
| Clean | Hexagonal (§65), Dependency Injection (§72), DTO (§58) | Same inversion generalised; DI is how the wiring happens; DTOs cross the circles. |
| Clean with Spring | Clean Architecture (§66) | It is §66's graph, assembled by a container. It depends on §66 being built and published first. |

The Dependency Injection link matters for sequencing: **§72 should ideally be
built before §66**, because Clean Architecture's wiring is where DI stops being
an abstraction. If it is not, §66 explains the wiring itself and links forward.

---

## 6. Deliverables per project

Identical to the microservices category — the same committed file set and the
same generators, per [`../../micro-services-design-patterns/docs/ai-build-spec.md`](../../micro-services-design-patterns/docs/ai-build-spec.md).

Four additions specific to this category, and they are what keep it concrete:

- **An architecture test that fails.** A test asserting the dependency rule,
  plus a demonstration of it going red when the rule is broken. Committed, run
  by `./gradlew test`, and shown in the video.
- **A counted forced change.** The change from §2 Rule 2, performed, with the
  files-touched count printed by the demo and quoted in the README.
- **A directory listing in the README**, because in this category the structure
  *is* the content and a reader should see it before reading a word.
- **A "when this is too much" section.** Every project names the application
  size at which its architecture is over-engineering. Without it, four videos in
  a row argue for more structure, which is bad advice.

---

## 7. Video, poster and publishing

Unchanged: 14 to 16 scenes, `Samantha` at 145 wpm, −16 LUFS, a poster that does
not strike out its message, an outro naming no successor, and the required
four-step opening. Target length eleven to thirteen minutes.

**This category has the hardest audio-only problem in the course**, because
architecture is normally taught by pointing at a diagram, and a listener has no
diagram. The rule that follows: narration describes architecture as **rules and
directions in words**, never as a picture. *"The order-placing code names an
interface called OrderStore. The database class implements that interface. So
the database knows about the order-placing code, and the order-placing code does
not know the database exists."* A reader with their eyes shut can hold that. They
cannot hold "as you can see in the diagram", and that phrase is banned outright.

If a scene needs the picture, the scene is rewritten.

---

## 8. Deliberately not included

| Pattern | Why not |
| --- | --- |
| Onion Architecture | Hexagonal with named rings. §65 and §66 already bracket it; a third project would be the same content again. |
| Microkernel / Plugin | A genuine pattern, and a fair candidate for a later addition. Left out because its honest demo needs dynamic loading, which is a classloader lesson wearing an architecture hat. |
| Event-Driven Architecture | Covered across §35, §36 and §46. As an architecture it is a style rather than a structure, and would restate them. |
| Pipe and Filter | Largely Chain of Responsibility (§15) and Decorator (§11) at application scale. |
| Space-Based, Serverless, Modular Monolith | Deployment and organisational shapes. They belong to the platform category's territory or to no category at all. |
| MVP and MVVM | Variants of §64 with the arrows moved, covered in a scene of it. Teaching them properly needs a UI toolkit, which this course does not have. |

A fifth *pattern* requires editing this section first. This category should stay
small deliberately: four architectures that differ meaningfully beats seven that
blur.

---

## 9. Conformance

Every item from the microservices category's §9 applies, plus ten:

- [ ] **The project implements the same order-placing feature** as the other
      three, so the four can be diffed against each other.
- [ ] **An architecture test exists, runs in `./gradlew test`, and is shown
      failing** when the dependency rule is deliberately broken.
- [ ] **The forced change is performed and its cost counted** in files touched
      and lines changed, from real output.
- [ ] The README opens with the **directory listing**.
- [ ] The explainer has a **"when this is too much"** section naming the scale
      at which the architecture is over-engineering, and the video says it
      aloud.
- [ ] **No narration line refers to a diagram**, and the video has been listened
      to with the screen ignored.
- [ ] The project says explicitly **which single step** it takes beyond the
      previous architecture, rather than presenting itself as unrelated.
- [ ] The naive version is treated fairly — for §66 that means saying plainly
      that the hexagonal version it replaces was already good.
- [ ] **Where a version of an architecture is built with a framework, it is its
      own project** — its own README, documents, poster, thumbnail and video —
      naming the framework-free project it pairs with in its first paragraph and
      in its opening scene, while that project links forward to it.
- [ ] **Every heavy dependency has a `docs/dependencies.md`** saying what it is,
      why it is here, what to install with the version pinned, what it costs, and
      that skipping it loses none of the architecture — and the video says so
      aloud before the dependency first appears.
