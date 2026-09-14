# Microservices Patterns — Category Specification

The standard the twelve microservices projects under
`gradle-java/micro-services-design-patterns/` are built to: which pattern gets
which scenario in the store, why that scenario is the right one, and what each
project has to deliver.

This document is the *what*. The companion
[`implementation-plan.md`](implementation-plan.md) is the *how* — the ordered
plan for building the twelve.

It **inherits** the repository-wide
[`video-and-publishing-spec.md`](../../docs/video-and-publishing-spec.md).
Everything there — the narration rate, the audio pipeline, the poster rules,
the publishing document, the conformance checklist — applies here unchanged
and is not repeated. This document adds only what is specific to the
microservices category. Where the two appear to disagree, the repository-wide
document wins.

---

## 1. Scope

Twelve projects, each a self-contained Gradle Java 21 project with sources,
JUnit 5 tests, `docs/`, `video/`, and a top-level `README.md` — the same shape
as the twenty-five Gang of Four projects that already exist.

| # | Pattern | Directory |
| --- | --- | --- |
| 1 | API Gateway | `api-gateway-pattern` |
| 2 | Service Registry and Discovery | `service-discovery-pattern` |
| 3 | Client-Side Load Balancing | `load-balancing-pattern` |
| 4 | Retry with Backoff | `retry-pattern` |
| 5 | Circuit Breaker | `circuit-breaker-pattern` |
| 6 | Bulkhead | `bulkhead-pattern` |
| 7 | Database per Service | `database-per-service-pattern` |
| 8 | API Composition | `api-composition-pattern` |
| 9 | CQRS | `cqrs-pattern` |
| 10 | Saga | `saga-pattern` |
| 11 | Transactional Outbox | `transactional-outbox-pattern` |
| 12 | Idempotent Consumer | `idempotent-consumer-pattern` |

The order is the learning order, not a catalogue order. It runs in three
movements:

- **1–3, the shape of a call.** How a request reaches a service at all, before
  anything is allowed to go wrong.
- **4–6, what to do when a call fails.** Failure is introduced only once the
  reader knows what is failing.
- **7–12, the data problem.** The genuinely hard part, and the reason most
  microservice architectures get into trouble: state split across services that
  cannot share a transaction.

Two projects lean on the Gang of Four projects that already exist and are
placed to take advantage of that: **API Gateway** immediately invites the
comparison with Facade, and **Saga** is far easier to teach to somebody who has
already met Command's undo.

Unlike the behavioural category, the video end screens do **not** point at the
next project. No video in this repository names its successor, because YouTube
publishing order is not the build order and a rendered video cannot be
corrected without re-uploading it.

---

## 2. What makes this category different

The other twenty-five patterns are about the arrangement of objects inside one
program. These twelve are about what happens when the program is not one
program: several services, each with its own data, talking over a network that
is slow, and that intermittently does not work.

That difference produces the single largest design decision in this category,
and it has to be stated in every project rather than assumed.

### 2.1 There is no network, and that is deliberate

**Every project runs in one JVM, with `./gradlew run`, and starts nothing.** No
Docker, no Spring Boot, no Kafka, no database, no HTTP port, no cloud account.
A "service" here is a plain Java class behind an interface, and a "remote call"
is a method call through a small simulated transport that can be told to be
slow, to fail, or to fail intermittently.

This is a teaching decision with a cost, and the cost is stated in each
project's explainer rather than buried:

- **What you do learn** is the pattern's shape — what objects exist, what each
  one decides, what state it keeps, and what the failure path looks like in
  code. That shape is identical whether the call underneath is a method call or
  an HTTP request, which is exactly why it can be taught this way.
- **What you do not learn** is operating a distributed system: deployment,
  service meshes, partial network partitions, clock skew, real broker
  semantics, or capacity planning. A reader who finishes all twelve knows what a
  circuit breaker *is* and could write one; they have not run one in production.

Every project must carry that limitation in its explainer, in those terms. A
project that lets a reader believe they have built a microservice has failed,
regardless of how correct its code is.

### 2.2 Failure is the subject, so failure must be deterministic

Half of these patterns exist because remote calls fail. Their tests must
therefore *cause* failure, and cause it reproducibly:

- **No `Thread.sleep` in tests, ever.** Time is an injected `Clock`; a timeout
  or a backoff window is tested by advancing a fake clock, not by waiting.
  A test suite that takes eleven seconds to prove a retry policy is a test suite
  people delete.
