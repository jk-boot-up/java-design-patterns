# Session Guide — Backends for Frontends Pattern

A one-hour facilitated session. It works as a live-coded walkthrough, a
study-group session, or a lunchtime talk with the exercises cut.

The session has one shape: spend the first twenty minutes making the group argue
themselves into a shared endpoint, so that when it fails they have watched their own
reasoning fail rather than somebody else's.

---

## Learning Objectives

By the end, everyone can:

1. Say why five calls from a phone is a different problem from five calls inside a
   data centre, and count both.
2. Explain why a `?fields=` parameter solves the size problem completely and solves
   nothing that matters.
3. State the pattern in one sentence and name the three words that carry it — each,
   own, shape.
4. Draw the line between a backend for a frontend and an API gateway using one
   question.
5. Say what may live inside a backend for a frontend and what must live behind it,
   and why the wrong answer fails without an error.
6. Give the rule for how many backends a shop should have, and defend a case where
   two clients share one.

---

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:06 | Setup, and a design question |
| 0:06–0:18 | The problem: five calls, then one endpoint |
| 0:18–0:28 | The pattern: a backend per frontend |
| 0:28–0:38 | Code walkthrough |
| 0:38–0:50 | Exercises |
| 0:50–0:58 | The bill |
| 0:58–1:00 | Wrap-up |

---

## 0:00–0:06 — Setup, And A Design Question

Have everyone run:

```bash
./gradlew run
```

While it runs, put this on screen — no code, just the two lists:

> The phone's product screen draws: title, price, one photo, rating, rating count,
> and one line about delivery. Six things.
>
> The desktop page draws fifteen, including the description, five photos and three
> reviews.
>
> You have five services. Design the API.

Take answers for three minutes and write each one up. You will reliably get:
"the phone calls the services", "one endpoint that returns everything", and if
somebody has read ahead, "GraphQL". Write all three down without judging any of
them.

**Facilitator note:** resist naming the pattern. The room has just proposed the two
designs the first two acts demolish, which is exactly the position you want them in.

---

## 0:06–0:18 — The Problem: Five Calls, Then One Endpoint

Walk Act 1 and Act 2 on screen.

**Act 1.** Point at the five, not the bytes. Ask: *"How many of these five can
happen at the same time?"* Somebody will work out that they cannot — pricing needs
to know which product, which means the catalog has to answer first. Five waits, in
sequence, on a train.

**Act 2.** Give the shared endpoint its due first. One call instead of five is a
real win and the pattern keeps it. Then read the waste figure — 87% — and let the
room propose the fix. They will propose `?fields=`, every time.

Then run it and show that it *works*: 212 bytes.

> This is the moment the session turns. Say plainly: if this pattern were about
> payload size, we would be finished, and the answer would be a query parameter.

Now show the delivery line:

```
delivery sentence: not available -- a field like this belongs to one client, and
                   this endpoint belongs to all of them
```

Ask the room to estimate the work: joining stock, a delivery date and the clock into
one sentence. They will say an afternoon. Then ask who has to agree to it.

**Facilitator note:** if the room has lived through this, they will start telling
their own five-week stories here. Let it run for a minute — it is the most valuable
minute of the session, and it is the only part you cannot supply yourself.

---

## 0:18–0:28 — The Pattern: A Backend Per Frontend

State it once:

> Give each frontend its own backend, owned by the team that owns the screen, whose
> only job is to turn what the shop knows into the exact shape that one screen draws.

Then pull the three words apart, because each one rules out a common near-miss:

- **Each** — more than one. One box in front of the services is a gateway, not this.
- **Own** — the phone team changes it. A platform-owned "mobile API" recreates the
  five-week queue with a new name.
- **Shape** — not rules. This is the setup for the bill.

Walk Act 3 and Act 4. On Act 4, cover the bytes column with your hand and read only
the last two:

```
  five calls from the phone       5 device   5 internal
  one shared endpoint             1 device   5 internal
  a backend for the phone         1 device   4 internal
```

Ask what happened to the four missing device calls. Answer: nothing happened to
them. They are still being made, on a network that costs nothing. **The pattern
moves work; it does not remove it.**

Then Act 3's price field. `4799` became `"£47.99"` — ask where that conversion would
have happened otherwise, and how long it takes to fix a formatting bug that shipped
inside a mobile app.

---

## 0:28–0:38 — Code Walkthrough

Five files, in this order. Keep it to eight minutes; the code is deliberately small.

**`Screens.java`** — two lists of field names. This is the ruler. Everything the
project calls "waste" means "not on one of these lists".

**`SharedApi.java`** — show `product(sku, fields)` and then `joinedDelivery()`. The
second returns a hard-coded sentence, and that is the point: there is no code that
could go there.

**`MobileBff.java`** — read the returned document *first*, then the method. Two
things to draw out:
- there is no `shop.recommendations(sku)` call, because the screen has no
  related-products strip;
- `deliveryPromise` is four lines, and it is the field they waited five weeks for.

