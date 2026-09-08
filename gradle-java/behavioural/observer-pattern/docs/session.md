# Session Guide — Observer Pattern

A 60-minute guided session for teaching or self-studying the Observer
pattern using this project.

- **Audience:** beginners comfortable with core Java
- **Duration:** ~60 minutes
- **Format:** live coding + discussion
- **Prerequisites:** see [`prerequisites.md`](prerequisites.md)

> **Optional pre-work.** Ask participants to watch the video
> (`video/observer-pattern-explained.mp4`) beforehand. If they do, you can
> compress the problem and pattern segments and spend the extra time on the
> exercises. If you are teaching a group that has *not* watched it, run the
> session exactly as written below.

## Learning Objectives

By the end of this session a participant should be able to:

1. Describe, in one sentence, what problem the Observer pattern solves.
2. Explain why `Order` has no field called `email`, and what that buys.
3. Identify the roles — subject, observer, concrete observer, event — in
   real code.
4. State honestly what the pattern costs, starting with the fact that
   reading `moveTo` no longer tells you what happens.
5. Distinguish Observer from Mediator, and from Strategy.

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

**Do not show `OrderListener` yet.** Start with the pain.

Open `NaiveOrderService` and put `markShipped` on the screen. Four lines.
Read them out. Then ask:

> *"This is four lines long and you can see everything it does. Convince me
> it's bad."*

Let the group struggle for a moment — they should, because for four lines
this really is a good program. Steer towards, in this order:

1. A fifth reaction edits this method, and everything that depended on it
   gets re-tested.
2. You cannot test the shipping transition without stubbing all four.
3. Analytics wants *every* transition, which means every status-changing
   method must remember to call it.

**Then point at the second line and ask the question that turns the
session:**

> *"Email talks to a network. What happens on the day the mail server times
> out?"*

Walk it through out loud: the order is already marked shipped. Inventory has
already released the stock. Analytics never runs. **The warehouse feed is
never written, so nobody picks the parcel.** The caller gets an exception
that says `SMTP timeout` and says nothing at all about the parcel.

Now run the demo's first section live, or show
`NaiveOrderServiceTest.oneFailureTakesTheRestDown`. Seeing
`warehouse feed : []` on screen lands harder than describing it.

This is the moment the session turns: it converts "a bit tangled" into "an
incident that passes code review".

## 0:16–0:26 — The Pattern

Use the newsletter analogy from
[`observer-pattern-explained.md`](observer-pattern-explained.md). Ask: *"When
a shop sends its newsletter, how much does it know about what you do with
it?"* Land on: nothing — and that is why a thousand new subscribers need no
new code.

Push it one step further, because this is the half people forget:

> *"And who owns the relationship? You do. You can unsubscribe without
> asking the shop's permission."*

Show the class diagram ([`images/class-diagram.png`](images/class-diagram.png))
and name the roles. Point out that **there is no arrow between the four
listeners** — that absence is the design.

Then show the sequence diagram
([`images/uml-diagram.png`](images/uml-diagram.png)) and go straight to the
red block. Step 20 is the exception; steps 21 to 24 are the ones that would
not have happened.

Optionally open [`animation.html`](animation.html) in a browser and play it
through once. It has a **Narration** button: leave it off if you want to talk
over it yourself, or switch it on to let it explain each step in its own
voice.

**The one point that must land:**

> `Order` cannot behave differently depending on who is listening, because
> there is no message it can send to find out. That is why the thousandth
> listener costs nothing.

## 0:26–0:41 — Code Walkthrough

Open the files in this order. Resist jumping ahead.

**1. The observer — `OrderListener.java`**
Two methods. Ask: *"What is deliberately missing?"* No priority, no ordering
hint, no `shouldHandle` predicate. Every one of those would let a listener
make claims about the other listeners.

Then ask why `name()` exists at all, given nothing dispatches on it. Because
a stack trace from inside a listener list is otherwise anonymous — and this
is exactly the code where a stack trace is all you get.

**2. The event — `OrderEvent.java`**
A record with three fields and **no reference back to the `Order`**. Ask:
*"Why not just pass the order?"* Because then a listener can change the
subject halfway through a notification, and whether listener three sees the
old value depends on registration order. Name the GoF terms: push and pull.

**3. The subject — `Order.java`**
The heart of the session. Search the file live, on screen, for "email", then
"inventory", then "warehouse". Zero hits each time. Say it out loud: *the
list of reactions is not in the class that causes them.*

Then read `moveTo` line by line and name the three decisions:

- the no-op guard (or every listener defends itself against duplicates, and
  the one that forgets sends a second shipping email);
- `status = next` **before** the loop;
- the `try`/`catch` inside the loop, which is the fix for the outage from the
  first segment.

**4. Why `CopyOnWriteArrayList`**
Not threads — one-shot subscriptions. Show
`OrderTest.selfRemovalDuringNotification`. Offer to change the field to
`ArrayList` live and watch it throw `ConcurrentModificationException`; it
takes fifteen seconds and nobody forgets it.

**5. Two concrete observers — `InventoryListener.java`, then `AnalyticsListener.java`**
The first ignores most statuses by simply returning; the second wants all of
them. Ask what they have in common. Only the interface.

**6. The trap — `NaiveOrderService.java`**
Back to it with fresh eyes now the alternative exists. Read the comment on
line `email.onStatusChanged(event);` out loud.