- **Failure is injected, not random.** A simulated service is configured with a
  script — "fail twice, then succeed" — so the assertion is about the pattern's
  behaviour, not about luck. Randomised jitter is drawn from a seeded source so
  the test can assert the exact sequence.
- **Concurrency, where a pattern genuinely needs it** (Bulkhead is the only
  one), uses a fixed pool and a latch, never a sleep-and-hope.

### 2.3 The demo has to show a timeline

As in the behavioural category, a static class diagram cannot carry these
patterns; what matters is a sequence, and specifically a sequence in which
something goes wrong. So:

- The demo prints a **call log with elapsed simulated time** — which service was
  called, at what millisecond, whether it succeeded, and what the pattern did
  about it. Printing only the final answer does not satisfy this.
- `animation.html` steps through that timeline, not the structure.
- `uml-diagram.md` shows a real interaction including its failure branch.

### 2.4 Each project is self-contained, including its harness

The small simulation harness — the fake clock, the scripted flaky service, the
call log — is **copied into each project**, not extracted into a shared module.
This is the same rule the other twenty-five follow, and it is deliberate: a
learner must be able to open one directory, read every class it uses, and run
it, without a shared library sitting between them and the pattern. Duplication
across projects is the price, and it is the right price here.

The harness is small on purpose. If it grows past roughly three classes in any
project, the pattern is being smothered by its scaffolding.

### 2.5 Every explanation must work with the listener's eyes closed

Most people who meet this material will not be reading the code while they meet
it. They will be listening — on a commute, while cooking, with the phone in a
pocket. The material is written for them first, and for the reader looking at the
screen second.

That is a hard constraint, not a preference, and it has four consequences that
apply to every README, every explainer and above all every line of narration in
this category:

1. **Nothing may depend on a visual.** No "as you can see here", no "the diagram
   on the left", no "this class". Name the actors out loud, say what each one
   decides, and describe the flow in the order it happens. If a sentence stops
   making sense when the screen is off, it is rewritten.
2. **Plain words before technical words.** Every project's explainer opens with a
   paragraph a complete beginner could follow, using no term the pattern's own
   name does not force. Words like *idempotent*, *eventually consistent* and
   *compensating transaction* are not banned — they are what the reader came for
   — but each one is defined in ordinary language at first use, in a sentence,
   before it is used again.
3. **An everyday analogy comes first, then the shop.** Each pattern is opened
   with a picture from ordinary life — a receptionist, a fuse box, a
   restaurant kitchen — because that is what a listener can hold in their head
   without a diagram. The analogy is then dropped and the online store takes
   over for the worked example. §4 fixes the analogy for each of the twelve so
   they stay consistent across README, explainer, animation and video.
4. **One idea per sentence.** Short sentences, active voice, and the actor named
   before the action. A listener cannot re-read.

The analogies in §4 are for *explanation only*. The code, the tests, the demo
output and the diagrams stay in the online-store domain, exactly as every other
project in this repository does. A project must never introduce a class called
`Receptionist`.

Two checks catch most violations. Read the explainer's opening aloud to somebody
who does not program, and ask them what the pattern is for. And search the
narration for the words *here*, *this*, *above*, *below*, *left* and *right* —
each hit is either a visual dependency or a sentence that can be made clearer.

---

## 3. The store, as a set of services

The other twenty-five projects share a domain. These twelve share something
narrower: **one service map**, used consistently, so a reader meeting their
fourth project already knows what `Pricing` is and can spend their attention on
the pattern.

| Service | What it owns | Notable trait |
| --- | --- | --- |
| `Storefront` | Nothing. The caller — a web or mobile client. | Always the client, never a dependency |
| `Catalog` | Product names, descriptions, images | Read-heavy, cacheable, rarely down |
| `Pricing` | Prices and active promotions | Fast, and must be current |
| `Inventory` | Stock levels and reservations | The one that says no |
| `Orders` | Orders and their line items | The system of record for a purchase |
| `Payments` | Charges and refunds | Slow, external, and occasionally flaky |
| `Shipping` | Shipments and tracking numbers | Fire-and-forget, mostly |
| `Recommendations` | "Customers also bought" | **Optional** — the page is fine without it |
| `Notifications` | Email and push | Fire-and-forget, at-least-once |

Two facts about this map do most of the teaching work across the category, and
projects should lean on them rather than inventing new services:

