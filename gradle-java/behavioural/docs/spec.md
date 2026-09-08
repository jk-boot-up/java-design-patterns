# Behavioural Patterns — Category Specification

The standard the eleven behavioural projects under `gradle-java/behavioural/`
are built to: which pattern gets which scenario in the store, why that
scenario is the right one, and what each project has to deliver.

This document is the *what*. The companion
[`implementation-plan.md`](implementation-plan.md) is the *how* — the ordered
plan for building the eleven.

It **inherits** the repository-wide
[`video-and-publishing-spec.md`](../../docs/video-and-publishing-spec.md).
Everything there — the narration rate, the audio pipeline, the poster rules,
the publishing document, the conformance checklist — applies here unchanged
and is not repeated. This document adds only what is specific to the
behavioural category. Where the two appear to disagree, the repository-wide
document wins.

---

## 1. Scope

Eleven projects, one per Gang of Four behavioural pattern, each a
self-contained Gradle Java 21 project with sources, JUnit 5 tests, `docs/`,
`video/`, and a top-level `README.md` — the same shape as the fourteen
creational and structural projects that already exist.

| # | Pattern | Directory |
| --- | --- | --- |
| 1 | Strategy | `strategy-pattern` |
| 2 | Observer | `observer-pattern` |
| 3 | Command | `command-pattern` |
| 4 | Template Method | `template-method-pattern` |
| 5 | State | `state-pattern` |
| 6 | Chain of Responsibility | `chain-of-responsibility-pattern` |
| 7 | Iterator | `iterator-pattern` |
| 8 | Mediator | `mediator-pattern` |
| 9 | Memento | `memento-pattern` |
| 10 | Visitor | `visitor-pattern` |
| 11 | Interpreter | `interpreter-pattern` |

The order is the learning order, and the end screen of each video points at
the next. It is not the book's order. It runs from the patterns a working
developer meets soonest and can apply immediately (Strategy, Observer) toward
the ones that need the most scaffolding before they make sense (Visitor,
Interpreter).

Two of them lean on projects that already exist and are placed to take
advantage of that: **Template Method** after the learner has met Factory
Method, and **Visitor** after Composite.

---

## 2. What makes this category different

Creational patterns are about *making* objects and structural patterns about
*arranging* them. Behavioural patterns are about how objects **decide** and
**talk to each other at runtime**, and that changes what a good teaching
example has to show.

The consequence for these projects: **a static class diagram is not enough.**
For most of these eleven, the interesting content is a sequence — what happens
in what order, and what the object graph looks like at each step. So:

- The `uml-diagram.md` sequence diagram carries more weight here than in the
  other two categories, and must show a real interaction, not a summary.
- `animation.html` must step through *runtime* state, not structure.
- The demo's printed output is the primary evidence. It has to make the
  behaviour visible — which handler took the request, which observers fired
  and in what order, which state refused the transition. A demo that prints
  only a final answer has failed to teach a behavioural pattern.

---

## 3. The scenarios

The repository-wide spec requires every project to teach through the online
store, and requires each project to pick a scenario where the pattern is
**genuinely the right answer** — a contrived e-commerce wrapper around a
non-e-commerce idea is worse than a clean example, because the honest "when
not to use this" section then has nothing to stand on.

Each subsection below therefore fixes four things: the scenario, why the
pattern genuinely fits it, the naive alternative the project must show
failing, and the honest cost the project must admit to.

### 3.1 Strategy — shipping cost calculation

Checkout must price delivery, and the rule varies: a flat rate, a
weight-banded rate, a distance-based rate, and free shipping above a
threshold. Merchandising changes which rule is live, per campaign, without a
deploy.

**Why it fits.** The rules are genuine peers — same inputs, same output,
different algorithm — and which one applies is decided per order at runtime.
That is Strategy's exact shape.

**Naive alternative.** One `calculateShipping` method with a `switch` over a
`ShippingMethod` enum, growing a branch per rule, with all four rules' details
tangled in one method that nothing can test in isolation.

**Honest cost.** Four small classes instead of one method is more files, and
for two rules that never change it would be over-engineering. The project says
so.

### 3.2 Observer — order status changes

When an order moves to `SHIPPED`, several unrelated things must happen:
inventory releases the reservation, the customer gets an email, analytics
records the event, and the warehouse feed is updated. The list grows, and the
order service should not grow with it.

