# Session Guide — Template Method Pattern

A 60-minute guided session for teaching or self-studying the Template Method
pattern using this project.

- **Audience:** beginners comfortable with core Java
- **Duration:** ~60 minutes
- **Format:** live coding + discussion
- **Prerequisites:** see [`prerequisites.md`](prerequisites.md)

> **Optional pre-work.** Ask participants to watch the video
> (`video/template-method-pattern-explained.mp4`) beforehand. If they do, you
> can compress the problem and pattern segments and spend the extra time on
> the exercises. If you are teaching a group that has *not* watched it, run
> the session exactly as written below.

## Learning Objectives

By the end of this session a participant should be able to:

1. Say why three hand-written copies of a sequence drift, and why extracting
   helper methods does not fix it.
2. Explain what `final` on the template method actually buys, and point at a
   line of code that depends on it.
3. Choose between an abstract step, a step with a default, and a hook — and
   justify the choice.
4. State honestly what the pattern costs, starting with the fact that it
   spends the subclass's one inheritance slot.
5. Distinguish Template Method from Factory Method, and from Strategy.

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

**Do not show `FulfilmentProcess` yet.** Start with the pain.

Open `NaiveFulfilment` and put all three methods on the screen at once —
scroll so the shape of them is visible even if the text is not. Then ask:

> *"Three copies of six steps. What's wrong with this?"*

Every group says "duplication". That is true and it is the *weaker* argument;
a competent developer can live with three short duplicated methods for years.
Steer to the strong one:

> *"Forget the bodies. What is duplicated that the compiler cannot see?"*

Land it: **the order**. It exists as a shape repeated by hand, and nothing
knows it is a shape.

Then run section 1 of the demo live. The email that says
`Key: (not dispatched)` does more work than ten minutes of argument. Follow
with the marketplace case — charged, then refused — which is the same mistake
in a different copy.

This is the moment the session turns: it converts "the code is repetitive"
into "the customer was charged and got nothing".

## 0:16–0:26 — The Pattern

Use the recipe analogy from
[`template-method-pattern-explained.md`](template-method-pattern-explained.md).
Ask: *"Which parts of a cake recipe are negotiable?"* Land on: the
ingredients are, the icing is optional, and the order is not — ice it before
you bake it and you have neither.

Then show `fulfil` and say nothing for a moment. It is seven lines and it is
the entire pattern. When someone asks about the `final`, you are ready:

> *"That word is the whole thing. Everything else here is a decision about
> what kind of hole each step should be."*

Show the class diagram ([`images/class-diagram.png`](images/class-diagram.png))
and count overrides out loud: warehouse four, marketplace six, digital seven.
The short one is the ordinary one — that is the sign the defaults were chosen
well.

Then the sequence diagram ([`images/uml-diagram.png`](images/uml-diagram.png)),
and go straight to steps 17–20, where `notifyCustomer` reads what `dispatch`
wrote. Put the naive version's identical two lines beside it.

Optionally open [`animation.html`](animation.html) and play it through once.
It has a **Narration** button: leave it off if you want to talk over it, or
switch it on to let it explain each step in its own voice.

**The one point that must land:**

> The subclass decides *how* each step behaves. It never decides *when* they
> run. That is not a convention, it is a `final` keyword.

## 0:26–0:41 — Code Walkthrough

Open the files in this order. Resist jumping ahead.

**1. The template — `FulfilmentProcess.fulfil`**
Seven lines. Ask: *"What would break if a subclass could override this?"*
Collect answers before showing them the answer in `NaiveFulfilment`.

**2. The private step — `validate`**
Ask why it is `private` rather than `protected`. Wait. Someone will say "so
you can't override it", and then ask the follow-up: *"who would want to, and
what would they write?"* The answer — `@Override protected void validate() { }`
— is why the modifier matters.

**3. The three kinds of hole**
Scroll the rest of the class slowly. Four abstract, two with defaults, two
hooks. For each one ask: *"why is this one that kind?"* This is the segment
worth spending time on; the sequence is easy, this is the design.

**4. The short route — `WarehouseFulfilment`**
Four methods. Ask what it says about packing. Nothing. Ask why that is a good
sign.

**5. The route that needs everything — `DigitalFulfilment`**
Put `dispatch` and `notifyCustomer` on screen together. Ask: *"what makes it
safe for the second one to read what the first one wrote?"*

Then point at `pack` — "nothing to pack" — and ask why it records a step at
all rather than being empty. (Because "this step had nothing to do" is a
fact, and because the reports stay comparable.)

**6. The hook that is not a question — `MarketplaceFulfilment.afterFulfilment`**
An empty method in the base class, called for everybody, used by one. Ask what
the alternative would have been.

**7. The trap, revisited — `NaiveFulfilment`**
Back to it with fresh eyes now the alternative exists. Read the two `// Drifted`
comments out loud.