1. **`Recommendations` is optional and `Payments` is not.** That single
   distinction is what makes fallback the right answer in one place and a bug in
   the other, and it recurs in Circuit Breaker, Retry and API Composition.
2. **`Orders`, `Inventory` and `Payments` each own their data.** No service
   reads another's tables. Every hard problem in projects 7–12 follows from
   that one rule.

Concrete values stay consistent with the existing projects: prices in pounds,
customers as `CUST-001`, products as `SKU-1234`, orders as `ORD-…`.

---

## 4. The scenarios

Each subsection fixes six things: the pattern in plain words, an everyday
analogy for it, the scenario in the shop, why the pattern genuinely fits that
scenario, the naive alternative the project must show failing, and the honest
cost the project must admit to.

The **plain words** line is the one-sentence answer to "what is this pattern?"
for somebody who has never heard of it, and it is the sentence the video's
opening narration and the README's first paragraph are both built from. The
**everyday analogy** is fixed here so that the README, the explainer, the
animation and the narration all use the same picture rather than three different
ones (§2.5).

### 4.1 API Gateway — one front door for the storefront

**In plain words.** Put one service in front of all the others, so a client
makes a single call instead of five, and only has to know one address.

**Everyday analogy.** A hotel reception desk. You do not phone housekeeping,
the restaurant and the concierge separately; you ask reception, and reception
deals with whoever needs dealing with. You need one phone number instead of
five, and when the hotel reorganises its departments, your number does not
change.

The mobile app needs a product page. That means the catalog entry, the current
price, whether it is in stock, and — if it is available — recommendations. Today
the app calls four services itself, which means it knows four addresses, four
authentication schemes and four response shapes, and a change to any of them
ships as an app-store release.

**Why it fits.** The client and the services genuinely want different things:
the services want to stay small and separate, the client wants one call over a
slow mobile link. A gateway is the one place that can hold that tension.

**Naive alternative.** `MobileStorefrontClient` calling the four services
directly, with authentication repeated in each call site, and a comment saying
the web client does the same thing slightly differently.

**Honest cost.** The gateway is a new single point of failure, a new deployment,
and a magnet for business logic that belongs in a service. The project must show
where that line is, and must state that for a single client and three services a
gateway is overhead.

### 4.2 Service Registry and Discovery — finding a live Pricing instance

**In plain words.** Instead of writing down where a service lives, let each copy
of it announce itself to a shared list when it starts, and ask that list for an
address every time you need one.

**Everyday analogy.** A taxi rank instead of a driver's personal phone number.
If you saved one driver's number, you are stuck when they are asleep or have
changed jobs. If you ring the rank, you get whoever is on duty right now. The
catch is the one the pattern spends most of its time on: the rank's list is only
as good as its last update, so a driver who went home five minutes ago may still
be on it.

`Pricing` runs as three instances, and the set changes: one is restarted during
a deploy, another is added on Black Friday morning. Hardcoding an address means
an outage every time that set changes.

**Why it fits.** The question "where is Pricing right now?" has a different
answer minute to minute, and every caller needs the same current answer.

**Naive alternative.** A `PRICING_URL` constant, and then a hand-maintained list
of three constants with a round-robin index, which nothing removes an instance
from when it dies.

**Honest cost.** The registry itself must now be found, and it can be wrong: an
instance that has died but not yet expired its registration is worse than no
registry at all, because callers trust it. The project must show a stale entry
being handed out and the heartbeat that eventually removes it.

### 4.3 Client-Side Load Balancing — spreading catalog reads

**In plain words.** When several identical copies of a service can answer your
question, the caller picks which one to ask, and it takes turns rather than
always asking the same one.

**Everyday analogy.** Choosing a queue at the supermarket checkout. There are
six tills; you look, and you pick. Nobody is standing at the door assigning
shoppers to tills — each shopper decides for themselves, using what they can see.
That is the whole idea, and it is also the whole weakness: everybody looking at
the same short queue walks to it at once.

Three `Catalog` instances are registered. A caller must pick one per request,
and picking badly — always the first, or always the slowest — wastes two thirds
of the capacity the shop is paying for.

**Why it fits.** The choice is per call, the strategies are genuine peers
(round-robin, random, least-connections), and the caller has information a
central balancer does not: how slow each instance was for *it*.

**Naive alternative.** Always calling the first registered instance, which works
in testing, where there is one instance, and concentrates all production load on
one box.

