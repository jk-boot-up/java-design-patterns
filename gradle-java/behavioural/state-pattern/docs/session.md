# Session Guide — State Pattern

A 60-minute guided session for teaching or self-studying the State pattern
using this project.

- **Audience:** beginners comfortable with core Java
- **Duration:** ~60 minutes
- **Format:** live coding + discussion
- **Prerequisites:** see [`prerequisites.md`](prerequisites.md)

> **Optional pre-work.** Ask participants to watch the video
> (`video/state-pattern-explained.mp4`) beforehand. If they do, you can
> compress the problem and pattern segments and spend the extra time on the
> exercises. If you are teaching a group that has *not* watched it, run the
> session exactly as written below.

## Learning Objectives

By the end of this session a participant should be able to:

1. Explain why a status field plus one conditional per method drifts, and why
   extracting a shared `checkStatus` helper does not fix it.
2. Say what "refusal by default" buys, and describe the failure mode it
   replaces.
3. Point at a place where two states do genuinely different work for the same
   verb, and say why that is the test for whether this pattern is warranted.
4. Distinguish State from Strategy without appealing to the class diagram,
   because the diagram is the same.
5. State honestly what the pattern costs, starting with the transition table
   that no longer exists anywhere readable.

## Timetable

| Time | Segment | Mode |
| --- | --- | --- |
| 0:00–0:05 | Setup check | Hands-on |
| 0:05–0:16 | The problem | Discussion |
| 0:16–0:26 | The pattern | Explanation |
| 0:26–0:41 | Code walkthrough | Live coding |
| 0:41–0:51 | Exercises | Hands-on |
| 0:51–0:58 | Costs & comparisons | Discussion |
| 0:58–1:00 | Wrap-up | — |

## 0:00–0:05 — Setup Check

Everyone runs:

```bash
java -version
./gradlew run
```

Anyone whose build fails pairs up with a neighbour. Do not debug installs
during the session — that is what the prerequisites doc is for.

## 0:05–0:16 — The Problem

Open `NaiveOrder.java` and put the lifecycle on the board:

```
PLACED -> PAID -> PACKED -> SHIPPED -> DELIVERED     (+ CANCELLED, REFUNDED)
```

**Do not** start by saying the conditionals are bad. Start by asking the room
to answer one question from the code:

> What can a `SHIPPED` order do?

Let them look. The honest answer is that you have to read all six methods and
do the boolean algebra yourself, because the lifecycle is not written down
anywhere — it exists only as the intersection of six guards.

Then read `cancel` and `refund` side by side and let somebody notice that one
is a blocklist and the other an allowlist. Both are correct-looking. Neither is
correct.

Run section 1 of the demo and let the ledger land:

```
buttons drawn   : [deliver]
cancel() anyway : accepted — status is now CANCELLED
the shop is out : -£97.49 over 2 refunds
```

**The question to sit on for a full minute:** the screen is right. The switch
in `allowedActions()` says a shipped order can only be delivered. So who is
this bug reachable by? (Answers: retries, scripts, integrations, support
tools, the mobile client, next year's endpoint. Everybody except the person
clicking the button.)

**Anticipate the objection**, because somebody will make it: *"just extract a
`canCancel()` helper"*. That is the right instinct and it fixes the immediate
duplication. Ask what happens next: `cancel` still needs three different
bodies for `PLACED`, `PAID` and `PACKED`, so you now have a shared guard and a
switch underneath it, and the two can drift apart from each other. Park it —
it comes back at 0:51.

## 0:16–0:26 — The Pattern

Give the definition, then throw away the first half of it: *the object will
appear to change its class.* Ask what that would mean literally. A `SHIPPED`
order and a `PLACED` order are the same instance; if they were different
classes, they would accept different messages.

Use the vending machine analogy from the video. The part worth labouring is
the last bit — nobody sets the machine's condition from outside; it got there
because a coin went in.

Draw the class diagram on the board **without names**, then say: this is also
the Strategy diagram. Do not resolve it yet. Tell them you will come back to
it at 0:51, and that anyone who solves it before then should say so.

## 0:26–0:41 — Code Walkthrough

Order matters here. Do it in this sequence:

1. **`OrderState.java` first, and slowly.** Six methods, six bodies, every one
   throws. Ask: what does a state have to write in order to forbid something?
   (Nothing.) Then: what is the failure mode when a developer forgets a rule
   in each version? In the enum, forgetting opens a transition. Here,
   forgetting closes one. That single asymmetry is the reason for the project.

2. **`Order.java`.** Read `attempt` out loud. Note there is no conditional in
   the file that mentions a status, and that `transitionTo` is
   package-private — from outside, a state can only change as a consequence of
   asking the order to do something.