**8. The proof — `FulfilmentProcessTest.RecordingRoute`**
A route that does nothing but write down that it was called. Ask: *"could
this test be written against `NaiveFulfilment`?"*

**9. Run it — `FulfilmentDemo`**
Section 2 prints three step lists side by side and they are identical. Then
section 4 adds a fourth route in the demo file itself.

## 0:41–0:51 — Exercises

Let participants work; circulate and help.

### Exercise 1 — Add a fifth route (everyone)

Write `SubscriptionRenewalFulfilment`: nothing to reserve, charge a stored
card, nothing to pack, extend the licence period on dispatch. Run it in the
demo.

> **The payoff:** ask how many methods they wrote, and whether they opened
> `FulfilmentProcess`. Say the answer out loud when someone finishes.

### Exercise 2 — Add a seventh step to both versions (everyone)

Add a fraud check between validate and reserve. Do it in `FulfilmentProcess`
first — one line, plus one abstract or default method. Then do the same to
`NaiveFulfilment` and count the edits and the chances of missing one.

**Never cut this exercise.** The shape of the diff is the argument.

### Exercise 3 — Try to break the order (discussion)

Add `@Override public FulfilmentReport fulfil(Order order)` to any route.
Read the compiler error out loud. Discuss why an error at compile time is a
different category of thing from a test that would have caught it later.

### Exercise 4 — Stretch (for fast finishers)

Make `validate` `protected` and override it in one route to skip the address
check. Get it working. Then ask the group what now stops the next person
overriding it to skip the *email* check — and put the `private` back.

## 0:51–0:58 — Costs & Comparisons

Be honest here; it is what makes the session credible.

- **It spends the inheritance slot.** Every route extends
  `FulfilmentProcess` and can extend nothing else, forever. This is the real
  price, and it is why composition is the better modern default for most
  problems.
- **The base class is fragile.** A seventh step in `fulfil` changes every
  route at once, including ones you cannot see. The sequence is public API.
- **Hooks are permissions.** Each one is granted for the lifetime of the
  class. A base class with a hook around every step has stopped protecting
  anything.
- **Steps must not call each other.** That re-creates the drift, because two
  places now know about ordering.

Then the comparisons. Two lines worth memorising:

> **Factory Method is Template Method narrowed to object creation.** One hole,
> and it returns a product.

> **Template Method guarantees an order and costs you inheritance. Strategy
> guarantees nothing about order and costs you nothing.** Choose by asking
> which invariant you actually need.

Finish by naming where they have already used it: `AbstractList`,
`InputStream.read(byte[], int, int)`, `HttpServlet.service`, JUnit's
`@BeforeEach`, and every Spring class with `Template` in its name.

## 0:58–1:00 — Wrap-Up

Ask three people for a one-sentence definition. Then assign follow-up:

> Find one sequence in your own codebase that is written out more than once.
> Ask whether anything at all would catch it if somebody swapped two of the
> steps in one copy. If the answer is "a code review, maybe", you have found
> a template method.

## Facilitator Notes

**Common misconceptions to correct:**

| They say | Correct with |
| --- | --- |
| "Isn't this just inheritance?" | It is inheritance used for one specific thing: fixing an order. Ordinary inheritance shares code; this constrains subclasses. The `final` is the difference |
| "Why not just extract helper methods?" | Helpers remove duplicated bodies. What is drifting is the call order, and a helper cannot own an order it is not the caller of |
| "Couldn't a test catch the reordering?" | Yes, and this project has one. A test tells you it broke; `final` means it cannot |
| "Should every step be abstract, to be safe?" | Then the common route has to write out behaviour it did not want to think about, and each new route re-decides something already settled. Defaults are how you stop that |
| "Why is `validate` private? I'd want to extend it" | Ask what you would write. Every override you can imagine is a way to weaken a check for everybody who comes after. The hook grants the one permission that was actually needed |
| "This is just Strategy with extra steps" | Strategy has no method that owns the sequence, so it cannot guarantee one. That is the trade, in both directions |
| "Isn't the empty hook dead code?" | It is called on every run. It is a place to stand, and the route that needs it must not have to negotiate for a call site |

**If you are running short on time:** cut Exercise 4 and shorten the costs
discussion. Never cut Exercise 2.

**If you have extra time:** have participants write the `@Nested` test class
for their fifth route, mirroring `FulfilmentRouteTest`, including the
assertion that its step names match the other four.

## Materials Checklist

- [ ] Everyone has JDK 21 and a green `./gradlew run`
- [ ] Diagrams open in a tab (`images/`)
- [ ] `animation.html` open in a browser
- [ ] Video on hand (`../video/template-method-pattern-explained.mp4`) —
      useful as a recap for anyone who joins late, or to send round afterwards
- [ ] `NaiveFulfilment` open in a second window, so you can put it beside
      `DigitalFulfilment` at the 0:26 mark
- [ ] The demo's section 1 and section 2 output ready to show side by side
- [ ] IDE font size raised for screen sharing