**Honest cost.** Every client now carries balancing logic and its own view of
the world, and those views disagree. The project must show two clients making
different, individually reasonable, collectively bad choices — and must name
server-side balancing as the simpler answer when clients are not yours.

This is also the project that must state plainly that the strategy interface
here is Strategy (§5), so the reader sees a Gang of Four pattern doing real work
inside a microservices one.

### 4.4 Retry with Backoff — a flaky payment gateway

**In plain words.** If a call fails for a reason that might not happen again,
try it once or twice more — but wait a little longer before each attempt, and be
sure that trying twice cannot do the job twice.

**Everyday analogy.** A phone call that does not connect. You redial. If it
still does not connect you wait a moment and try again, rather than jabbing the
button thirty times — partly because it will not help, and partly because
everybody jabbing at once is why the line is busy. Waiting longer each time is
what "backoff" means.

`Payments` fails about one call in five, and almost always succeeds on the next
attempt: a dropped connection, not a declined card. Failing the customer's
checkout for that is throwing away money.

**Why it fits.** The failure is genuinely transient and the operation can be
made safe to repeat. Both halves matter, and the second is the one people skip.

**Naive alternative.** A `for` loop retrying three times immediately, with no
delay, no jitter and no idempotency key — which turns one struggling gateway
into a stampede, and can charge the customer twice.

**Honest cost.** Retrying a non-idempotent operation is how customers get
double-charged, and retrying a *permanent* failure is how a slow system becomes
a dead one. The project must classify errors into retryable and not, must carry
an idempotency key, and must show the double charge happening when it does not —
pinned by a passing test, as every naive alternative in this repository is.

### 4.5 Circuit Breaker — when Recommendations stops answering

**In plain words.** Count the failures. Once a service has failed enough times
in a row, stop calling it altogether for a while and fail instantly instead —
then let one call through later to see whether it has recovered.

**Everyday analogy.** The fuse box in a house, which is where the pattern's name
and its three states come from. When something is badly wrong the fuse trips, and
it stays tripped: the point is not to punish the appliance but to stop the fault
setting the house on fire. Later somebody flips the switch back on to see whether
the problem has gone. If it has, everything runs; if it has not, it trips again
straight away. Closed means current flows, open means it does not, and that is
the one piece of vocabulary worth learning here — an *open* circuit breaker is
the broken-looking one.

`Recommendations` is down and every call to it takes the full three-second
timeout before failing. The product page is now three seconds slower for a
feature nobody would miss, and those blocked threads are the ones checkout
needs.

**Why it fits.** The failure is sustained rather than transient, so retrying is
actively harmful. Refusing to call for a while — and letting one probe through
to see if it has recovered — is the only thing that helps both sides.

**Naive alternative.** Retry, applied to an outage: three attempts, three
timeouts, nine seconds, and a service being kept down by the traffic of everyone
retrying it.

**Honest cost.** A breaker adds state, tuning and a new way to be wrong: too
sensitive and it opens on a blip, too slow and it never opens. It also demands
an answer to "what do we do while it is open", and that answer must be
different for `Recommendations` (show nothing) than for `Payments` (fail the
checkout honestly). The project must show both, and must say that a fallback
which hides a real failure is worse than an error.

This project also carries the comparison with Retry (§4.4): retry a blip, break
on an outage, and the question to ask is whether the next attempt is plausibly
going to work.

### 4.6 Bulkhead — the slow supplier feed and the checkout

**In plain words.** Do not let every job in the system draw from the same pot of
workers. Give the important work its own set, so that a slow job filling up its
own set cannot stop the important work getting a worker.

**Everyday analogy.** The watertight compartments in a ship's hull, which is
literally what a bulkhead is. A hole below the waterline floods one compartment
and the ship stays up; the same hole in an undivided hull sinks it. The cost is
visible in the analogy too — the walls take up space, and a compartment can be
empty while the one next door is full.

One thread pool serves everything. The nightly supplier feed calls a slow
partner API, fills the pool, and checkout — which is fine, and fast — cannot get
a thread. The shop stops selling because of a background job.

**Why it fits.** The resource is genuinely shared and the workloads genuinely
have different priorities. Partitioning the pool is the only thing that keeps
one from sinking the other.

**Naive alternative.** One shared pool, sized for the common case, with a
comment saying it is plenty.

**Honest cost.** Partitioned pools are idle capacity by design: checkout's
threads sit unused while the feed's queue backs up, and the total is worse than
one pool would be *on a good day*. The project must state that trade honestly —
bulkheads cost throughput to buy isolation — and must show the shared pool
drowning first, so the price looks worth paying.

