# Foundational Patterns — Category Specification

The ninth category. Five projects, numbered 68 to 72 — the patterns that are
taught alongside the Gang of Four without being in it, and that every Java
codebase uses daily.

This document fixes what each project is before any of it is written. It is the
contract; [`implementation-plan.md`](implementation-plan.md) is the schedule.

---

## 1. Scope

Five patterns, in learning order:

| # | Project | One line |
| --- | --- | --- |
| 68 | `null-object-pattern` | The discount that is not there |
| 69 | `object-pool-pattern` | Expensive to make, cheap to borrow |
| 70 | `registry-pattern` | The well-known place everything is kept |
| 71 | `service-locator-pattern` | Ask a middleman for what you need |
| 72 | `dependency-injection-pattern` | Stop asking; be given |

These are often called loose ends, and this category rejects that framing. They
share a subject:

> **How does an object get hold of another object — and what happens when there
> isn't one?**

Null Object answers the second question. Object Pool answers it when creating
one is expensive. The last three are one argument in three moves: Registry is a
well-known place to put things, Service Locator is a middleman you ask, and
Dependency Injection is what happens when you stop asking altogether. Taught in
that order they are a single story with a conclusion, and the conclusion is
worth arriving at rather than being handed.

---

## 2. Why this category exists

Two reasons, and the second is the important one.

**They are ubiquitous and rarely taught.** Dependency Injection is the mechanism
behind every Spring application, and most developers meet it as an annotation
rather than as an idea. Null Object removes more null checks than any other
technique available. Object Pool is what a connection pool is. A course that
teaches all twenty-three Gang of Four patterns and not these has left out the
ones the reader will use this week.

**Three of them exist mainly to be argued about, and that argument is the
lesson.** Service Locator is widely considered an anti-pattern — Fowler weighed
it against Dependency Injection and most of the industry went the other way.
Registry is a shared global by another name. Object Pool is usually the wrong
answer on a modern JVM, where allocation is cheap.

A course that teaches those three as straightforwardly good is teaching
something false. A course that skips them leaves a reader unable to recognise
them in the code they maintain. So:

> **This category teaches contested patterns honestly: what the pattern is, why
> it was reasonable, what replaced it, and how to recognise it in code you did
> not write.**

That makes it the category where "the bill" — already required everywhere in
this course — carries the most weight. For §69, §70 and §71 the bill is close to
the whole point.

---

## 3. The store, continued

Same online shop. The running example across the five is small and concrete: a
checkout needs a **discount policy**, a **payment gateway** and a **notifier**,
and it has to get hold of all three.

Null Object is the customer with no discount. Object Pool is the payment
gateway's expensive connection. Registry, Service Locator and Dependency
Injection are three answers to the same question about the same three
collaborators — which is what lets the last three projects be compared directly
rather than described separately.

---

## 4. The five scenarios

### 4.68 Null Object — the discount that is not there

**Scenario.** Most customers have no discount. Some have a loyalty discount, a
few a staff discount.

**The naive version.** `getDiscount()` returns `null`, and the caller checks.
The demo shows the check spreading — five call sites, then eight — and then
shows the one that was missed, with a real `NullPointerException` at checkout.
It also shows the subtler cost: `if (discount != null)` appears so often that a
reader stops seeing it, and the missing check hides in plain sight.

**The pattern.** A `NoDiscount` that implements the same interface and does
nothing — returns the price unchanged. `getDiscount()` never returns null. The
demo deletes every null check in one diff and the behaviour is identical.

**The bill, and it is the one most treatments omit.** A null object **hides
errors**. "No discount" and "the discount service was down" now look the same to
the caller, and the demo shows a failed lookup silently becoming a full-price
order that nobody notices. That is a worse bug than the exception it replaced,
because it is quiet.

So the project must draw the line clearly: a null object is right when absence is
a **legitimate domain state**, and wrong when absence means **something went
wrong**. It then shows the two modern alternatives fairly — `Optional`, which
makes absence explicit at the type level and is often the better answer in Java,
and an explicit failure. A reader should leave able to choose, not converted.

### 4.69 Object Pool — expensive to make, cheap to borrow

**Scenario.** The payment gateway connection takes 200ms to establish.

**The naive version.** A new connection per payment. The demo prints the timings
and the cost is obvious and real.

**The pattern.** A pool of connections, borrowed and returned. The demo prints
the difference, and it is large.

