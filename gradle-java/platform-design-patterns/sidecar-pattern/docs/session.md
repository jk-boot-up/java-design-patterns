# Session Guide — Sidecar Pattern

A one-hour facilitated session. It works as a live-coded walkthrough, a
study-group session, or a lunchtime talk with the exercises cut.

The session has one shape: make the room solve the March policy change themselves
before they have heard the pattern's name. They will solve it the way the shop
solved it — open each service and change two lines — and they will miss the fourth
service, because you are going to give them only three.

---

## Learning Objectives

By the end, everyone can:

1. Count the copies of a cross-cutting decision in a system, and say why sixteen
   copies is a different number from four services.
2. Explain why the failure and the cause landed in different repositories on the
   night of the incident, and why no test in any of the four could have caught it.
3. State the pattern in one sentence, and name the two things that make a sidecar
   a sidecar rather than a library.
4. Draw the line between what may move into a proxy and what must not, and say how
   the wrong answer fails.
5. Name all three items on the bill — the extra process, the extra failure, the
   extra millisecond — without being prompted.
6. Say honestly what the difference is between this pattern and Decorator, and give
   the two questions that decide between them.

---

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:06 | Setup, and a maintenance question |
| 0:06–0:20 | The problem: sixteen copies, and the night |
| 0:20–0:30 | The pattern: stand it next door |
| 0:30–0:38 | Code walkthrough |
| 0:38–0:48 | Exercises |
| 0:48–0:57 | The bill, and the Decorator admission |
| 0:57–1:00 | Wrap-up |

---

## 0:00–0:06 — Setup, And A Maintenance Question

Have everyone run:

```bash
./gradlew run
```

While it runs, put this on screen — no code, just the situation:

> Your shop charges cards in four places: checkout, refunds, overnight
> subscription billing, and Friday payouts to sellers. Four teams, four
> repositories.
>
> Your payment provider writes to you. From now on: at most three attempts per
> payment, and wait properly between them.
>
> You are the platform engineer. What do you do this afternoon?

Take answers for three minutes. You will reliably get "change it in all four",
"put it in a shared library", and "surely there's a config service for this".
Write all three up without judging any of them. All three are reasonable and the
project takes all three seriously.

**Facilitator note:** do not name the pattern. Do not say the word "proxy". The
room is currently standing exactly where the shop stood in March, which is the
only place from which the incident is surprising.

---

## 0:06–0:20 — The Problem: Sixteen Copies, And The Night

Walk Acts 1, 2 and 3 on screen. Give each one about four minutes.

**Act 1.** Read the grid out loud, then read the two lines under it:

```
  copies of a cross-cutting decision: 16
  places to edit to change one:       4
```

Ask the room which of the sixteen values is about checkout, or about refunds, or
about subscriptions. None of them are. They are all facts about a network and a
supplier's contract — they would be identical if the shop sold bicycles. That is
the definition of a **cross-cutting concern**, and it is worth writing on the
board in exactly those terms.

**Act 2.** The engineer does the obvious thing and does it well. Three pull
requests, three reviews, three releases, one afternoon. Then show the fourth row.

Stop here and ask the room, seriously: *"Whose fault is that?"* Let them try. The
answers will be "the billing team", "the engineer", "the process". Then say
plainly: **nobody was careless and nobody was wrong.** There was no fourth place
to look unless you already knew to look there.

Then close the door on the three easy escapes, because someone will reach for
each one:

- *"A test would have caught it."* A test lives inside one service and can only
  see that service's copy. Subscription billing's tests all pass — its copy is
  internally consistent.
- *"A checklist would have caught it."* A checklist requires somebody to know a
  fourth copy exists. That knowledge is the missing thing.
- *"A shared library fixes it."* Best objection, and the session comes back to it
  at 0:57. Park it visibly on the board.

**Act 3.** Run it and read the failure rows slowly. Then read the ledger:

```
    subscription-billing  6 attempts
    marketplace-payouts   1 attempt
    total                 13 of 12 allowed, 1 refused
```

Ask which service has the bug and which service failed. They are not the same
service. **Subscription billing — the one that misbehaved — succeeded, and its
dashboard is green.** Marketplace payouts — correct in every line, updated in
March — did not pay the sellers.

> This is the sentence to leave hanging over the next twenty minutes: on Monday
> morning somebody opens an incident about marketplace payouts, and every line of
> that service is correct.

