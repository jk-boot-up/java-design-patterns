# Session Guide — Simple Factory Pattern

A 60-minute guided session for teaching or self-studying the Simple Factory
idiom using this project.

- **Audience:** beginners comfortable with core Java
- **Duration:** ~60 minutes
- **Format:** live coding + discussion
- **Prerequisites:** see [`prerequisites.md`](prerequisites.md)

> **Optional pre-work.** Ask participants to watch the ~7 minute video
> (`video/simple-factory-pattern-explained.mp4`) beforehand. If they do, you
> can compress the problem and pattern segments and spend the extra time on
> the exercises. If you are teaching a group that has *not* watched it, run
> the session exactly as written below.

## Learning Objectives

By the end of this session a participant should be able to:

1. Describe, in one sentence, what problem the Simple Factory idiom solves.
2. Identify the four roles — product, concrete products, factory, client —
   in real code.
3. Explain why the client must never name a concrete product type.
4. Write a small factory over two or more existing implementations.
5. State plainly that Simple Factory violates the Open/Closed Principle, and
   say why that is an acceptable trade.
6. Distinguish Simple Factory from Factory Method, Abstract Factory and a
   static factory method.

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

**Do not show the factory yet.** Start with the pain.

Put the naive `if`/`else` chain from
[`problem-statement.md`](problem-statement.md) on screen and ask:

> *"This same block exists in the web controller, the mobile API and the
> admin tool. We are adding wallet payments on Monday. What happens?"*

Guide the group to name the problems themselves:

- Three places to edit, and nothing tells you when you miss one.
- The checkout class knows the name of every payment class.
- One copy trims the string, another does not.
- You cannot test the choosing without running a checkout.

**Key question to land:** *"Whose job is it to know that `UPI` means
`UpiPayment`?"* Answer: exactly one class's job — and right now it is
nobody's.

## 0:15–0:25 — The Pattern

Introduce the coffee-shop counter analogy from
[`simple-factory-pattern-explained.md`](simple-factory-pattern-explained.md).
Let a participant retell it back — if they can, they understand it.

Show the class diagram ([`images/class-diagram.png`](images/class-diagram.png))
and name the four roles. Trace the arrows out of `PaymentMethodFactory` with
a finger and say: *"these are the dependencies the client no longer has."*
Then show the sequence diagram
([`images/uml-diagram.png`](images/uml-diagram.png)) and point out the two
phases — creation once, then use through the interface.

Optionally open [`animation.html`](animation.html) in a browser and play it
through once. It has a **Narration** button: leave it off if you want to
talk over the animation yourself, or switch it on to let it explain each
step in its own voice — useful when participants revisit it alone
afterwards.

**The one point that must land:**

> The client names the type as **data**. It never names the class.

Ask why that matters. Target answer: data can come from a form, a database
or a config file; a class name cannot.

## 0:25–0:40 — Code Walkthrough

Open the files in this order. Resist jumping ahead.

**1. The product interface — `PaymentMethod.java`**
Two methods, no implementation. Ask: *"What does a client that holds one of
these know about credit cards?"* Nothing.

Cover the `sealed` primer here if anyone is new to it — but promise that its
real payoff arrives two files later.

**2. A concrete product — `UpiPayment.java`**
Point out how small and unaware it is. Ask: *"Could I use this class in a
totally different app?"* Yes. That is the point.

Skim `CreditCardPayment`, `PayPalPayment`, `NetBankingPayment` — same shape,
no surprises.

**3. The value objects — `PaymentRequest.java`, `PaymentReceipt.java`**
Cover the `record` primer if needed. Emphasise: one object in, one object
out.

**4. The factory — `PaymentMethodFactory.java`**
This is the heart of the session. Walk through `create` and ask the group to
spot what it is doing. Draw out three answers:

- **choosing** the implementation from data,
- **constructing** it, so no caller has to,
- **validating** the input in one place.

Then the moment worth waiting for: point at the `switch` and ask *"where is
the `default` branch?"* There is none — the enum is exhaustive. Explain that
adding a case breaks the build here and nowhere else.

Also show the `String` overload and ask *why* it exists. Answer: real input
is text.