**Why it fits.** One state change, many independent reactions, and the
publisher genuinely has no business knowing who is listening.

**Naive alternative.** `OrderService.markShipped()` calling each of the four
services directly, so adding a fifth listener means editing the order service
and re-testing it.

**Honest cost.** The call graph becomes invisible: reading `markShipped()` no
longer tells you what happens. The project must show this, and must cover
listener exceptions and the fact that notification order is not something
observers may rely on.

### 3.3 Command — cart operations with undo

Cart edits — add item, remove item, change quantity, apply a coupon — are
turned into objects, so the cart can offer undo, and so the same objects can
be logged and replayed.

**Why it fits.** Undo requires the request to be reified; there is no way to
undo a method call that has already returned. A history of executed commands
is the natural representation.

**Naive alternative.** Mutating the cart directly, plus a hand-rolled `Stack`
of ad-hoc "what I changed" tuples that has to be extended for every new kind
of edit.

**Honest cost.** Every operation becomes a class, and every command must
correctly implement its own inverse — which is where the bugs live. The
project must show a command whose undo is not trivial.

### 3.4 Template Method — the fulfilment workflow

Fulfilling an order always runs the same sequence: validate, reserve stock,
charge, pack, dispatch, notify. *How* several of those steps work depends on
the fulfilment route — the store's own warehouse, a third-party marketplace
seller, or a digital download that has no stock and nothing to pack.

**Why it fits.** The sequence is genuinely invariant and must not be
overridable; several individual steps genuinely differ; and some steps have a
sensible default that only one route overrides — which is what hooks are for.

**Naive alternative.** Three fulfilment classes that each write the whole
sequence out, already subtly divergent in the order of the last two steps.

**Honest cost.** Inheritance. The base class and its subclasses are welded
together, and the project must compare this directly with composing
strategies, which is usually the better modern default.

> **Required distinction.** The repository already has a Factory Method
> project, also described as "a workflow with a hole in it", and a learner
> will meet them close together. Both projects must draw the line explicitly:
> Factory Method's hole is *which object to create* — exactly one, returning a
> product. Template Method's holes are *how several steps behave*, return
> nothing in particular, and include optional hooks. Factory Method is
> Template Method narrowed to object creation.

### 3.5 State — the order lifecycle

An order moves `PLACED → PAID → PACKED → SHIPPED → DELIVERED`, and may be
cancelled — but only up to a point. What `cancel()`, `ship()` and `refund()`
do, and whether they are allowed at all, depends entirely on where the order
currently is.

**Why it fits.** This is a real state machine with real illegal transitions,
and the behaviour genuinely varies by state rather than merely the data.

**Naive alternative.** An `OrderStatus` enum field and a nested `if`/`else`
over it at the top of every method — the same chain repeated in `cancel()`,
`ship()` and `refund()`, kept in agreement by hand.

**Honest cost.** A class per state, and the transition rules end up
distributed across them rather than visible in one table. The project must be
honest that for a small, stable machine an enum with a permitted-transitions
map is often clearer.

> **Required distinction.** State and Strategy have the same class diagram.
> The difference is intent and control: a Strategy is chosen by the caller and
> does not change itself; a State is entered as a consequence of what the
> object did, and states hand control to one another. Both projects must say
> this.

### 3.6 Chain of Responsibility — checkout screening

Before an order is accepted it passes a series of independent checks:
the address is deliverable, the items are in stock, the fraud score is under
threshold, the payment is within the customer's limit. Any check can reject
outright; otherwise the request moves on. Which checks run, and in what order,
is configuration.

**Why it fits.** The checks are genuinely independent, the order genuinely
matters, and the set is genuinely assembled at runtime rather than compiled in.

**Naive alternative.** One `validate()` method running all four in sequence
with early returns, where reordering means editing the method and testing one
check means constructing the state for all of the preceding ones.

**Honest cost.** A request can fall off the end of the chain unhandled, and
debugging "which link rejected this?" is harder than reading four sequential
`if`s. The project must show the unhandled case being dealt with deliberately.

### 3.7 Iterator — paging the catalog

A catalog search matches forty thousand products, and the backend returns them
a page at a time. Calling code wants to write a `for` loop over *products* and
should never see a page, a cursor, or a fetch.

**Why it fits.** The traversal is genuinely non-trivial — it is lazy, it does
I/O partway through, and the total is not known up front — which is precisely
the case where implementing `Iterable` earns its keep.