This is the only project in the category that uses real threads. Its tests use a
fixed pool and latches, never sleeps (§2.2).

### 4.7 Database per Service — Orders and Catalog stop sharing tables

**In plain words.** Each service keeps its own data and nobody else is allowed to
read it directly. If you want somebody else's data, you ask them for it.

**Everyday analogy.** Two departments that stop sharing a filing cabinet. While
they share it, either one can reorganise the folders and break the other without
knowing. Once each has its own cabinet, they are free to reorganise — and the
price is that a question spanning both departments now needs two conversations
instead of one look in a drawer. Everything difficult in the rest of this
category is that price being paid.

`Orders` and `Catalog` share one schema, and the order history page joins across
both. It is fast, it is correct, and it means the catalog team cannot rename a
column without breaking checkout.

**Why it fits.** This is the foundational constraint of the whole category, and
it is a decision rather than a technique: every later project in this category
exists because of it.

**Naive alternative.** The shared schema and the join — shown working, because
it does work, and shown as the thing that makes two services one service wearing
two hats.

**Honest cost.** Losing the join is genuinely painful, and the project must not
pretend otherwise. The order history page now needs two calls and an assembly
step (§4.8), reports get harder, and a foreign key that used to be enforced by
the database is now enforced by hope. The project's job is to make the reader
feel that cost and understand what is bought with it.

### 4.8 API Composition — assembling the order details page

**In plain words.** To build one page out of data owned by three services, ask
all three at once, wait for the answers, and put them together yourself.

**Everyday analogy.** Making a sandwich from three different shops. There is no
one shop that sells the finished sandwich, so somebody walks to the baker, the
grocer and the deli, and assembles it at home. Two things follow immediately, and
they are the pattern's whole lesson. Go to the three shops one after another and
lunch takes three times as long, so go at the same time. And if any one shop is
closed, you must decide in advance whether that means no lunch or a sandwich
without the pickle.

The order details page needs the order from `Orders`, the product names from
`Catalog` and the delivery status from `Shipping`. There is no join any more
(§4.7), so somebody has to fetch three things and stitch them together.

**Why it fits.** It is the simplest possible answer to the problem §4.7 creates,
it needs no new storage, and for a page that is read a few times per order it is
the right answer.

**Naive alternative.** Three sequential calls, each waiting for the last, so the
page takes the sum of three latencies — and one that fails takes the whole page
with it, including the parts that had already arrived.

**Honest cost.** The page is as slow as its slowest dependency and as available
as the *product* of its dependencies' availabilities, which is the number that
surprises people: three services at 99.9% give a page at 99.7%. The project must
compute that in the explainer, must show partial results being returned when an
optional service fails, and must name CQRS (§4.9) as the answer when composition
stops being enough.

### 4.9 CQRS — order history without the joins

**In plain words.** Keep two shapes of the same data: one built for changing it
safely, and a second, pre-assembled one built purely for reading quickly. Every
change to the first sends an update to the second.

**Everyday analogy.** A library's card catalogue. The books on the shelves are the
real thing, and there is exactly one copy of each — that is where changes happen.
The card catalogue is a second, redundant copy of the same information, arranged
by author and by title, existing only so that nobody has to walk the shelves to
find something. Both facts you need are in the analogy: looking up a card is far
faster than searching the shelves, and a book that arrived this morning may not
have a card yet. Reading something a moment out of date is exactly what
"eventually consistent" means, and it is fine for a catalogue and fatal for the
count of how many copies are left to lend.

The customer's order history page is read thousands of times more often than an
order is placed, and composing it from three services on every view (§4.8) is
both slow and pointless. A read model, kept up to date by the events the
services already publish, answers it in one lookup.

**Why it fits.** The read and write shapes genuinely differ, and the read side's
requirements — fast, denormalised, tolerant of being a second stale — are
incompatible with the write side's.

**Naive alternative.** The composition of §4.8 on every page view, plus a cache
bolted on top with a five-minute expiry and no way to know when it is wrong.

**Honest cost.** Two models must be kept in step, and the read model is
*eventually* consistent: a customer can place an order and not see it. The
project must show that window happening, must state where it is unacceptable
(never do this for the stock level you sell against), and must say that the
denormalised read model is a second thing to build, test, back up and migrate.

### 4.10 Saga — placing an order across four services

