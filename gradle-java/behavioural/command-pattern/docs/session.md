# Session Guide — Command Pattern

A 60-minute guided session for teaching or self-studying the Command pattern
using this project.

- **Audience:** beginners comfortable with core Java
- **Duration:** ~60 minutes
- **Format:** live coding + discussion
- **Prerequisites:** see [`prerequisites.md`](prerequisites.md)

> **Optional pre-work.** Ask participants to watch the video
> (`video/command-pattern-explained.mp4`) beforehand. If they do, you can
> compress the problem and pattern segments and spend the extra time on the
> exercises. If you are teaching a group that has *not* watched it, run the
> session exactly as written below.

## Learning Objectives

By the end of this session a participant should be able to:

1. Say why undo cannot be built out of method calls.
2. Explain why `previousQuantity` is set in `execute` and not in the
   constructor, and what breaks if you move it.
3. Identify the roles — command, concrete command, receiver, invoker — in
   real code.
4. State honestly what the pattern costs, starting with the fact that every
   operation becomes a class and every inverse is yours to get right.
5. Distinguish Command from Memento, and from Strategy.

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

**Do not show `CartCommand` yet.** Start with the pain.

Open `NaiveCartEditor` and put `addItem` and `undo` on the screen together.
Read them out. Then ask:

> *"This is fifteen lines and it obviously works. Convince me it's wrong."*

Let them try. Most groups go straight to "the switch will grow", which is
true and is the *weaker* argument. Steer to the strong one by asking:

> *"What does the note say? And what does undo actually need to know?"*

Land it: **the note records the request; undo needs the state.** Then run
section 1 of the demo live. Three headphones on screen, then an empty cart.
Nobody argues after that.

Follow with the coupon case, which is the same mistake wearing a different
hat: applying `BLACKFRIDAY` over `WELCOME10` *replaced* something, and
clearing on undo takes away a discount the customer never touched.

This is the moment the session turns: it converts "the code will get messy"
into "the customer is charged the wrong amount".

## 0:16–0:26 — The Pattern

Use the order-slip analogy from
[`command-pattern-explained.md`](command-pattern-explained.md). Ask: *"Why
does a waiter write a slip instead of just remembering?"* Land on: a slip can
be stacked, read back, passed to someone else, and torn up. Spoken words
cannot.

Then the one-liner that makes it click:

> *"A method call is an event. It happens and it's gone. You can't put it in
> a list, and you can't ask it what it did."*

Show the class diagram ([`images/class-diagram.png`](images/class-diagram.png))
and name the roles. Point out the two directions of ignorance: `Cart` has
never heard of a command, and `CartHistory` has never heard of a coupon.

Then show the sequence diagram
([`images/uml-diagram.png`](images/uml-diagram.png)) and go straight to steps
10–12. That capture is the whole pattern; the rest is bookkeeping.

Optionally open [`animation.html`](animation.html) and play it through once.
It has a **Narration** button: leave it off if you want to talk over it, or
switch it on to let it explain each step in its own voice.

**The one point that must land:**

> A command records what it needs to reverse itself *during* `execute`, by
> asking the receiver. Not in the constructor — that is a guess about a cart
> you have not reached yet.

## 0:26–0:41 — Code Walkthrough

Open the files in this order. Resist jumping ahead.

**1. The command — `CartCommand.java`**
Three methods. Ask: *"Which one is hard?"* Everyone says `undo`, and they are
right. Read the three rules in the Javadoc out loud; they are the whole
session in twelve lines.

**2. The interesting one — `AddItemCommand.java`**
Put the two branches of `undo` on screen and ask which one runs. The answer
is "it depends what the cart had", and *that* is why there is a field the
constructor does not set. Spend real time here.

**3. The one about position — `RemoveItemCommand.java`**
Ask: *"What does undo have to restore?"* Wait for someone to say "the line".
Then ask where it goes. Show `undoRestoresThePosition`.

**4. The one that is usually a no-op — `ApplyCouponCommand.java`**
`previousCoupon` is null nine times in ten. Ask what happens the tenth time
if you write `cart.setCoupon(null)` instead.

**5. The invoker — `CartHistory.java`**
Search the file live, on screen, for "coupon", then "quantity", then "sku".
Zero hits each time. Say it out loud: *the thing that runs the edits does not
know what any of them are.*

Then read `execute` and name the two decisions: `undone.clear()`, and the
fact that a throwing command is never pushed.

**6. The trap, revisited — `NaiveCartEditor.java`**
Back to it with fresh eyes now the alternative exists. Read the two comments
on the `switch` arms out loud.

**7. The proof — `CartHistoryTest.anUnknownCommandWorksUnchanged`**
Gift wrapping, declared inside the test. Ask: *"Could this test exist against
the naive editor?"*

