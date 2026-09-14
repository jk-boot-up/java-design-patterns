# Session Guide — CQRS

A one-hour session. The mechanism takes five minutes: publish what you did, keep a
prepared answer, read the prepared answer. Everything worth the hour is the two things
either side of it — why a cache is not this, and what you are not allowed to do with a
read model once you have one.

Protect the last twenty minutes. A room that leaves thinking CQRS is "a cache you
control" has learned something worse than nothing.

**Audience:** developers who know Java and have used a cache in anger. No
distributed-systems or event-sourcing experience assumed.

**Format:** laptops open. Everything runs offline with a JDK. There is no broker and no
database to install, which is worth saying at the start because people will ask.

## Learning Objectives

By the end, a participant can:

1. Explain why composing a page on every view is correct and still wrong at scale, and
   why nothing will ever alert you to it.
2. State the difference between a cache and a read model without using the word "fast".
3. Say where the work went rather than claiming it disappeared.
4. Describe the staleness window honestly, including the frame where a paid order is not
   on the customer's page.
5. Say the rule — never decide anything with a read model — and name what enforces it.
6. Argue for or against a projection in a system of their own, using the read-to-write
   ratio as the test.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:05 | Setup check, and being fair to composition |
| 0:05–0:14 | Act one: the cost nobody is paged about |
| 0:14–0:26 | The cache, taken seriously and then taken apart |
| 0:26–0:36 | The mechanism, and act two |
| 0:36–0:44 | Act three: eventual consistency, shown rather than mentioned |
| 0:44–0:56 | Act five, the rule, and exercises |
| 0:56–1:00 | Wrap-up |

## 0:00–0:05 — Setup Check, And Being Fair

```bash
cd micro-services-design-patterns/cqrs-pattern
./gradlew test
```

18 tests, green, in about a second.

Then open `ComposingOrderHistory` and spend two minutes defending it. The catalog call is
batched. There is no loop. It is the API Composition pattern done properly.

> Nobody would object to this in review, and nobody has ever been paged about it. That
> is exactly why it survives.

## 0:05–0:14 — Act One

```
  3 views cost 270ms and 6 service calls
  every view rebuilt a page identical to the last one
```

**Ask the room what is wrong with this before you say anything.** Someone will say "it's
slow". Push back — ninety milliseconds is not slow. Let them get to it.

Two facts to land:

1. **The ratio.** An order is placed once. Its page is viewed by the customer, the
   confirmation email, a support agent, the customer again next week. The facts changed
   once; the shop paid a thousand times.
2. **The dependency.** Every view is a live call to two services. A page about orders the
   customer has *already paid for* cannot be shown if Catalog is down.

The second one usually surprises the room more than the first, and it is the one that
survives contact with their own systems.

## 0:14–0:26 — The Cache

This is the best twelve minutes in the session. Do not rush it.

Ask for the fix. Somebody will say cache. **Agree enthusiastically**, then open
`CachedOrderHistory` and run `itCachesThePage`. It works. The second view is free.

Then walk the other four tests, one at a time, and let each one land before moving on:

- `itServesAPageItKnowsNothingAbout` — it stored rows. It never understood them.
- `aRenameCannotInvalidateIt` — Catalog renames a product. The cache has no idea, and
  there is no mechanism by which it could be told.
- `itIsCorrectedByATimerAndNothingElse` — the only thing that will ever fix it is the
  clock.
- `thereIsNoFreeSetting` — and so you tune an expiry forever.

Then put the sentence on the board and leave it there for the rest of the session:

> **A cache is a copy that cannot know it is wrong.**

Ask the room what would have to be true for the copy to know. Wait. Somebody will say
"it would have to be told." That is the pattern, and they just invented it.

## 0:26–0:36 — The Mechanism, And Act Two

The mechanism is small and should feel small:

```java
public void apply(ShopEvent event) { ... }
```

A write side that publishes what it did. A bus. A listener that keeps a prepared answer.
A query that reads it and calls nobody.

Then act two:

```
  3 views cost 15ms and 0 service calls
  the work did not vanish: Catalog was called 1 time when the order was placed
```

Point at both numbers, and be clear which is bigger news:

- **5ms instead of 90ms** is latency, and it is the headline.
- **0 service calls** is availability. `readsSurviveAnOutage` takes Orders down and the
  page still renders. The composing version could never do that.