**7. The proof — `NaiveOrderServiceTest.java`**
Show `thePatternIsolatesTheSameFailure` and
`anUnknownListenerWorksUnchanged` back to back. Ask: *"Could either test
exist against the naive design?"*

**8. Run it — `OrderEventsDemo.java`**
Run `./gradlew run` live. Compare section 1 and section 4 on screen: same
broken mail server, two different outcomes.

## 0:41–0:51 — Exercises

Let participants work; circulate and help.

### Exercise 1 — Add a fifth reaction (everyone)

Write a `SupplierListener` that prints a line only when an order becomes
`PAID`. Attach it in the demo. Then count the files you had to open.

> **The payoff:** one new class and one `addListener` call. `Order` and all
> four existing listeners were not touched. Say this out loud when someone
> finishes.

### Exercise 2 — Do the same thing to the naive version (everyone)

Add the same supplier notification to `NaiveOrderService`. You will need a
fifth field, a fifth constructor parameter, a fifth call — and every existing
test that constructs the service now fails to compile. Compare that diff to
Exercise 1's.

**Never cut this exercise.** The compile errors are the argument.

### Exercise 3 — Break the isolation on purpose (discussion)

Delete the `try`/`catch` from `Order.moveTo` and run
`NaiveOrderServiceTest.thePatternIsolatesTheSameFailure`. Watch the pattern
acquire exactly the bug the naive version had. Discuss: *the pattern did not
fix that on its own — a deliberate decision inside the loop did.*

### Exercise 4 — Stretch (for fast finishers)

Make `EmailListener` remove itself from the order after the `DELIVERED`
message. Confirm `listenerCount()` drops. Then change `Order`'s field to a
plain `ArrayList` and watch it throw.

## 0:51–0:58 — Costs & Comparisons

Be honest here; it is what makes the session credible.

- **The call graph becomes invisible.** Reading `moveTo` tells you nothing
  about what happens when an order ships. Your IDE cannot help, because
  every call site is typed as the interface. This is a real loss.
- **Debugging is harder** in the way it always is with indirection — hence
  `name()` and `ListenerFailure`.
- **Notification order is not a contract.** It happens to be registration
  order. A listener that depends on that is already broken. Two reactions
  that must be sequenced are one reaction.
- **Memory leaks are the classic failure.** A long-lived subject holding a
  short-lived listener keeps it alive forever. `removeListener` is the whole
  of the answer, and somebody has to remember to call it.

Then the comparison table. The line worth memorising:

> **Observer decouples; Mediator centralises. In Observer the publisher
> knows nothing and the subscribers know the publisher. In Mediator a hub
> knows everyone, deliberately, so it can coordinate them.**

Finish with `java.util.Observer` being deprecated since Java 9, and why: not
type-safe, `Observable` was a class you had to extend, and it promised
nothing about ordering or threads. **The pattern was never the problem; that
implementation of it was.** Then name what replaced it —
`java.util.concurrent.Flow`, Spring's `@EventListener`, and every UI toolkit
ever written.

## 0:58–1:00 — Wrap-Up

Ask three people for a one-sentence definition. Then assign follow-up:

> Find one method in your own codebase that changes a status and then calls
> three or four services by name. Ask whether those services are independent
> of each other. If they are, you have found an Observer. If the third needs
> the second's result, you have found a workflow — and that is a different
> pattern.

## Facilitator Notes

**Common misconceptions to correct:**

| They say | Correct with |
| --- | --- |
| "Isn't this just callbacks?" | Yes, and that is fine. Observer is callbacks with the list owned by the subject and the subscription owned by the subscriber. The pattern is the naming and the discipline |
| "So I should use `java.util.Observer`?" | No — deprecated since Java 9, for good reasons worth knowing. Use your own interface, `Flow`, or your framework's events |
| "Can I make the listeners run in a set order?" | You can, and the moment you do, you have two listeners that are really one workflow. Merge them instead, or move to Chain of Responsibility |
| "Isn't this the same as Mediator?" | Opposite intent. Observer's publisher knows nothing; Mediator's hub knows everyone on purpose |
| "Four classes instead of four lines seems like a lot" | Agree. For four reactions that will never change, it is. The pattern pays when the list is open-ended — and the list of people interested in an order genuinely is |
| "Why not fire the event before updating the status?" | Then a listener that looks at the order sees the world the event has already contradicted. Show the `statusIsUpdatedBeforeListenersRun` test |

**If you are running short on time:** cut Exercise 4 and shorten the costs
discussion. Never cut Exercise 2 — the compile errors are the single most
persuasive minute in the session.

**If you have extra time:** have participants write a full test class for
their `SupplierListener`, mirroring the `@Nested` structure of
`OrderListenerTest`, and then attach it to an `Order` in a test and confirm
nothing else needed changing.

## Materials Checklist

- [ ] Everyone has JDK 21 and a green `./gradlew run`
- [ ] Diagrams open in a tab (`images/`)
- [ ] `animation.html` open in a browser
- [ ] Video on hand (`../video/observer-pattern-explained.mp4`) — useful as
      a recap for anyone who joins late, or to send round afterwards
- [ ] `NaiveOrderService` open in a second window, so you can put it beside
      `Order` at the 0:26 mark
- [ ] The demo's section 1 and section 4 output ready to show side by side
- [ ] IDE font size raised for screen sharing