**The bill, which here is larger than the benefit in most cases and must be
stated up front.** Pooling is one of the most over-applied ideas in Java, and
the project's honesty is its value:

- **On a modern JVM, allocation is cheap.** Object pools for ordinary objects
  are almost always a pessimisation, and the demo shows pooling a small object
  being *slower* than allocating one, because the pool adds synchronisation and
  defeats the generational garbage collector's cheapest path.
- **A returned object carries its old state.** The demo shows a connection
  returned dirty and the next borrower seeing the previous customer's data —
  which is a security bug, not a performance one, and it is the failure that
  actually happens in the field.
- **A leaked object is never returned**, and the demo exhausts the pool and
  shows the application hang, which is worse than a slow start.
- **Sizing is a guess**, and both directions are shown.

**The conclusion the project must reach.** Pool things that are expensive
*outside* the JVM — connections, threads, native handles — and nothing else.
That is why connection pools and thread pools exist and general object pools do
not. The project links to Thread Pool (§47) as the pattern's one
unambiguously correct application.

### 4.70 Registry — the well-known place

**Scenario.** Several parts of the checkout need the same configured payment
gateway.

**The naive version.** Pass it down through six constructors, four of which do
not use it and exist only to forward it. The demo shows those four, and this
naive version deserves genuine sympathy: constructor-passing through deep stacks
is real friction and pretending otherwise is dishonest.

**The pattern.** A well-known object others can find things in. `Registry.get(
PaymentGateway.class)`. The demo shows the six constructors collapsing and the
friction disappearing.

**The bill, and it arrives fast.** A registry is a global variable with better
manners, and it brings everything that implies. Dependencies become **invisible**
— the demo shows a class whose constructor takes nothing and which cannot run
without three things being registered first, and nothing in its signature says
so. Tests must set up global state and leak it into each other, and the demo
shows one test failing *because of the order the tests ran in*, which is the
symptom teams meet first. Thread safety becomes a question. And "what is in the
registry at this moment" is not answerable by reading any one file.

The project ends by naming the one place it is genuinely the best answer — a
small number of truly application-wide things, established at startup and never
changed — and §71 as where it leads.

### 4.71 Service Locator — asking a middleman

**Scenario.** The same three collaborators, with the registry's problems now
felt.

**The pattern.** A locator that knows how to *find or create* what you ask for,
rather than a bag of things someone remembered to put in. It can create lazily,
manage lifetimes, and be swapped for a test implementation — the demo shows that
swap, which is the genuine advance over §70.

**The bill, and this project's job is to make the case against itself
honestly.** Service Locator is widely regarded as an anti-pattern, and the
project must show why rather than assert it:

- **Dependencies are still hidden.** `new CheckoutService()` compiles fine and
  fails at runtime. The demo shows the compiler saying nothing while a required
  collaborator is missing — the failure arrives in production, not in the build.
- **Every class now depends on the locator**, which is coupling to
  infrastructure everywhere, in code that is otherwise pure domain logic.
- **Testing needs the locator configured**, so a unit test is never quite a unit
  test.
- **A missing registration is a runtime error**, and the demo produces it.

The project is fair about where it is still used and why — plugin systems where
what is available is genuinely not known until runtime, and Java's own
`ServiceLoader`, which is this pattern in the standard library and is not
anybody's mistake.

**The moment it hands over.** The whole difficulty is the word *ask*. The class
asks, so nobody outside it knows what it needs. §72 removes the asking.

### 4.72 Dependency Injection — stop asking; be given

**Scenario.** The same checkout, the same three collaborators, one more time.

**The pattern.** The class declares what it needs in its constructor and is
given it. It never looks anything up. The demo prints the constructor and the
point makes itself out loud: **the signature is the dependency list**, complete
and checked by the compiler.

Then the three forms — constructor, setter, field — with a clear recommendation
rather than a survey. Constructor injection, because it makes dependencies
mandatory and visible and the object valid the moment it exists. Setter
injection for genuinely optional things. Field injection discouraged, with the
reason shown: the object can be constructed in an invalid state, and it cannot
be built in a test without a framework.

And the wiring is shown by hand first — a `main` method that constructs
everything in order — so the reader sees that **a container is an optimisation of
something they can write themselves**, roughly twenty lines for this
application. That demystification is the project's most valuable minute.

