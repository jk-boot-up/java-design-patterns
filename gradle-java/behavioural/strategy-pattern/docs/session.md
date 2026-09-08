# Session Guide — Strategy Pattern

A 60-minute guided session for teaching or self-studying the Strategy
pattern using this project.

- **Audience:** beginners comfortable with core Java
- **Duration:** ~60 minutes
- **Format:** live coding + discussion
- **Prerequisites:** see [`prerequisites.md`](prerequisites.md)

> **Optional pre-work.** Ask participants to watch the video
> (`video/strategy-pattern-explained.mp4`) beforehand. If they do, you can
> compress the problem and pattern segments and spend the extra time on the
> exercises. If you are teaching a group that has *not* watched it, run the
> session exactly as written below.

## Learning Objectives

By the end of this session a participant should be able to:

1. Describe, in one sentence, what problem the Strategy pattern solves.
2. Explain why `CheckoutService` takes a `ShippingCostRule` as a
   constructor argument instead of a `ShippingMethod` enum.
3. Identify the three roles — strategy, concrete strategy, context — in
   real code.
4. Say honestly where the branch went, and why a registry at the edge is
   not the same thing as a `switch` in the pricing logic.
5. Distinguish Strategy from State, and from Simple Factory.

## Timetable

| Time | Segment | Mode |
| --- | --- | --- |
| 0:00–0:05 | Setup check | Hands-on |
| 0:05–0:15 | The problem | Discussion |
| 0:15–0:25 | The pattern | Explanation |
| 0:25–0:40 | Code walkthrough | Live coding |
| 0:40–0:50 | Exercises | Hands-on |
| 0:50–0:58 | Pitfalls & comparisons | Discussion |
| 0:58–1:00 | Wrap-up | — |

## 0:00–0:05 — Setup Check

Everyone runs:

```bash
java -version
./gradlew run
```

Anyone whose build fails pairs up with a neighbour. Do not debug installs
during the session — that is what the prerequisites doc is for.

## 0:05–0:15 — The Problem

**Do not show `ShippingCostRule` yet.** Start with the pain.

Open `NaiveCheckoutService` and put the whole `quote` method on the screen.
Read the four branches out loud, slowly. Then ask:

> *"Everything in this method is correct. Every price it produces is
> right. So what is wrong with it?"*

Let the group work. Steer towards, in this order:

1. Four unrelated policies live in one method.
2. None of them can be tested without going through checkout.
3. A fifth rule means editing the method every existing rule depends on.

**Then point at the `default` branch.** Ask:

> *"What happens if I add `LOCKER_COLLECTION` to `ShippingMethod` and
> forget this method exists?"*

Land it hard: the shop ships for free. No compile error, no exception, just
a quietly wrong number on the receipt. This is the moment the session turns
— it converts "this is a bit untidy" into "this is a live hazard".

## 0:15–0:25 — The Pattern

Use the getting-across-town analogy from
[`strategy-pattern-explained.md`](strategy-pattern-explained.md). Ask:
*"When you walk to the station, do you re-decide 'bus or bike?' at every
street corner?"* Land on: no — the choice is made once, then you just use
it.

Show the class diagram ([`images/class-diagram.png`](images/class-diagram.png))
and name the three roles. Then show the sequence diagram
([`images/uml-diagram.png`](images/uml-diagram.png)) and point out that its
two halves have the *same message sequence* with different participants.

Optionally open [`animation.html`](animation.html) in a browser and play it
through once. It has a **Narration** button: leave it off if you want to
talk over the animation yourself, or switch it on to let it explain each
step in its own voice.

**The one point that must land:**

> `CheckoutService` cannot behave differently depending on which rule it
> holds, because there is no message it can send to find out which one it
> is. If you ever need `instanceof` there, the pattern has not been
> applied.

## 0:25–0:40 — Code Walkthrough

Open the files in this order. Resist jumping ahead.

**1. The strategy — `ShippingCostRule.java`**
Two methods. Ask: *"Why is `name()` on here at all?"* Because otherwise the
client needs a map from rule to display name — and that map is the `switch`
growing back somewhere new.

**2. The parameter object — `Shipment.java`**
Point out that `FlatRateRule` reads none of these fields. Ask: *"Isn't that
wasteful?"* No — it is what keeps the interface stable. If `costFor` took
just a weight, adding the distance rule would change every implementation.

**3. Two concrete strategies — `FlatRateRule.java`, then `WeightBandedRule.java`**
The first ignores everything; the second has a band table. Ask: *"What do
these two have in common?"* Only the interface. That is the point — they
are peers, not variations on each other.

**4. The context — `CheckoutService.java`**
This is the heart of the session. Search the file live, on screen, for the
words "flat", "weight" and "distance". Zero hits. Say out loud: *the switch
did not move, it is gone.*

**5. The honest bit — `ShippingRules.java`**
Somebody will say "you just moved the switch". Agree, then draw the
distinction: the naive branch ran inside the pricing logic on every quote;
this runs once, at the edge, answering "which rule is configured today". In
production it is a database row, not code.