And say the honest line out loud, because the demo does:

> The work did not vanish. It moved to write time. That is only a good trade because a
> shop places one order and shows the page a thousand times. Invert the ratio and this
> pattern is a straight loss.

## 0:36–0:44 — Act Three

```
  ord-5001 is placed, paid for, and final
  events still in flight: 3
  rows on the customer's order history page: 0
```

Stop on this frame. Read all three lines aloud. **Ask the room if they would ship it.**

Then the two properties that make it survivable, and insist on both:

- The window is short.
- It closes **by itself**. `theWindowClosesByItself` is a separate test from
  `theStalenessWindowIsReal` on purpose, because they are separate promises.

Then the question that makes it real: for which of *your* pages is this fine, and for
which is it not? Order history, fine. The screen a warehouse worker packs from, not.

## 0:44–0:56 — Act Five, The Rule, And Exercises

```
  read model still shows on the shelf: 1
  the ledger actually has: 0
  the ledger refused: cannot reserve 1 of SKU-KETTLE, only 0 left
  it was the write side that saved the shop, because the sale was decided there
```

Put the rule on the board and make somebody say it back:

> **Show a read model's number. Never decide anything with it.**

Then ask what enforces that rule. The answer is uncomfortable and worth sitting in:
nothing in the type system. A test, a review, and people remembering.

Finish with the consolation, because it is genuinely liberating:

```
  and a read model is throwaway: rebuilt from 6 events, 2 rows back
```

### Exercise 1 — Break the rule (everyone)

Change the second purchase to check `stockOnDisplay` and sell if it says yes. Watch
`theWriteSideIsWhereASaleIsDecided` fail, and notice that in a real shop this failure
would be a customer being charged for a kettle that does not exist.

### Exercise 2 — Teach the projection a new event (everyone)

Add a fourth `ShopEvent` and do *not* handle it in `apply`. The sealed interface means
the compiler tells you. Then discuss what would have happened without `sealed`: a
projection silently ignoring facts, drifting, with every test still green.

### Exercise 3 — Tune the cache (pairs)

Find an `EXPIRY_MILLIS` that is both fast and correct. They cannot.
`thereIsNoFreeSetting` is the point; let them spend five minutes proving it to
themselves.

### Exercise 4 — Discussion: the ratio

On a system they actually work on: pick a page, estimate reads per write. Under about
ten to one, ask honestly whether a permanent second copy of the data is worth it.

## 0:56–1:00 — Wrap-Up

Five sentences:

1. Commands change things, queries read things, and they are different jobs.
2. A cache is a copy that cannot know it is wrong; a read model is a copy that is told.
3. The work moved to write time. It did not vanish, and the ratio is what funds it.
4. The staleness window is real, it is sometimes alarming, and it closes by itself.
5. Never decide anything with a read model — and if you delete one, replay the events
   and it comes back.

## Facilitator Notes

- **Do not attack the cache too early.** Let the room enjoy it working first. The
  argument only lands if they have felt it be the obvious right answer.
- **"So CQRS is event sourcing?"** will come up, probably twice. Answer it flatly: no.
  This project projects from events; it does not store events as the system of record.
  You can use either without the other, and conflating them is why people think this
  pattern is much bigger than it is.
- **Expect "we could just invalidate the cache on a rename".** Take it seriously, then
  ask what does the invalidating. The answer is: something that subscribes to events —
  at which point they have built a read model with extra steps and worse guarantees.
- **Expect "isn't this just denormalisation?"** Partly yes, and that is a good instinct.
  The addition is *who keeps it correct*, and the answer is the event stream rather than
  a nightly job.
- **The act three frame is the emotional centre of the session.** Do not summarise it.
  Show it, stop, and ask.
- **Timings assume a group that argues.** The mechanism section compresses. The cache
  section and act five do not.

## Materials Checklist

- [ ] JDK 21 installed, `./gradlew test` run once beforehand so nothing downloads live
- [ ] A terminal with a font big enough to read act one's timeline from the back
- [ ] [`animation.html`](animation.html) open in a browser tab for the two copies drifting
- [ ] [`uml-diagram.md`](uml-diagram.md) open for the five acts as sequences
- [ ] A whiteboard, for "a cache is a copy that cannot know it is wrong" and the rule
