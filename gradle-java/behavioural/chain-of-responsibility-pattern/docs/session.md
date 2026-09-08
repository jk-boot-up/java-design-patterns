# Session Guide — Chain of Responsibility

A 60-minute guided session for teaching or self-studying the Chain of
Responsibility pattern using this project.

- **Audience:** beginners comfortable with core Java
- **Duration:** ~60 minutes
- **Format:** live coding + discussion
- **Prerequisites:** see [`prerequisites.md`](prerequisites.md)

> **Optional pre-work.** Ask participants to watch the video
> (`video/chain-of-responsibility-pattern-explained.mp4`) beforehand. If they
> do, you can compress the problem and pattern segments and spend the extra
> time on the exercises. If you are teaching a group that has *not* watched it,
> run the session exactly as written below.

## Learning Objectives

By the end of this session a participant should be able to:

1. Explain why a sequence of `if` statements welds an ordering into a method,
   and why extracting each check into a private helper does not fix it.
2. Say what "no opinion" buys, and why `Optional.empty()` and a rejection are
   different things.
3. Point at the links that were **not** consulted and say why that absence is
   the pattern rather than an implementation detail.
4. Distinguish Chain of Responsibility from Decorator by asking one question,
   without appealing to the class diagram, because the diagram is the same.
5. State honestly what the pattern costs, starting with the fact that the
   policy is no longer readable in one place.

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

Open `NaiveScreening.validate` and put it on the screen. **Do not** start by
saying it is bad. Ask the room to read it and tell you what is wrong with it.

The honest answer is *nothing*. It is short, it is one file, and it is the
right answer for a shop with one market and fixed rules. Say that out loud
before you take it apart — the whole argument depends on the audience believing
you are being fair to it.

Then run section 1 and let this land:

```
  A monitor, on a £250 card, scoring 92 out of 100 for fraud:
    naive says      : REJECTED — card limit exceeded, please try another card
```

**The question to sit on for a full minute:** what does the customer do next?
(They try another card. It works. The order ships.) And what did the fraud team
receive? (Nothing. The method returned two lines before it got there.)

Then the trade copy, side by side with `validate`, and ask the room to find the
missing check before you tell them. Somebody usually finds it in about twenty
seconds — which is the point. It was *findable* and nobody was looking, because
nothing in the code relates the two methods.

**Anticipate the objection**, because somebody will make it: *"extract each
check into a private method"*. That is the right instinct and it does help
readability. Ask what happens next: the *order* is still four call sites in one
method, the trade variant is still a second method, and the fraud check is
still only reachable by satisfying the three above it. Park it — it comes back
at 0:51.

## 0:16–0:26 — The Pattern

Use the expenses-approval analogy from
[the explainer](chain-of-responsibility-pattern-explained.md): you submit once,
whoever can approve it approves it, and the hierarchy is not in the claim form.
Then push on the third part — a claim nobody is authorised to approve sits in a
queue forever and nobody is told. Ask the room what the software equivalent is.
That is the fallback the chain's constructor insists on, and it is worth them
predicting it before they see it.

Draw the class diagram on the board **without names**: an abstract class, a
`next` field of its own type, four subclasses. Then say: this is also the
Decorator diagram. Do not resolve it yet. Tell them you will come back to it at
0:51, and that anyone who solves it before then should say so.

## 0:26–0:41 — Code Walkthrough

Order matters here. Do it in this sequence:

1. **`ScreeningHandler.java` first, and slowly.** It is about twenty lines and
   the whole pattern is in `screen`. Ask why `screen` is `final`. (Because the
   textbook version has every handler write its own `else next.handle(...)`,
   and the bug everybody hits is the missing `else` — the request vanishes with
   no error.)

2. **`check`'s return type.** `Optional<Decision>`. Ask what empty means.
   (No opinion.) Then ask what a rejection means. (An answer.) Make sure
   somebody says out loud that those are different, because half the confusion
   about this pattern is people reading "returns nothing" as "says no".

3. **`ScreeningChain`.** Note there is no loop, no index, and no count. Then
   note that the constructor takes a fallback and there is no constructor
   without one, and ask why somebody went to that trouble.

4. **Two `check` methods**, opened side by side: `AddressCheck` and
   `FraudScoreCheck`. The second one is the slide that changes people's mental
   model — it has three answers where the first has two, and the base class
   knows about none of them.

5. **`ScreeningReport.neverRan`.** Run section 2 and read the `never ran:`
   line out. Ask what that costs in a system where the risk model is a paid API
   call.

6. **`ScreeningChainTest.linksBehindTheDecisionNeverRun`.** Ask which of the
   tests in this project would still pass against `NaiveScreening`. (The
   outcome ones. Not this one.)