---

## 0:20–0:30 — The Pattern: Stand It Next Door

State it once, and slowly:

> Move the cross-cutting concern out of the service and into a **separate
> process** that runs beside it on the same machine. The service talks to
> `localhost` and knows nothing else. The proxy is the only thing that leaves the
> machine.

Then pull out the two words that carry it, because each rules out a near-miss:

- **Separate process.** Not a library, not a base class, not a framework. It is
  not compiled into your service and it does not change when your service is
  rebuilt. This is the whole of the difference, and it is also the whole of the
  cost.
- **Beside.** Same machine, same lifecycle, one per service instance. Not a shared
  proxy somewhere on the network — that is a different pattern with different
  failure modes, and it does not give you `localhost`.

Walk Act 4. Two things to draw out:

1. Every service now has the same policy, and it was **stated once**, not applied
   four times. Show the test:

   ```java
   for (Sidecar sidecar : sidecars) {
       assertSame(one, sidecar.config(), "every sidecar must read the same one");
   }
   ```

   `assertSame`, not `assertEquals`. Ask the room why that matters. Four equal
   copies would be the March problem again with better manners.

2. Twelve of twelve attempts, nobody refused. The wobble still happened. The
   gateway was still bad for three hundred milliseconds. Nothing about the network
   improved — the shop simply stopped spending its allowance in the wrong place.

---

## 0:30–0:38 — Code Walkthrough

Five files, eight minutes. The code is small on purpose.

**`PaymentGateway.java`** — start at the callee, not the caller. Point at the fact
that it owns the `CallLog`. Every attempt count in this project comes from the
supplier's ledger, never from a service's own tally, because a service's belief
about how many times it tried is precisely what was wrong.

**`CheckoutService.java`** — read the retry loop. Then say: you are going to see
this loop five times today.

**`SubscriptionBillingService.java`** — put it side by side with checkout and ask
the room to find the difference. Give them thirty seconds of silence. The
difference is that `applyPolicyReview()` **is not there**. Then show the test:

```java
assertTrue(!methods.contains("applyPolicyReview"),
        "the point of this project is that nobody wrote this method here");
```

> Say this out loud: the incident is not a wrong value. It is an absence. Nothing
> in any build, in any repository, knows that a fourth file exists.

**`Sidecar.java`** — the same loop one more time, reading `config` instead of its
own fields, plus `clock.waitFor(HOP_MILLIS)` before each attempt. That one line is
Act 7's entire bill, and it is deliberately in the source where they can see it.

**`Concerns.java`** — read the two methods together:

```java
public static int copiesInsideTheServices(int services) { ... }
public static int copiesBesideTheServices() { ... }
```

Ask what happened to the argument. It is gone, because the answer does not depend
on how many services there are. **The missing parameter is the pattern.**

---

## 0:38–0:48 — Exercises

### Exercise 1 — Add the fifth service (everyone, 4 min)

Add a `GiftCardsService` by copying `RefundsService`. Do not touch anything else.
Run `ConcernsTest`.

`copiesInsideTheServices(5)` is now 20, and `copiesBesideTheServices()` is still 4.

Discuss: the first number grew and the second did not, and that is not a slogan —
it is the return type of a method with no arguments.

### Exercise 2 — Repair the fourth copy (everyone, 3 min)

Add `applyPolicyReview()` to `SubscriptionBillingService` and make its fields
non-final. The tests fail.

Ask whether that is the tests being wrong. It is not. The absence is the subject
of the project — and more usefully, ask the room how they would have known to open
that file in March. Nothing tells you. That is the answer.

### Exercise 3 — Put a business rule in the proxy (discussion, 3 min)

Ask: could we also move "refunds are not allowed after ninety days" into
`SidecarConfig`? It is a rule, it is shared, it would be one line.

Let them argue. Land it: the day a business rule lives in a proxy's configuration,
a developer will read the whole refunds service and not find the rule that governs
refunds. **The line is not "shared or not shared". It is "about the network, or
about the shop".**

### Exercise 4 — Stretch

Change `Sidecar.HOP_MILLIS` from 1 to 5 and rerun. Then ask: on a payment that
takes 600 milliseconds, does that matter? On an internal call between two of the
shop's own services that takes 2 milliseconds, does it? Every hop in a meshed
system is paid twice — leaving one service and entering the next.