**5. The client — `CheckoutService.java`**
One line to get the object, then ordinary method calls. Ask what it knows
about PayPal. Nothing.

**6. The tests — `PaymentMethodFactoryTest.java`, `CheckoutServiceTest.java`**
Show that the factory's selection logic is testable entirely on its own, and
that `sameCallSiteDifferentImplementation` proves the client code does not
change when the type does.

Run `./gradlew run` live. Point out that the `Checkout:` lines are identical
across all four blocks and only the payment lines differ. That visual is
worth more than any slide.

## 0:40–0:50 — Exercises

Let participants work; circulate and help.

### Exercise 1 — Break the build on purpose (everyone)

Add `WALLET` to `PaymentType`. Compile. Read the error.

> **The payoff:** the compiler found the one place that needed changing.
> Say this out loud when someone finishes — it is the lesson of the whole
> session.

Then write `WalletPayment`, add it to `permits` and to the `switch`. Confirm
that `CheckoutService` was never touched.

### Exercise 2 — Prove the client is decoupled (everyone)

Search `CheckoutService.java` for the word `Payment` followed by a concrete
class name. There is none. Now search `PaymentMethodFactory.java` — all four
live there. Discuss what that concentration bought you.

### Exercise 3 — Spot the anti-pattern (discussion)

Present a factory that also validates the amount, looks up the customer's
country, applies a currency conversion and logs to an audit table. Ask:
*"Is this still a factory?"* No — it has absorbed business logic. A factory
chooses and constructs; it does not decide anything else.

### Exercise 4 — Stretch (for fast finishers)

Replace the `switch` with a
`Map<PaymentType, Supplier<PaymentMethod>>` registry. Discuss what this buys
(products can register themselves; no central edit) and what it costs (you
lose the compiler's exhaustiveness check, so a missing entry becomes a
runtime failure). There is no universally right answer — that is the
discussion.

## 0:50–0:58 — Pitfalls & Comparisons

Cover the "What to Watch Out For" section:

- It violates Open/Closed — deliberately, in exchange for one place to
  change.
- A factory is not a god object; keep logic out of it.
- Forty cases means you want a registry.
- Static is convenient and hard to substitute in tests.

Then the comparison table. The line worth memorising:

> **Simple Factory chooses with a `switch`. Factory Method chooses with
> inheritance. Abstract Factory chooses a whole family at once.**

Close with real-world sightings: `Calendar.getInstance()`,
`Charset.forName()`, `DriverManager.getConnection()`.

## 0:58–1:00 — Wrap-Up

Ask three people for a one-sentence definition. Then assign follow-up:

> Find one place in your own codebase where a caller picks an implementation
> with an `if`/`else` chain, and sketch the factory that would replace it.

## Facilitator Notes

**Common misconceptions to correct:**

| They say | Correct with |
| --- | --- |
| "So it's a GoF pattern?" | No — it is an idiom. Factory Method and Abstract Factory are the GoF ones |
| "The switch is still there, what did we gain?" | One copy instead of many, and the compiler guards it |
| "Isn't this the same as Factory Method?" | Factory Method chooses by subclassing; here nothing is subclassed |
| "Shouldn't the factory be an interface?" | Only when you need to swap it — otherwise you are inventing Abstract Factory for no reason |
| "Why not just `new`?" | With one implementation, do. This pays off from about three onwards |

**If you are running short on time:** cut Exercise 4 and shorten the
pitfalls discussion. Never cut Exercise 1 — it is where the concept
actually lands.

**If you have extra time:** have participants convert this project to
Factory Method (an abstract `Checkout` class with an abstract
`createPaymentMethod()`), then compare the two side by side. This is the
best possible bridge to the next session.

## Materials Checklist

- [ ] Everyone has JDK 21 and a green `./gradlew run`
- [ ] Diagrams open in a tab (`images/`)
- [ ] `animation.html` open in a browser
- [ ] Video on hand (`../video/simple-factory-pattern-explained.mp4`) —
      useful as a recap for anyone who joins late, or to send round
      afterwards
- [ ] Naive `if`/`else` snippet ready to show first
- [ ] IDE font size raised for screen sharing