## 0:41–0:51 — Exercises

### Exercise 1 — Add a velocity check (everyone)

Reject when a customer has placed more than three orders in the last hour. They
will need a field on `CheckoutRequest` and one new class.

Have them **count the files they had to open**: the request record, the new
class, and the wiring. Then have them add the same rule to `NaiveScreening` —
in both methods — and count again.

### Exercise 2 — Move a link and watch the answer change (everyone)

Take the standard chain and move `PaymentLimitCheck` above `FraudScoreCheck`.
Run the demo.

`ScreeningChainTest.reorderingChangesTheAnswer` already does exactly this and
asserts the naive answer comes back, and section 3 of the demo prints it. Have
them find that test afterwards. The
point to make: the naive behaviour was not wrong, it was *a configuration you
could not change without editing code*.

### Exercise 3 — Reuse one link in two chains (discussion, then code)

Ask them to put the *same* `AddressCheck` instance into two chains. Predict what
happens first, then try it.

The second chain rewires the instance's `next` field, so the first chain now
runs the second chain's links, and nothing complains. Ask what the alternative
designs are — a chain that builds its own links, or a stateless handler with the
successor passed in as an argument — and what each of those costs.

### Exercise 4 — Stretch (for fast finishers)

Turn the chain into a collector: report *every* problem with a request instead
of the first. Notice what has to go: the early return, the `neverRan` list,
and the entire skipping-work argument. Then ask whether the result is still
Chain of Responsibility. (It is not. It is a list and a loop, and that is fine.)

## 0:51–0:58 — Costs & Comparisons

Resolve the diagram question first, and make somebody else say it if you can:

> Does every layer have to run? If yes, it is a Decorator, and a layer that
> did not delegate would be a bug. If no, it is a chain, and a layer that
> always delegated would be pointless.

Point at the `if` in `ScreeningHandler.screen`. In a decorator, the call to
`next` is not inside a conditional. That is the whole structural difference, and
it is one character deep.

Then the bill, honestly:

- Four check classes, a base class, a chain and a wiring line where there was
  one method.
- **The policy is no longer readable in one place.** `validate` could be read
  top to bottom. Ask whether `ScreeningChain.toString()` is documentation or a
  second source of truth — there is no comfortable answer.
- **`ScreeningReport` exists only because the pattern needs explaining.** Four
  `if`s never needed a record of which of them ran. Count that as a cost, not a
  feature.
- A link instance belongs to one chain, because it holds its own successor.
- Now return to the parked "extract private methods" suggestion. It is
  genuinely the right answer when the checks and their order never change. Say
  so plainly: reaching for a chain every time you see three `if`s in a row is
  the same mistake in the other direction, and the closing lines of the demo
  say so in the program's own output.

## 0:58–1:00 — Wrap-Up

One sentence each, round the room: *when would you not use this?*

Good answers mention a fixed set of checks; a requirement to report every
problem rather than the first; genuine data dependencies between the checks,
where B only makes sense after A has produced something; and two checks, where
the machinery costs more than it saves.

Point at [`animation.html`](animation.html) and the video for revision, and at
[`chain-of-responsibility-pattern-explained.md`](chain-of-responsibility-pattern-explained.md)
for the written version of everything above.

## Facilitator Notes

- **The best single moment in this session** is the gap between "REJECTED —
  card limit exceeded" and "so they used another card". Do not rush it. Almost
  everyone has shipped that bug, and almost nobody has thought of it as an
  ordering problem.
- **Be genuinely fair to `validate` at 0:05.** If the room thinks you are
  attacking a straw man, nothing after 0:16 lands.
- **Expect the `List<Check>` and a `for` loop suggestion**, probably around
  0:26. It is a good suggestion and [`prerequisites.md`](prerequisites.md)
  agrees with it. The honest answer is that the loop is fine here and the linked
  version earns its keep when a handler needs a say in where the request goes
  next.
- **Watch for "returns nothing means no"** in exercise 1. Someone will write a
  `check` that returns a rejection for the case it does not care about.
- **If you are short on time**, cut exercise 4 and the single-use-instance
  bullet. Never cut the Decorator comparison at 0:51 — it is the reason this
  pattern gets misapplied.

## Materials Checklist

- [ ] Java 21 and the Gradle wrapper working for every participant
- [ ] `./gradlew run` output on screen, or printed
- [ ] `docs/images/class-diagram.png` and `docs/images/screening-flow.png`
      visible side by side
- [ ] `docs/animation.html` open in a browser tab
- [ ] A whiteboard, for the unnamed class diagram at 0:16