**`WebBff.java`** — fifteen fields, five services, and `delivery` is the bare date
rather than a sentence. Ask whether that inconsistency is a bug. It is not: the
desktop has a delivery panel and wants the parts.

**`ClientBackend.java`** — one method, and it could be deleted without breaking
anything. Ask why it is there. The answer is that it names the claim: this shop has
more than one idea of what a product screen is, and both are legitimate.

---

## 0:38–0:50 — Exercises

### Exercise 1 — Break the guard rail (everyone, 4 min)

Add a seventh field to `MobileBff.productScreen` — the warehouse name, say. Run the
tests.

`sendsOnlyWhatIsDrawn` fails, because the assertion is `assertEquals(Screens.PHONE,
screen.paths())` — equality, not containment.

Discuss: why equality? Because a field that arrives and is never drawn is exactly
the waste the pattern exists to remove, and without this test every backend grows
back into a shared endpoint over about eighteen months.

### Exercise 2 — Move a decision into the app (everyone, 4 min)

Change the phone's `price` field to return the raw integer `4799` instead of
`Money.format(...)`, and change `Screens.PHONE` so the test still passes.

Now ask: the app has to format it. It ships in three languages. A customer on an
eighteen-month-old Android build sees whatever the app did then. How long is the fix
cycle for a formatting bug in each design?

### Exercise 3 — Find the divergence (discussion, then code, 4 min)

Before running anything, ask the room how they would *detect* the Act 5 failure in
production. Take answers. Most rooms arrive at "a customer complains" and are
unhappy about it.

Then fix it: in `ProductScreenDemo`, pass `SavingRules.current()` to the phone's
backend instead of `SavingRules.copiedBeforeTheReview()`. One line. Point out that
nothing in the codebase would ever have told them which line.

### Exercise 4 — Stretch

Make the four internal calls in `MobileBff` concurrent. How much does the pattern's
advantage grow? This is the exercise that shows how much the simulation understates
the benefit — four sequential internal calls become roughly one.

---

## 0:50–0:58 — The Bill

Three costs, about two and a half minutes each.

**Act 5 — divergence.** Run it. Put the two lines side by side:

```
  desktop store says:  (nothing — no saving may be claimed for this price)
  phone app says:      Save £12.00
```

Ask what went wrong. The room will look for the bug. Say plainly: there isn't one.
The copy was correct when it was written, it is well named, its tests pass, and it
is wrong only in relation to a decision made months later by people with no reason
to know it existed.

Then give the rule, and make them write it down: **a backend for a frontend holds
the shape. Anything the shop would still believe with every client switched off
belongs behind it.**

**Act 6 — the gateway line.** Eight copies against four. Ask the question that
settles every "is this a gateway or a BFF?" argument:

- *"What does this screen need?"* → a backend for that frontend.
- *"Is this request allowed in at all?"* → in front of all of them.

**Act 7 — how many.** Read the six clients. Stop on the tablet and let the room
argue about whether it deserves its own backend. Land on the rule: not per device,
not per team — **per genuine disagreement about what a product is.** Then read the
four recurring costs and the closing line: two backends is a pattern, nine is a
department.

---

## 0:58–1:00 — Wrap-Up

One sentence back:

> Each frontend gets its own backend, owned by the team that draws the screen, and
> it holds the shape and nothing else.

One question to take away:

> In your own system, what is the last thing a client had to wait for because the
> endpoint it uses belongs to everybody?

---

## Facilitator Notes

**The most common wrong turn** is a room deciding early that this is about payload
size. Head it off by showing that `?fields=` works. A session that does not do that
produces people who add a query parameter and believe they have applied the pattern.

**The second most common** is confusing this with an API gateway. Keep Act 6's
question visible from the moment you first say the pattern's name.

**The third** is "so we build one per app". Act 7 exists for that, but if you are
short of time, cut something else. A room that leaves with "one per client" will
build nine backends.

**If a senior engineer objects that this duplicates logic** — agree with them
immediately, and say Act 5 is that objection in code. The objection is right, and
the answer is not that it does not happen, it is that only *shape* goes inside.

**If somebody raises GraphQL** — take it seriously. It is a real alternative to this
pattern and answers the same problem by letting each client describe its own shape.
Note that it moves the ownership question rather than removing it: somebody still
owns the schema, and adding the delivery sentence to it is still somebody's queue.

**Timing pressure.** If you are behind at 0:38, cut Exercise 2 and Exercise 4. Never
cut the bill — a session that ends at Act 4 has sold a pattern without its cost, and
that is the failure mode this whole course is written against.

---

## Materials Checklist

- [ ] Everyone has a JDK 21 and has run `./gradlew run` before the session starts
- [ ] Act 1 and Act 2 output on screen, ready to show
- [ ] `docs/animation.html` open in a browser tab
- [ ] `docs/class-diagram.md` image ready for the 0:28 walkthrough
- [ ] The one-sentence definition written somewhere visible for the whole hour
- [ ] Act 6's two questions on a slide of their own
