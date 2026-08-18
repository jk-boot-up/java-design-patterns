# Session Guide — Abstract Factory Pattern

A 60-minute guided session for teaching or self-studying the Abstract Factory
pattern using this project.

- **Audience:** beginners comfortable with core Java, especially interfaces
- **Duration:** ~60 minutes
- **Format:** live coding + discussion
- **Prerequisites:** see [`prerequisites.md`](prerequisites.md)

> **Optional pre-work.** Ask participants to watch the ~9 minute video
> (`video/abstract-factory-pattern-explained.mp4`) beforehand. If they do, you
> can compress the problem and pattern segments and spend the extra time on
> the exercises.
>
> **Even better pre-work:** run the two sibling sessions first —
> [`../../simple-factory-pattern`](../../simple-factory-pattern), then
> [`../../factory-method-pattern`](../../factory-method-pattern). This is the
> third pattern in a progression, and the progression is most of the lesson.

## Learning Objectives

By the end of this session a participant should be able to:

1. Describe, in one sentence, what problem the Abstract Factory pattern
   solves.
2. Identify the five roles — abstract factory, concrete factories, abstract
   products, concrete products, client — in real code.
3. Explain why "the three objects always match" is a structural guarantee
   rather than a check.
4. Add a whole new family without editing any existing class.
5. Explain why adding a new *product kind* is expensive, and why that is the
   exact mirror of the pattern's strength.
6. Say honestly when Abstract Factory is *too much* machinery for the job.

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

If anyone sees `?` instead of `£` or `₹`, their console is not UTF-8. It does
not matter for the session; tell them so and move on.

## 0:05–0:15 — The Problem

**Do not show `MarketFactory` yet.** Start with the pain.

Put the naive `CheckoutService` from
[`problem-statement.md`](problem-statement.md) on screen — the one with three
consecutive `if` chains on the same string — and ask:

> *"What happens if I reorder the cases in the middle block and not the
> other two?"*

Let them find it: you get British VAT rendered in dollars. It compiles. It
runs. It produces a wrong invoice, silently.

Follow with:

> *"Where in this method would a test catch that?"*

Guide the group to name the problems themselves:

- Three branches that must stay in step with each other, forever.
- A mismatched family is one copy-paste away.
- Adding Germany means editing working code in three places.
- The client is a directory of nine class names.

**Key question to land:** *"There are nine product classes and only three
legal combinations. What in this code says so?"* Nothing does.

If someone proposes "extract each `if` into its own factory method" —
excellent, they have just re-invented Factory Method. Acknowledge it, then
ask the follow-up: *"could a subclass still return a British tax rate and an
American validator?"* It could. Park that until 0:15.

## 0:15–0:25 — The Pattern

Introduce the set-menu analogy from
[`abstract-factory-pattern-explained.md`](abstract-factory-pattern-explained.md):
à la carte lets you pair a delicate fish with a heavy red; the tasting menu
takes that freedom away on purpose, and that is what you are paying for. Let a
participant retell it back — if they can, they understand it.

Show the grid from the prerequisites doc on the board:

|  | tax | money | address |
| --- | --- | --- | --- |
| **UK** | | | |
| **US** | | | |
| **India** | | | |

Fill in the nine cells with the class names as a group. Then draw a box round
each row and say: *"three families. Nine classes, but only three legal
selections."*

Show the roles diagram ([`images/class-diagram.png`](images/class-diagram.png))
and the families diagram ([`images/families.png`](images/families.png)) —
the second one is the rows made visible, with no arrow between the columns.
Then the sequence diagram ([`images/uml-diagram.png`](images/uml-diagram.png)):
three creation calls up front, and the factory never consulted again.

Optionally open [`animation.html`](animation.html) in a browser and play it
through once. It has a **Narration** button: leave it off if you want to talk
over the animation yourself, or switch it on to let it explain each step in
its own voice — useful when participants revisit it alone afterwards.

**The one point that must land:**

> A mismatched family is not caught. It is impossible. No code exists that
> could produce one.

Expect someone to ask "but what stops me writing that code myself?" The honest
answer: nothing stops you writing a new class that mixes markets — but no
existing path does it, and you would have to work at it. Compare that with the
naive version, where a mismatch is a typo.