**Naive alternative.** Every caller looping over pages itself, tracking the
cursor and the end-of-results condition, with the off-by-one on the last page
duplicated everywhere.

**Honest cost.** This is the one pattern in the category that Java already
gives you. The project must be explicit that you should almost never write an
iterator over a plain collection, must show `Iterable` and the enhanced `for`
loop being satisfied, and must mention `Stream` and `Spliterator` as the
modern alternatives.

### 3.8 Mediator — the checkout page

The checkout screen has interacting parts: a cart summary, a country
selector, a shipping-method picker, a coupon field, a payment panel, and an
order total. Changing the country changes which shipping methods are
available, which changes the total, which can invalidate a coupon that had a
minimum spend, which changes the total again.

**Why it fits.** This is genuinely many-to-many. Six components wired directly
to each other is the class of problem the pattern exists for, and the
cascading update is a real interaction rather than an invented one.

**Naive alternative.** Each component holding references to the others and
calling them directly — a graph nothing can be tested or reused apart from.

**Honest cost.** The mediator becomes the place all the complexity moves to,
and left unchecked it grows into a god object. The project must name that
failure mode and show where the line is.

> **Required distinction.** Observer and Mediator both decouple
> communication. Observer is one-to-many broadcast where the publisher does
> not care who listens; Mediator is many-to-many coordination where something
> genuinely has to know the rules of the interaction. The Mediator project
> must reference the Observer project directly.

### 3.9 Memento — restoring a saved cart

A customer bulk-edits a large cart — clears it, applies a promotion, changes
quantities — and wants to get back to how it was. The cart takes a snapshot
before each risky edit and can be restored from one, without exposing its
internals to whatever is holding the snapshot.

**Why it fits.** The saved state is genuinely private to the cart, and the
caretaker genuinely must not be able to read or forge it. That encapsulation
constraint is what separates a memento from "just keep a copy".

**Naive alternative.** Exposing the cart's internal item list so the caller
can copy it — which both breaks encapsulation and hands out a reference that
can mutate the live cart.

**Honest cost.** Snapshots are expensive for a large cart, and a naive
implementation keeps a full copy per edit. The project must address what is
copied and when snapshots are discarded.

> **Required distinction.** Command and Memento both provide undo, and this
> project sits two after Command deliberately. Command stores the *operation*
> and reverses it; Memento stores the *state* and restores it. Commands are
> cheap and compose; mementos are simple but heavy. The project must say when
> each is the right choice.

### 3.10 Visitor — reporting over the catalog tree

The catalog is the same tree of categories and products the Composite project
builds. The business keeps asking for new reports over it: total inventory
value, a count by category, a CSV export, a compliance audit of restricted
items. Each is a new operation over a structure that does not change.

**Why it fits.** The structure is genuinely stable and the operations
genuinely keep coming, which is the one condition under which Visitor pays
for itself.

**Naive alternative.** A new method on `CatalogComponent` for every report —
so a reporting requirement edits the domain model, and every node type gains a
method about CSV formatting.

**Honest cost.** The trade runs the other way for node types: adding a new
kind of catalog node breaks *every* visitor. Visitor is only correct when you
are confident the structure is settled, and the project must state that as
plainly as it states the benefit. Double dispatch is also genuinely awkward to
read, and the project must not pretend otherwise.

> **Required dependency.** This project reuses the Composite project's
> catalog domain — the same `Category` and `Product` shape and the same demo
> tree — so a learner arrives already understanding the structure and only has
> to absorb the traversal. It must link back to it explicitly.

### 3.11 Interpreter — promotion rules

Marketing wants to define promotion eligibility without a deploy:
`cart total over 100 AND country is UK AND NOT already discounted`. The rule
is parsed into an expression tree of terminal and non-terminal nodes and
evaluated against a cart.

**Why it fits.** A small, genuinely recursive grammar with a real evaluation
context.

**Naive alternative.** A growing set of hard-coded eligibility methods, one
per campaign, each requiring a release.

**Honest cost — and this project must lead with it.** Interpreter is the least
broadly useful pattern in the book. It does not scale past a small grammar,
hand-writing a parser is more work than it looks, and in practice you would
reach for a parser generator, a rules engine, or an embedded scripting
language. It is included because it is in the book, because the expression
tree is genuinely instructive, and because *knowing when not to reach for it*
is the actual lesson. Being last in the order is deliberate.

---