**8. Run it — `CartCommandsDemo`**
Compare section 1 and section 4 on screen: the same two edits, two different
answers.

## 0:41–0:51 — Exercises

Let participants work; circulate and help.

### Exercise 1 — Add a fifth kind of edit (everyone)

Write a `ClearCartCommand` that empties the cart, and make its undo put every
line back **in order**. Attach it in the demo.

> **The payoff:** one new class and no edit to `Cart` or `CartHistory`. Say
> this out loud when someone finishes.

### Exercise 2 — Do the same thing to the naive version (everyone)

Add clearing to `NaiveCartEditor`. You need a new field on `Change` that
every other kind of edit will carry as null, a new case in the `switch`, and
a decision about what the note should hold. Compare that diff to Exercise 1's.

**Never cut this exercise.** The shape of the diff is the argument.

### Exercise 3 — Break undo on purpose (discussion)

Move `previousQuantity = cart.quantityOf(sku)` out of `execute` and into the
constructor of `AddItemCommand`. Run the suite. Exactly one test goes red —
the one that adds, undoes, and adds again. Discuss *why* that is the test
that catches it.

### Exercise 4 — Stretch (for fast finishers)

Give `CartHistory` an `undoAll()`, then write the test that proves a cart
which has had every kind of edit applied to it ends up exactly as it started.

## 0:51–0:58 — Costs & Comparisons

Be honest here; it is what makes the session credible.

- **Every operation becomes a class.** For four edits that will never change,
  `NaiveCartEditor` is a third of the code and it works. Command pays when
  undo, logging or queuing is a requirement.
- **The inverse is yours to get right.** The pattern gives you a place to put
  `undo`; nothing checks that yours is correct. Every command needs a test
  that executes *and then undoes* against a cart that was not empty.
- **Ordering is a contract.** Undo must be called on the state the command
  left behind. That is `CartHistory`'s job, and calling `undo` by hand out of
  order is undefined.
- **Not everything should be a command.** Reads should not be — nothing to
  undo, nothing to log.

Then the comparison. The line worth memorising:

> **Command stores the difference and needs each edit to know its inverse.
> Memento stores the state and needs no inverses at all — at the cost of a
> copy per step and no record of what changed.**

Finish by naming where they have already used it: `Runnable` and every
`ExecutorService`, `javax.swing.undo`, database migrations with `up()` and
`down()`, and event sourcing, where the log of commands *is* the system of
record.

## 0:58–1:00 — Wrap-Up

Ask three people for a one-sentence definition. Then assign follow-up:

> Find one feature in your own product that a user would expect to be able to
> take back. Ask what its inverse is. If you cannot state the inverse in a
> sentence, that is the real work — the pattern is the easy half.

## Facilitator Notes

**Common misconceptions to correct:**

| They say | Correct with |
| --- | --- |
| "Isn't this just a lambda?" | For `execute` alone, yes — `Runnable` is a command. Undo needs state that survives between two calls, which is what makes it an object rather than a function |
| "Can't I just snapshot the cart?" | You can, and it is a real pattern — Memento. It costs a full copy per edit and gives you no record of what changed. Both are valid; know which you are choosing |
| "Why not put `undo` on the Cart?" | Then the cart has to know what was done to it, and you are back to a `switch` over kinds of edit — the naive version with extra steps |
| "Should `execute` be idempotent?" | No, and do not try. `execute` is expected to run once per push; redo re-runs it deliberately, after an undo has put the cart back |
| "Why does a failed command not go on the stack?" | Because undoing a half-applied edit applies the reverse of something that never fully happened. Show `aFailedCommandIsNotRecorded` |
| "Four classes for four edits seems like a lot" | Agree. It is. The trade is that the fifth costs one class and the naive version's fifth costs a field, a case and a re-test of the other four |

**If you are running short on time:** cut Exercise 4 and shorten the costs
discussion. Never cut Exercise 2.

**If you have extra time:** have participants write the `@Nested` test class
for their `ClearCartCommand`, mirroring `CartCommandTest`, and confirm that
nothing outside their new files had to change.

## Materials Checklist

- [ ] Everyone has JDK 21 and a green `./gradlew run`
- [ ] Diagrams open in a tab (`images/`)
- [ ] `animation.html` open in a browser
- [ ] Video on hand (`../video/command-pattern-explained.mp4`) — useful as a
      recap for anyone who joins late, or to send round afterwards
- [ ] `NaiveCartEditor` open in a second window, so you can put it beside
      `AddItemCommand` at the 0:26 mark
- [ ] The demo's section 1 and section 4 output ready to show side by side
- [ ] IDE font size raised for screen sharing