**6. The trap — `NaiveCheckoutService.java`**
Back to it with fresh eyes now the alternative exists. Ask which version
they would rather add a fifth rule to.

**7. The proof — `CheckoutServiceTest.java`**
Show `acceptsARuleDefinedEntirelyInThisTest`. Ask: *"Could this test exist
against the naive design?"* No — and note that the arithmetic tests
*could*, which is why they prove nothing about the pattern.

**8. Run it — `ShippingCostDemo.java`**
Run `./gradlew run` live. Read down the "campaign" column and across the
Cardiff row.

## 0:40–0:50 — Exercises

Let participants work; circulate and help.

### Exercise 1 — Add a fifth rule (everyone)

Add a `LockerCollectionRule`: free when the destination contains "Locker",
£3.00 otherwise. Register it in `ShippingRules` under `"locker"`. Then
count the files you had to open.

> **The payoff:** one new class and one registry line. `CheckoutService`,
> and all four existing rules, were not touched. Say this out loud when
> someone finishes.

### Exercise 2 — Do the same thing to the naive version (everyone)

Add `LOCKER_COLLECTION` to `ShippingMethod` — *and do not touch
`NaiveCheckoutService`*. Run it. Watch the shop ship for free. Then fix it
properly and compare the diff to Exercise 1's.

### Exercise 3 — Break the abstraction on purpose (discussion)

Add a `getRule()` accessor to `CheckoutService`, and have the demo write
`if (checkout.getRule() instanceof FreeOverThresholdRule) { ... }`.
Discuss: *"What did we just throw away?"* Every reason the four rules were
separated. Client code can now branch on rule type again, and the fifth
rule will break it.

### Exercise 4 — Stretch (for fast finishers)

Rewrite `FlatRateRule` as a lambda at the call site. It works — Strategy
with a single-method interface is just a function. Then ask what
`checkout.ruleName()` prints, and what you would have to give up or add
back to fix it.

## 0:50–0:58 — Pitfalls & Comparisons

Cover the "What to Watch Out For" section:

- Strategies must not carry state between calls; the registry hands out
  shared instances, so a rule that remembers the last shipment is a
  concurrency bug waiting for traffic.
- The client must never ask what it is holding — `instanceof` is the branch
  returning.
- The interface must not grow a method per rule. New data goes on
  `Shipment`.
- Four classes instead of one method is a genuine cost. For two rules that
  will never change, the `switch` is the better answer.

Then the comparison table. The line worth memorising:

> **Strategy and State have the same shape. The difference is who chooses
> and how often: Strategy's choice comes from outside and stays put; a
> State object swaps itself for another as events arrive.**

Close with real-world sightings: `Comparator`, `RejectedExecutionHandler`,
Spring's `PasswordEncoder`, and cache eviction policies.

## 0:58–1:00 — Wrap-Up

Ask three people for a one-sentence definition. Then assign follow-up:

> Find one `switch` or `if/else` chain in your own codebase that branches
> on a "type" or "mode" field and does real work in each branch — tax
> calculation, export format, and retry policy are common ones — and sketch
> what the strategy interface would be called.

## Facilitator Notes

**Common misconceptions to correct:**

| They say | Correct with |
| --- | --- |
| "You just moved the switch into `ShippingRules`" | Half right, and worth taking seriously. The naive branch ran inside the pricing logic on every quote, tangling decision with arithmetic. The registry runs once, at the edge, and answers a different question. In production it is a config table, not code |
| "Isn't this just polymorphism?" | Yes — Strategy *is* polymorphism, applied deliberately to a family of interchangeable algorithms. The pattern is the naming and the discipline, not a new language feature |
| "Isn't this the same as State?" | Same shape, different question. Strategy's rule is handed in from outside and does not change itself; a State object decides what replaces it. Cover this properly in the State project |
| "Four classes for four `if`s seems like a lot" | Agree. For two rules that never change, it is. The pattern pays when the family is open-ended — and delivery pricing genuinely is, because marketing owns it |
| "Why not a `Map<ShippingMethod, Supplier<Money>>`?" | That *is* the pattern, with the interface replaced by a functional type. Ask them where `name()` went |

**If you are running short on time:** cut Exercise 4 and shorten the
pitfalls discussion. Never cut Exercise 2 — watching the naive version ship
for free is the single most persuasive minute in the session.

**If you have extra time:** have participants write a full test class for
their `LockerCollectionRule`, mirroring the `@Nested` structure of
`ShippingCostRuleTest`, and add it to the interchangeability loop in
`CheckoutServiceTest` (it will pass with no changes — that is the point).

## Materials Checklist

- [ ] Everyone has JDK 21 and a green `./gradlew run`
- [ ] Diagrams open in a tab (`images/`)
- [ ] `animation.html` open in a browser
- [ ] Video on hand (`../video/strategy-pattern-explained.mp4`) — useful as
      a recap for anyone who joins late, or to send round afterwards
- [ ] `NaiveCheckoutService` open in a second window, so you can put it
      beside `CheckoutService` at the 0:25 mark
- [ ] The printed four-rule table from `./gradlew run` ready to put on the
      board
- [ ] IDE font size raised for screen sharing