**The bill.** The wiring has to live somewhere, and by hand it grows with the
application. A container solves that and costs you magic: the demo shows a
container failing to start with an error about a bean it could not construct,
which is the modern equivalent of §71's missing registration — better, because
it fails at startup rather than at the first request, but still not at compile
time. Constructors grow long, and the project says plainly that a class needing
seven collaborators has a design problem that no injection style fixes.
Circular dependencies become a startup failure the demo produces on purpose.

**Where this lands.** Dependency Injection is not Spring. The demo has proved
that by doing it in plain Java, and Tier 2 shows the same graph wired by a
container so the reader recognises what the annotations replaced.

**The capstone role.** This project closes the three-part argument: Registry put
things in a known place; Service Locator made a middleman that could find them;
Dependency Injection stopped the class asking at all. It must state that
progression explicitly, because arriving at the conclusion is what makes it
stick.

---

## 5. Relationships to the existing projects

| Project | Depends on | Why |
| --- | --- | --- |
| Null Object | Strategy (§20), Special Case (PoEAA) | It is a Strategy that does nothing; Fowler's Special Case is its generalisation. |
| Object Pool | Thread Pool (§47), Flyweight (§13), Singleton (§4) | §47 is the correct application; Flyweight shares instead of recycling — the contrast matters. |
| Registry | Singleton (§4) | A registry is usually a singleton holding several singletons, and inherits every one of §4's problems. |
| Service Locator | Factory Method (§3), Abstract Factory (§1) | A locator is a factory that decides what to return at runtime. |
| Dependency Injection | Clean Architecture (§66), Hexagonal (§65), Builder (§2) | It is how §65 and §66's wiring happens; assembling a graph is close to §2. |

The link to §66 runs both ways and matters for scheduling: **building §72 before
§66 is preferable**, so Clean Architecture can link to it rather than explaining
injection itself.

---

## 6. Deliverables per project

Identical to the microservices category — the same committed file set and the
same generators, per [`../../micro-services-design-patterns/docs/ai-build-spec.md`](../../micro-services-design-patterns/docs/ai-build-spec.md).

Three additions specific to this category:

- **A "how to recognise this in code you did not write" section.** For the three
  contested patterns especially, a reader's most likely encounter is
  maintenance, not greenfield. What does it look like, what breaks first, and
  what to do about it.
- **A verdict, stated plainly.** Every project ends with a clear position: use
  this, use it in these narrow cases, or prefer this other thing. Hedging is
  what makes contested patterns confusing, and this category exists partly to
  end that confusion.
- **A `real/` Tier 2 for §72 only**, showing the same object graph wired by a
  container. Excluded from `./gradlew test`, pinned, one command to run.

---

## 7. Video, poster and publishing

Unchanged: 14 to 16 scenes, `Samantha` at 145 wpm, −16 LUFS, a poster that does
not strike out its message, an outro naming no successor, and the required
four-step opening. Target length eleven to thirteen minutes.

Two of these — Service Locator and Object Pool — have videos that largely argue
against their own subject. Their titles and posters must be straight about that
rather than clickbait: a poster promising a technique and a video advising
against it is a bait-and-switch, and the audience will say so.

---

## 8. Deliberately not included

| Pattern | Why not |
| --- | --- |
| Special Case (PoEAA) | Null Object generalised, covered in a scene of §68. |
| Multiton | A registry keyed by name, covered in §70. |
| Lazy Initialisation | An idiom rather than a pattern. It appears where it matters, in Lazy Load (§55) and in §71's lazy creation. |
| Value Object, Money | Base patterns worth knowing, but there is no naive-version-fails-then-pattern story to build a project around. |
| Immutable Object | Absorbed by Java records and taught throughout the course by example. |
| Marker Interface, Type Object | Technique and idiom respectively, with too little design content for a project. |

A sixth project requires editing this section first.

---

## 9. Conformance

Every item from the microservices category's §9 applies, plus six:

- [ ] **The project ends with a plain verdict** — use this, use it narrowly, or
      prefer the alternative — and the video says it aloud.
- [ ] The explainer has its **"how to recognise this in code you did not write"**
      section.
- [ ] **The contested patterns argue against themselves with evidence, not
      assertion.** §69's slower-than-allocation demo, §70's order-dependent test
      failure and §71's compiler saying nothing are all runnable.
- [ ] **The naive version is treated fairly.** Constructor-passing through six
      levels really is friction; saying so is what makes §70's bill credible.
- [ ] The three-part progression — Registry, Service Locator, Dependency
      Injection — is stated explicitly in §72.
- [ ] §72 shows the wiring by hand before showing any container, and says how
      many lines it took.