## 0:25–0:40 — Code Walkthrough

Open the files in this order. Resist jumping ahead.

**1. The three product interfaces — `TaxCalculator`, `CurrencyFormatter`,
`AddressValidator`**
Two methods each. Ask: *"which of these mentions a country?"* None. Point out
that each carries **vocabulary** as well as behaviour — `label()`,
`currencyCode()`, `postcodeLabel()`. That is what will let the client write
market-correct sentences with no branching.

**2. One family of concrete products — `UkVatCalculator`, `PoundFormatter`,
`UkPostcodeValidator`**
Small and unaware. Ask: *"does `UkVatCalculator` know about pounds?"* No. *"So
what makes these three a family?"* Only their name and the factory. Let that
land — the relationship is not in the classes, it is in the factory.

Skim the other six quickly; the repetition is the point.

**3. The abstract factory — `MarketFactory.java`**
Four methods, no bodies. Ask the group to find the parameter that says which
market. There is none — and that absence is the design.

**4. A concrete factory — `UkMarketFactory.java`**
Three `new` calls in a class whose name says British. Ask: *"how much code
enforces that these three match?"* Zero lines. The consistency comes from
there being nowhere else the choice is made.

Show `UsMarketFactory` alongside it — same shape, different nouns.

**5. The client — `CheckoutService.java`**
This is the heart of the session. Read the constructor: four lines and the
world is configured. Then ask the group to search the *whole class* for "UK",
"US" or "India". Nothing. Then read `quote(...)` and ask them to point at any
branch on the market. There is none, including in the error message.

Point at the last statement of the constructor and say: *"after this line, the
factory has done its job and is never used again."*

**6. The value objects — `Order.java`, `Quote.java`**
Cover the `record` primer if needed. Ask why `Quote` holds `String tax` rather
than `double tax`. Target answer: so the currency decision survives all the way
out to the caller.

**7. The demo — `AbstractFactoryDemo.java`**
One loop, three markets. Ask what changes between iterations: one constructor
argument.

**8. The tests — `MarketFactoryTest.java`, `CheckoutServiceTest.java`**
Show `newMarketNeedsNoExistingChange` — it invents Germany entirely inside one
test method, as anonymous classes, and the unchanged `CheckoutService` quotes
€238.00 for it. Show `identicalCodeProducesAMarketCorrectQuote` — one
parameterised test body, three markets, three different totals.

Run `./gradlew run` live. Point out that the three blocks are structurally
identical and only the money differs, then read the final `Rejected:` line
aloud. That visual is worth more than any slide.

## 0:40–0:50 — Exercises

Let participants work; circulate and help.

### Exercise 1 — Add Germany (everyone)

Write `GermanVatCalculator` (19%, "MwSt"), `EuroFormatter` (`€`, "EUR"),
`GermanPlzValidator` (five digits) and `GermanyMarketFactory`, then add one
line to the demo.

> **The payoff:** ask everyone who finishes *"how many existing files did you
> edit?"* The answer is one — the demo, and only because it is a demo. Say
> this out loud; it is half the lesson of the session.

### Exercise 2 — Feel the expensive direction (everyone)

Now add a fourth product kind: `ReceiptTemplate`, with one method
`String render(Quote quote)`. Add `createReceiptTemplate()` to
`MarketFactory` and make it compile.

> **The payoff:** count the files touched. It is every factory, including
> Germany from Exercise 1. Ask: *"which change was cheaper, and why?"* Target
> answer: rows are cheap, columns are expensive, and that trade is the pattern.

This is the other half of the lesson. Do not skip it.

### Exercise 3 — Try to build a mismatch (everyone)

Without editing `CheckoutService`, give it British tax and American address
validation. Let them try for two minutes. The constructor does not offer the
opportunity.

Then ask: *"what would you have had to change to make it possible?"* Answer:
the constructor's signature — which is exactly the design decision under
discussion.

### Exercise 4 — Spot the anti-pattern (discussion)

Present a `MarketFactory` with the signature
`TaxCalculator createTaxCalculator(String market)`. Ask: *"what have we
lost?"* Everything — the decision moved back to the call site, per call, and
the family guarantee is gone.