---

## 0:48–0:57 — The Bill, And The Decorator Admission

Three costs, and then the honest part.

**Act 5 — the extra process.** Put the third row up on its own:

```
  processes to run and patch                     4         8
```

Say it plainly: the pattern **doubled** the number of things to run, monitor,
version, patch and restart. Read all three rows or none of them.

**Act 6 — the extra failure.** Run it. The gateway is healthy, the service is
healthy, the network is healthy, and:

```
    connection refused to localhost — no sidecar beside checkout
    attempts that reached the gateway: 0
```

Zero. Ask what the service can do about it. Nothing — we deleted the retry code on
purpose in Act 4. **When a sidecar goes, it does not take one call with it; it
takes every call that service makes.** The failure is rarer than the network's and
wider.

**Act 7 — the extra millisecond.** Six hundred against six hundred and three. On
a payment, nothing. On a two-millisecond internal call, fifty per cent. This is
arithmetic, not taste, and it is the arithmetic that decides whether a service mesh
belongs in your system.

**Then the admission, and do not skip it.** Everything in this project happened in
one Java program. In one program, a proxy the service talks through is an object
wrapping another object — and that is Decorator, from §11. The `Sidecar` class
would not surprise anybody who has read it.

Now go back to the shared-library objection you parked at 0:20, and answer it with
two questions. Write them up:

- *Does this concern need to change without rebuilding the service?*
- *Does it apply to a service written in a language your library does not support?*

Yes to either, and it goes next door. **No to both, and a library in your own
process is cheaper, faster, and has one fewer thing that can fail.** Say that last
part with a straight face — a room that leaves thinking every cross-cutting concern
deserves a proxy has learned the wrong lesson.

---

## 0:57–1:00 — Wrap-Up

One sentence back:

> Put the cross-cutting concern in a process that runs beside the service, so it
> can be changed without opening the service, and pay for that with an extra
> process, an extra thing that can be down, and a millisecond on every call.

One question to take away:

> In your own system, how many copies are there of the decision you would have to
> change if your biggest supplier wrote to you tomorrow — and could you name every
> file without grepping?

---

## Facilitator Notes

**The most common wrong turn** is a room that treats the incident as a process
failure — better checklists, better ownership, a Jira ticket per repository. Head
it off at Act 2 by insisting that nobody was careless. If the fix is "be more
careful", the pattern has no reason to exist.

**The second most common** is confusing a sidecar with an API gateway. The gateway
is at the front door and sees traffic coming *in*. These four services are making
calls *out*, to a supplier. A gateway never sees them. `problem-statement.md` has
one paragraph on this if you need it.

**The third** is a room that falls in love with it and wants a proxy for
everything. Act 5's third row and Act 6 exist for exactly that. If you are short of
time, cut an exercise — never the bill.

**If a senior engineer says "this is just a decorator"** — agree with them
immediately and enthusiastically, and then make it the last ten minutes of the
session. They are right about the structure and the interesting question is what
the process boundary buys. That objection is the best thing that can happen to this
session.

**If somebody raises service meshes, Istio or Envoy** — good. Say that a mesh is
this pattern applied to every service automatically, and that the arithmetic in Act
7 is exactly how you decide whether that is worth it. Do not let it become a
twenty-minute tools discussion.

**If somebody asks why this project has no second process** — answer honestly:
Tier 1 runs on a JDK and nothing else so that anybody can run it, and the project
says out loud in four places that it is Decorator until you deploy it separately.
`real/` has the genuine second process: nginx beside the service, with the retry
policy in a config file nobody compiles.

**Timing pressure.** If you are behind at 0:38, cut Exercises 2 and 4. Protect the
last nine minutes at all costs.

---

## Materials Checklist

- [ ] Everyone has a JDK 21 and has run `./gradlew run` before the session starts
- [ ] Acts 1, 2 and 3 output on screen, ready to show
- [ ] `CheckoutService.java` and `SubscriptionBillingService.java` open side by
      side, ready for the thirty seconds of silence at 0:30
- [ ] `docs/animation.html` open in a browser tab
- [ ] `docs/uml-diagram.md` ready — the process boxes are the point
- [ ] The one-sentence definition written somewhere visible for the whole hour
- [ ] The two deciding questions from 0:57 on a slide of their own