## 4. Relationships to the existing projects

Behavioural patterns are the category where learners most often confuse one
pattern for another, because several share a class diagram and differ only in
intent. The pairs below are the ones that actually cause trouble, and each is
assigned to a project that must address it head-on in its
`{pattern}-pattern-explained.md`:

| Confusion | Addressed in |
| --- | --- |
| Template Method vs Factory Method | Template Method (§3.4) |
| State vs Strategy | State (§3.5) |
| Observer vs Mediator | Mediator (§3.8) |
| Command vs Memento, for undo | Memento (§3.9) |
| Visitor vs putting the method on the Composite | Visitor (§3.10) |
| Strategy vs Simple Factory | Strategy — choosing *behaviour* versus choosing *which object to construct* |
| Chain of Responsibility vs Decorator | Chain of Responsibility — both are linked wrappers, but a decorator always delegates onward and adds; a handler may stop the chain |

A cross-reference is not a paragraph saying the two are "similar but
different". It must state the distinguishing question a developer can actually
ask themselves at the point of choosing.

---

## 5. Deliverables per project

Exactly as the repository-wide spec §7 requires, with no additions and no
omissions: `docs/` (prerequisites, problem statement, the explainer, class
diagram, UML sequence diagram, `animation.html`, `session.md`, `youtube.md`,
`thumbnail.png`, and a generated `spec.md` / `spec.html`), `video/` (scenes,
slides, subtitles, build script, `narration.md`, `README.md`), and a top-level
`README.md` quoting the real `./gradlew run` output.

Two category-specific requirements on top:

1. **The demo must make the behaviour visible**, per §2. Printed output that
   shows only a result, and not the interaction that produced it, does not
   satisfy this.
2. **Tests must cover the interaction, not just the outcome.** For these
   patterns the outcome is often reachable by an implementation that has not
   applied the pattern at all: a State project passes an "order ships" test
   whether or not there are state objects. So the tests must also assert the
   things only the pattern gives you — that an illegal transition is refused,
   that an observer added later is notified, that a handler later in the chain
   is not consulted after an earlier one rejects, that undo restores exactly
   the prior state. Nine tests is the working floor, matching the leanest of
   the existing projects.

---

## 6. Video, poster and publishing

Inherited wholesale from the repository-wide spec §§3–6 and §8: 145 wpm,
Samantha, the two-pass `loudnorm`, one AAC encode at the mux, the continuity
self-check, no strikethrough on the poster, and the seven-section
`docs/youtube.md`. The build scripts are generated from
`creational/abstract-factory-pattern`'s, as the existing thirteen are.

The one category-specific point: several of these patterns are about a
*sequence*, and a slide showing a class diagram cannot carry that. Scenes for
Observer, Chain of Responsibility, State, Mediator and Command must include
at least one slide that walks the interaction step by step, in the order it
happens, rather than presenting the finished structure and describing it.

Titles follow the existing series convention — the pattern name, then a dash,
then the worked scenario:

| Pattern | Working title |
| --- | --- |
| Strategy | Strategy Pattern in Java - Shipping Rules |
| Observer | Observer Pattern in Java - Order Status Events |
| Command | Command Pattern in Java - Undoable Cart Edits |
| Template Method | Template Method in Java - The Fulfilment Workflow |
| State | State Pattern in Java - The Order Lifecycle |
| Chain of Responsibility | Chain of Responsibility - Checkout Screening |
| Iterator | Iterator Pattern in Java - Paging the Catalog |
| Mediator | Mediator Pattern in Java - The Checkout Page |
| Memento | Memento Pattern in Java - Restoring a Saved Cart |
| Visitor | Visitor Pattern in Java - Catalog Reports |
| Interpreter | Interpreter Pattern in Java - Promotion Rules |

Each is under the 60-character limit. These are working titles and may be
revised at publication.

---

## 7. Conformance

A behavioural project is compliant when it passes **every item of the
repository-wide checklist** (`video-and-publishing-spec.md` §9) plus these
four:

- [ ] The scenario is the one this document assigns to the pattern, and the
      "when not to use this" section states the honest cost named here.
- [ ] The demo output makes the interaction visible, not just the result.
- [ ] Tests assert the behaviour only the pattern provides, per §5.2, and
      there are at least nine of them.
- [ ] The cross-reference this document assigns to the project (§4) is
      present, and states a question a developer can act on rather than
      observing that two patterns resemble each other.