**In plain words.** A job that spans several services is done as a series of
small steps, each of which commits on its own. There is no undo button, so every
step is written together with an action that cancels out its effect, and if a
later step fails the earlier ones are cancelled out in reverse order.

**Everyday analogy.** Booking a holiday: a flight, a hotel and a hire car, from
three different companies. Each booking is confirmed the moment you make it —
there is no way to hold all three "pending" until you are sure. So when the car
company turns you down, nobody rewinds time; you ring the hotel and cancel, and
you ring the airline and cancel. That is the crucial idea, and the one people miss
about this pattern. A cancellation is not the booking being erased. It is a new
event, it may cost you a fee, and it can itself fail — the hotel might not pick
up the phone.

Placing an order reserves stock, takes payment, creates the order and schedules
a shipment. Four services, four databases, no transaction that spans them. If
payment succeeds and shipping refuses, the stock must be released and the money
returned — by explicit action, because there is nothing to roll back.

**Why it fits.** This is the canonical case, and the store's most important
operation. Nothing else in the category makes the absence of a distributed
transaction as concrete.

**Naive alternative.** Four calls in a row inside a `try` block, with a
`@Transactional` annotation on the method that a reader may believe is doing
something, and a catch block that logs and returns. Money is taken; nothing
ships; the log line is never read.

**Honest cost.** Every step needs a compensating action, and compensation is not
rollback: a refund is a new fact, not the erasure of an old one, and some steps
(the confirmation email) cannot be compensated at all. The saga is also
*visible* to the customer as an intermediate state. The project must implement
orchestration, must contrast it with choreography in the explainer, and must
show a compensation running.

This project carries the cross-reference to Command (§5): a saga step and its
compensation are `execute` and `undo` under different names, with the difference
that undo here can itself fail.

### 4.11 Transactional Outbox — never losing the order event

**In plain words.** When you have to save something *and* tell somebody about it,
do not do two separate things that can half-happen. Write the message into your
own database alongside the record, in the same single save, and let a separate
job read those messages and send them afterwards.

**Everyday analogy.** The out-tray on a desk. You do not stop mid-task to run to
the post box, because then you are away from your desk with a half-finished job
and a letter in your hand. You finish the paperwork and drop the letter in the
tray, in one motion, and somebody comes round later to collect the tray. The
letter cannot go missing, because the moment the paperwork was filed the letter
was already in the tray. What the analogy also predicts is the pattern's price:
the collector might post a letter and then forget it had, and come back and post
it again.

`Orders` must save the order and publish `OrderPlaced`. Doing both means two
systems and no shared transaction: commit then publish loses the event if the
process dies in between, publish then commit invents an event for an order that
never existed.

**Why it fits.** The problem is exactly a two-thing-atomicity problem with one
transaction available, and writing the message into the same database, in the
same transaction, is the trick that resolves it.

**Naive alternative.** `repository.save(order); broker.publish(event);` — two
lines that look atomic, are not, and fail in a way no test written by their
author will catch. The project pins the lost event with a passing test.

**Honest cost.** A relay process now polls a table, which is more moving parts,
and delivery becomes **at least once**: a crash between publish and mark-sent
sends the event twice. That is not a flaw to be apologised for — it is the
deliberate trade, and it is what makes §4.12 mandatory rather than optional.

### 4.12 Idempotent Consumer — the duplicate OrderPlaced

**In plain words.** Since the same message can arrive twice, write down the id of
every message you have handled, and if one arrives whose id you already have,
throw it away. Handling it twice then has the same effect as handling it once —
which is all the word *idempotent* means.

**Everyday analogy.** A club doorman with a list of everyone he has already
stamped. Somebody comes back to the door and says they have not been let in yet;
the doorman checks the list, finds their name, and does not stamp them a second
time. The subtle part is the part that goes wrong in real code: the name has to go
on the list at the same moment as the stamp goes on the hand. Stamp first and
write the name afterwards, and a doorman who is interrupted in between will stamp
the same person twice.

`Notifications` receives `OrderPlaced` twice, because the outbox relay
guarantees at-least-once delivery (§4.11). The customer gets two emails; if the
consumer were `Payments`, they would be charged twice.

**Why it fits.** It is the necessary other half of §4.11, and the pattern is
small enough to be shown completely: record the message id inside the same
transaction as the effect, and ignore anything already recorded.