Then present a version where `createCurrencyFormatter()` returns
`PoundFormatter` instead of `CurrencyFormatter`. Same question, same answer.

### Exercise 5 — Stretch (for fast finishers)

Delete `MarketFactory` entirely and inject the three products into
`CheckoutService` directly with a three-argument constructor. It works, it is
less code, and a dependency-injection framework would wire it happily.

Ask: *when* is that better? Target answer: when nothing enforces a relationship
between the three anyway, or when the container is the thing guaranteeing
consistency. Then ask what you have lost: any object that means "the British
market", and any compile-time reason the three go together.

There is no universally right answer here — that is the discussion.

## 0:50–0:58 — Pitfalls & Comparisons

Cover the "What to Watch Out For" section:

- Adding a product *kind* means editing every factory. This is real and it
  gets worse as you add families.
- The class count is markets × product kinds. Be sure the families are real.
- Something still has to choose the factory. That decision often becomes a
  Simple Factory, and that is fine as long as you notice and keep it in one
  place.
- Do not use it when the products have no reason to agree. The test question:
  *would a mismatched pair be a bug?*
- No parameters on the creation methods, ever.
- Beware the abstract factory with exactly one implementation, added "in case
  we go international one day".

Then the comparison table. The line worth memorising:

> **Simple Factory chooses with a `switch`. Factory Method chooses with
> inheritance. Abstract Factory chooses a whole family at once.**

And the one-sentence test for which to reach for:

> If getting two objects from different groups would be a bug, you want
> Abstract Factory.

If the group did the earlier sessions, put all three class diagrams side by
side on screen and walk left to right. The arrows tell the whole progression
without words.

Close with real-world sightings: `DocumentBuilderFactory`, `java.sql.Connection`
handing you a matching `Statement` and `ResultSet`, Swing's `LookAndFeel`, and
any application that swaps a whole coordinated set of behaviour on a locale, a
theme or a cloud provider.

## 0:58–1:00 — Wrap-Up

Ask three people for a one-sentence definition. Then assign follow-up:

> Find one place in your own codebase where two or more objects are chosen
> separately but must agree, and sketch the abstract factory that would make
> the mismatch impossible.

## Facilitator Notes

**Common misconceptions to correct:**

| They say | Correct with |
| --- | --- |
| "Isn't this just Factory Method with more methods?" | Factory Method varies *one* product by subclassing the creator. Here the point is that several products must agree — the guarantee, not the count |
| "So it prevents mismatches by validating?" | No. It prevents them by there being no code that could create one. Nothing is checked |
| "Why not just pass the three objects in?" | You can — that is Exercise 5, and sometimes it is right. The factory earns its place when the three must match and nothing else enforces it |
| "Nine classes for three countries?" | A fair objection. Ask what the naive version costs on the day a fourth country arrives, and what a wrong invoice costs |
| "Can I add a product kind later?" | Yes, and it is the expensive direction. That is Exercise 2, and it is deliberate |
| "Is `market()` part of the pattern?" | Not strictly — it is a convenience so the client can label output. The three `create...` methods are the pattern |
| "Is this a Builder?" | No. Builder assembles one complicated object step by step; Abstract Factory hands you several finished ones that match |

**If you are running short on time:** cut Exercise 5 and shorten the pitfalls
discussion. Never cut Exercises 1 and 2 — they are the two halves of the
trade-off, and the session does not work with only one of them.

**If you have extra time:** open the Factory Method project side by side and
have the group argue about whether the delivery-tier example could be
rewritten as an abstract factory, and whether it should be. The answer is
"it could, and it should not" — but the argument is the learning.

## Materials Checklist

- [ ] Everyone has JDK 21 and a green `./gradlew run`
- [ ] Diagrams open in a tab (`images/`)
- [ ] `animation.html` open in a browser
- [ ] Video on hand (`../video/abstract-factory-pattern-explained.mp4`) —
      useful as a recap for anyone who joins late, or to send round afterwards
- [ ] Naive three-`if`-chain `CheckoutService` snippet ready to show first
- [ ] The blank 3×3 grid on a whiteboard or slide
- [ ] Simple Factory and Factory Method class diagrams ready for the 0:50
      comparison
- [ ] IDE font size raised for screen sharing