3. **The three `cancel` methods**, opened side by side: `PlacedState`,
   `PaidState`, `PackedState`. Three different bodies for one word. This is the
   slide that decides whether the pattern was warranted; if these had all been
   the same body behind a different guard, the enum was the right answer.

4. **`ShippedState.cancel`.** Ask why it overrides at all, given the default
   already refuses. (To give a human a reason worth reading.)

5. **`CancelledState`.** Show that it is nine lines and overrides nothing.
   Then ask where the rule "you cannot refund a cancelled order twice" is
   written. It is not. That is the point.

6. **`OrderStateDemo.theButtons()`.** The anonymous `AT-LOCKER` state, and
   `Order` — compiled without it — accepting it.

## 0:41–0:51 — Exercises

### Exercise 1 — Add `RETURN_REQUESTED` (everyone)

Between `DELIVERED` and `REFUNDED`. A delivered order can request a return; a
return-requested order can be refunded or cancelled back to delivered.

Have them **count the files they had to open**: the new class, and
`DeliveredState`. Then have them do the same change to `NaiveOrder` and count
again. The shape of those two diffs is the entire argument.

### Exercise 2 — Break it on purpose (everyone)

Delete `ShippedState.cancel` entirely. Run the tests.

The `cannotBeCancelled` test still passes — because the inherited default
refuses. Ask what *did* change (the message a support agent reads), and what
that tells them about which overrides are behaviour and which are ergonomics.

### Exercise 3 — Try to reach the naive bug (discussion)

Ask them to write a line of code, anywhere, that gets an `Order` from
`SHIPPED` to `CANCELLED`. They cannot without adding a method to
`ShippedState`. Ask what the equivalent of "cannot" is in `NaiveOrder`.

### Exercise 4 — Stretch (for fast finishers)

Make the states stateful: give `ShippedState` a courier name passed to its
constructor. Notice what has to go: the shared `INSTANCE`, `assertSame` in
`OrderLifecycleTest`, and the assumption that a state is free to allocate.

## 0:51–0:58 — Costs & Comparisons

Resolve the diagram question first, and make somebody else say it if you can:

> A Strategy is chosen by the caller and does not change itself. A State is
> entered as a consequence of what the object did, and states hand control to
> one another.

Point at `PaidState.pack` ending with `transitionTo(PackedState.INSTANCE, …)`.
A state names its successors. A strategy never names another strategy.

Then the bill, honestly:

- Seven classes where there was one enum.
- **The transition table is gone.** In `NaiveOrder` you could read the whole
  lifecycle in one `switch`. Now it is one arrow per file. Ask whether the
  `stateDiagram` in [`uml-diagram.md`](uml-diagram.md) is documentation or a
  second source of truth that can drift — there is no comfortable answer.
- Persistence stores `"PACKED"`, not an object, so something has to map names
  back to states and that map is a place a new state gets forgotten.
- Now return to the parked `canCancel()` helper. It is genuinely the right
  answer for a machine where every state's version of a method is the same
  body behind a different guard. Say so plainly: reaching for State every time
  you see a status field is the same mistake in the other direction.

## 0:58–1:00 — Wrap-Up

One sentence each, round the room: *when would you not use this?*

Good answers mention a small, stable machine; states that differ only in
permissions; a lifecycle that has to be readable in one place by non-authors;
and anything that has to be serialised across a version boundary.

Point at [`animation.html`](animation.html) and the video for revision, and at
[`state-pattern-explained.md`](state-pattern-explained.md) for the written
version of everything above.

## Facilitator Notes

- **The best single moment in this session** is the gap between "the screen is
  right" and "the endpoint takes the call anyway". Do not rush it. Almost
  everyone has shipped that bug.
- **Expect scepticism at seven classes**, and welcome it. The project agrees.
  The counter is not "classes are cheap", it is the three `cancel` bodies.
- **If somebody says "just use an enum with a permitted-transitions map"**,
  they are right and you should say so out loud, then ask what happens to
  `PackedState`'s stock return in that design.
- **Watch for the Strategy confusion resurfacing** at exercise 4. Someone
  usually asks why states are singletons if strategies often are too. The
  answer is that it is a coincidence of this domain, not a property of either
  pattern.
- **If you are short on time**, cut exercise 4 and the persistence bullet.
  Never cut the comparison at 0:51 — it is the reason this pattern is
  misunderstood.

## Materials Checklist

- [ ] Java 21 and the Gradle wrapper working for every participant
- [ ] `./gradlew run` output on screen, or printed
- [ ] `docs/images/class-diagram.png` and `docs/images/state-machine.png`
      visible side by side
- [ ] `docs/animation.html` open in a browser tab
- [ ] A whiteboard, for the unnamed class diagram at 0:16