**Naive alternative.** A `HashSet` of seen ids, updated after the work is done —
which loses its memory on restart, and which double-processes if the crash
lands between doing the work and recording the id.

**Honest cost.** The dedupe store grows and needs an expiry policy, and its
window is a guess: too short and a late duplicate slips through, too long and it
is another table to operate. The project must also draw the distinction between
*idempotent handling* — dedupe by id — and a *naturally idempotent* operation
like "set status to SHIPPED", which needs no store at all and is always the
better answer when it is available.

---

## 5. Relationships to the existing twenty-five

The strongest thing this category can teach a reader who has done the other
twenty-five is that these are not a separate discipline. Each project below must
address its assigned comparison head-on in its explainer, in the terms the
repository already uses: a distinguishing question a developer can act on, not
an observation that two things resemble each other.

| Comparison | Addressed in |
| --- | --- |
| API Gateway vs Facade | API Gateway (§4.1) — the same shape, one process boundary apart; a facade simplifies for a caller in the same program, a gateway also crosses a network, terminates authentication and is a deployable thing that can be down |
| Service Registry vs Simple Factory and Singleton | Service Discovery (§4.2) — both answer "give me an instance", but a registry's answer changes without a code change and can be wrong |
| Load-balancing strategies vs Strategy | Load Balancing (§4.3) — the balancer *is* Strategy; the microservices pattern is the deployment context, not a new structure |
| Circuit Breaker vs Proxy and Decorator | Circuit Breaker (§4.5) — a breaker is a decorator that is allowed to refuse to delegate, which is precisely what a decorator may not do |
| Bulkhead vs Object Pool | Bulkhead (§4.6) — pooling is about reuse, bulkheading about partitioning; the same pool class, opposite motivations |
| API Composition vs Facade | API Composition (§4.8) — a facade hides steps that all succeed; a composer must decide what to return when one of them does not |
| CQRS vs Observer | CQRS (§4.9) — the read model is an observer of the write model, with the events durable and the subscriber in another process |
| Saga vs Command and Memento | Saga (§4.10) — `execute`/`undo` across a network, where undo is a new fact rather than a restored snapshot, and can itself fail |
| Outbox and Idempotent Consumer vs Singleton's double-checked locking | Transactional Outbox (§4.11) — both are about an operation that looks atomic and is not; the tell is the same in both cases |

---

## 6. Deliverables per project

Exactly as the repository-wide spec §7 requires, with no additions and no
omissions: `docs/` (prerequisites, problem statement, the explainer, class
diagram, UML sequence diagram, `animation.html`, `session.md`, `youtube.md`,
`thumbnail.png`, and a generated `spec.md` / `spec.html`), `video/` (scenes,
slides, subtitles, build script, `narration.md`, `README.md`), and a top-level
`README.md` quoting the real `./gradlew run` output.

Six category-specific requirements on top:

0. **The explanation works with the eyes closed** (§2.5). The explainer opens
   with the pattern in plain words and the everyday analogy §4 assigns it, before
   any code, any class name and any diagram. Every term of art is defined in
   ordinary language at first use. No sentence anywhere in the project's prose or
   narration depends on the reader looking at something.

1. **One JVM, no infrastructure.** `./gradlew run` must work on a machine with
   nothing installed but a JDK, offline. No Spring, no Docker, no broker, no
   database, no network sockets.
2. **The limitation is stated.** Every explainer says, in its own words, that
   this teaches the shape of the pattern and not the operation of a distributed
   system (§2.1).
3. **The demo prints a timeline** with simulated elapsed time, showing the
   failure and what the pattern did about it (§2.3).
4. **Tests are deterministic and fast.** No `Thread.sleep`, no wall-clock
   dependence, no randomness without a seed; failure is scripted (§2.2). The
   whole suite runs in under two seconds.
5. **Tests assert the property, not the happy path.** As in the behavioural
   category, the outcome is usually reachable without the pattern: an order is
   placed whether or not there is a saga. So the tests must assert what only the
   pattern gives — that the breaker refuses the call while open, that the second
   delivery of a message has no effect, that compensation ran in reverse order,
   that a retry did not fire on a permanent error. **Twelve tests is the working
   floor**, three above the Gang of Four floor, because these patterns have more
   states worth pinning.

---

## 7. Video, poster and publishing

Inherited wholesale from the repository-wide spec §§3–6 and §8: 145 wpm,
Samantha, the two-pass `loudnorm`, one AAC encode at the mux, the continuity
self-check, no strikethrough on the poster, the fixed four-step opening, an
outro that names no successor pattern, and the seven-section `docs/youtube.md`.
The build scripts are generated from `behavioural/strategy-pattern`'s, which is
the most recently reviewed copy.

Three category-specific points:

1. **The narration is self-sufficient.** A listener who never looks at the screen
   must finish the video understanding the pattern (§2.5). Concretely: the
   everyday analogy from §4 is narrated in full before any class name is spoken;
   every slide's narration says what the slide shows rather than pointing at it;
   and code slides are described in words — "the call method asks the breaker
   whether it is allowed to proceed, and throws if it is not" — not read out as
   syntax. The slides illustrate the narration; they do not carry it.
2. **Every project needs a timeline slide.** Not the class diagram, and not a
   summary — the sequence of a failing call and the pattern's response to it,
   in the order it happens.
2. **The naive alternative must be shown running and failing.** These are
   patterns whose value is invisible when everything works; the console slide
   has to contain the double charge, the lost event or the drowned thread pool.

Working titles, all inside the 60-character limit:

| Pattern | Working title |
| --- | --- |
| API Gateway | API Gateway in Java - One Front Door for the Store |
| Service Discovery | Service Discovery in Java - Finding a Live Instance |
| Load Balancing | Client-Side Load Balancing in Java - Catalog Reads |
| Retry | Retry with Backoff in Java - A Flaky Payment Gateway |
| Circuit Breaker | Circuit Breaker in Java - When a Service Stops |
| Bulkhead | Bulkhead Pattern in Java - Isolating a Slow Job |
| Database per Service | Database per Service in Java - Losing the Join |
| API Composition | API Composition in Java - The Order Details Page |
| CQRS | CQRS in Java - Order History Without the Joins |
| Saga | Saga Pattern in Java - Placing an Order, Safely |
| Transactional Outbox | Transactional Outbox in Java - Never Lose an Event |
| Idempotent Consumer | Idempotent Consumer in Java - The Duplicate Message |

---

## 8. Patterns deliberately not included

Naming what is out, and why, is part of the specification — otherwise the list
grows by accretion until the category is a survey rather than a course.

| Pattern | Why not |
| --- | --- |
| Sidecar / Service Mesh | Its entire content is deployment topology. Simulated in one JVM it degrades into "a wrapper class", which teaches nothing the reader did not learn from Decorator. |
| Strangler Fig | A migration strategy measured in months. What it needs is a legacy system with real users, and a story about routing, neither of which survives simulation. |
| Backends for Frontends | A variation on API Gateway (§4.1), and better covered as one section of that project's explainer than as a thirteenth video. |
| Distributed Tracing | Worth knowing, but honest tracing needs a collector and a UI; a correlation id threaded through method calls is a five-minute topic, and lands in the API Gateway project instead. |
| Event Sourcing | Genuinely large, and frequently confused with CQRS (§4.9) — which is exactly why it is not squeezed in next to it. A candidate for a future project, on its own. |
| Service Mesh / Config Server / Externalised Configuration | Operational concerns rather than design patterns. Nothing about them is visible in the code a reader would write. |

---

## 9. Conformance

A microservices project is compliant when it passes **every item of the
repository-wide checklist** (`video-and-publishing-spec.md` §9) plus these eight:

- [ ] The explainer opens with the pattern in plain words and the everyday
      analogy §4 assigns it, before any class name, and every term of art is
      defined in ordinary language at first use.
- [ ] The narration stands alone with the screen off: the analogy is spoken in
      full before the code, no sentence points at a visual, and a search of the
      narration for *here*, *this*, *above*, *below*, *left* and *right* turns up
      nothing that needs the picture.
- [ ] The scenario is the one this document assigns to the pattern, uses the
      service map in §3, and the "when not to use this" section states the
      honest cost named here.
- [ ] `./gradlew run` works offline with only a JDK installed; the project
      starts no server, opens no socket and needs no container.
- [ ] The explainer states the limitation of §2.1 — the shape is real, the
      distributed system is not.
- [ ] The demo output is a timeline that shows the failure and the pattern's
      response, not just a final answer.
- [ ] Tests are deterministic — no sleeps, no wall clock, seeded randomness —
      run in under two seconds, and there are at least twelve of them,
      including one that pins the naive alternative's wrong behaviour.
- [ ] The cross-reference this document assigns to the project (§5) is present
      and states a question a developer can act on.
