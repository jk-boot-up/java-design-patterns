# Session Guide — Interpreter Pattern

A 60-minute session plan for teaching the Interpreter pattern from this
project. Written for a facilitator working with beginners; every timing is a
suggestion, and the exercises are the part worth protecting if you run late.

**Audience:** developers who can write a class that implements an interface,
and who have at some point added one more `if` to a method that already had
several.

**Setup:** everyone has the project cloned and `./gradlew test` passing before
the session starts. See [`prerequisites.md`](prerequisites.md).

## Learning Objectives

By the end, participants can:

1. Explain what a terminal and a non-terminal expression are, and say which one
   is allowed to hold another expression.
2. Read a rule tree and say what sentence it represents, and the reverse.
3. Write a new terminal without changing any existing class.
4. Say what the pattern costs — one class per phrase, and a parser that grows —
   and name a case where two `if` statements are the better answer.
5. Say why a rule that can describe itself is worth more than a rule that
   merely works.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:05 | Setup check |
| 0:05–0:17 | The problem |
| 0:17–0:27 | The pattern |
| 0:27–0:40 | Code walkthrough |
| 0:40–0:50 | Exercises |
| 0:50–0:58 | Pitfalls and comparisons |
| 0:58–1:00 | Wrap-up |

## 0:00–0:05 — Setup Check

Have everyone run:

```bash
./gradlew test    # 21 tests
./gradlew run
```

Anyone whose tests fail should pair for the session rather than debug.

Then, before showing any code, write this on the board and ask the room to read
it out as English:

```java
new AndRule(List.of(new CountryIs("UK"), new BasketOver(50)))
```

Somebody will say "country is UK and basket over fifty". That is the whole
session in one line, and it is worth having the room say it before anybody has
seen a class definition. Leave it on the board.

## 0:05–0:17 — The Problem

Open [`problem-statement.md`](problem-statement.md) and set the scene: three
promotions, each a code, a percentage and a rule about who qualifies. Show the
first one as Java and agree that there is nothing wrong with it.

Then show `NaiveVoucherRules` and run `./gradlew run`, reading the second
section out loud together. A US order takes 15% off. A UK shopper with three
items is offered nothing.

Three things to draw out, in this order:

1. **Both bugs are copies.** Each promotion was written by copying the one above
   it. SAVE15 never got its UK check written at all; FREESHIP kept a
   `firstOrder()` test from a welcome offer that retired last spring.
2. **Neither throws.** Ask how the shop would find out. The answer for the first
   is "when somebody adds up the margin", and for the second is "never" — a
   missing discount looks exactly like a shopper who did not qualify.
3. **Marketing wants an offer live on Friday.** That is now a branch, a pull
   request, a review and a release, written by someone who did not read the
   campaign brief. Both bugs live in that gap.

## 0:17–0:27 — The Pattern

Give the definition, and then immediately take it apart:

> Given a language, define a representation for its grammar along with an
> interpreter that uses the representation to interpret sentences in the
> language.

Say plainly that this sentence is why the pattern has a reputation, and then
give the beginner's version: **write one small class per kind of phrase, and let
a big phrase hold small ones.**

Use the sentence-diagram analogy. "The tall man in the blue coat" and "the man"
are both noun phrases; either drops into "…bought a laptop" without rewriting
the sentence around it. Rules compose for the same reason.

Then point back at the board snippet and name the parts: `CountryIs` and
`BasketOver` are terminals, `AndRule` is a non-terminal, and the `Order` it will
be asked about is the context. Ask the room which of those three can hold
another rule. It is worth making them say it.

## 0:27–0:40 — Code Walkthrough

In this order:

1. **`Rule`** — two methods, no fields. Say that every other rule class in the
   project implements this, from the smallest to the largest, and that this is
   the fact everything else rests on.
2. **`BasketOver`** — a whole terminal, on one screen. One comparison and one
   string. Ask whether it needs to be bigger; it does not.
3. **`AndRule`** — read the loop, then ask what it knows about its parts. Land
   on: nothing. Not what they are, not whether they are leaves, not how deep the
   tree below goes. Then ask what would need to change to nest an `OrRule`
   inside it. Nothing does, and that is the pattern working.
4. **`describe()`** — show that the sentence in the audit log is *rebuilt* from
   the objects rather than remembered from the line that was read in, and show
   `parsingAndDescribingRoundTrip` asserting it. This is the section people
   remember afterwards.
5. **`RuleParser`** — say up front that this is not part of the pattern. Then
   show the two splits, and why splitting on `or` first is what gives `and` the
   tighter grip. Finish on the `throw`: a typo is refused on Wednesday when the
   promotion is *saved*, not on Friday when an order is *priced*.
6. **`PromotionBook`** — search it, live, for the word "UK". It is not there.
   Every fact about when an offer applies lives in a line of text.

## 0:40–0:50 — Exercises

### Exercise 1 — Add a terminal (everyone)

Add `basket under N`: one record implementing `Rule`, and one `if` in the
parser. Then write a promotion that uses it.

The point to draw out is what was *not* touched: no existing rule class,
nothing in `PromotionBook`, nothing in `Promotion`. Ask what the equivalent
change would have been in `NaiveVoucherRules`.

### Exercise 2 — Break the precedence (everyone)

Swap the order of `parseOr` and `parseAnd` so `and` splits first, and run the
tests. `andBindsTighterThanOr` fails.

Then ask the more interesting question: which of the shop's promotions would
have quietly changed meaning, and would anyone have noticed? This is the
exercise most worth protecting if you are short of time.

### Exercise 3 — Break the round trip (most people)

Make `OrRule.describe()` join with `" OR "` instead of `" or "`. The rule still
evaluates correctly, and the round-trip test still fails.

Ask why that is worth failing a build over. The answer — that the audit log and
the tree the checkout obeys are not allowed to drift — is the argument for
`describe()` existing at all.

### Exercise 4 — Stretch (for fast finishers)

Add brackets, so `country is UK and (basket over 100 or items at least 5)`
parses. This is deliberately the hard one: it is the moment the parser stops
being a convenience and becomes a parser. Nobody will finish it, and that is
the lesson — see the first pitfall below.

## 0:50–0:58 — Pitfalls and Comparisons

**It does not scale to a big language.** One class per phrase is fine for seven
phrases and unbearable for seventy. Whoever attempted Exercise 4 has just felt
the wall; let them describe it. The Gang of Four say the same thing, and it is
the most commonly ignored sentence in the chapter.

**The parser is the part that grows.** Adding a terminal is small forever.
Adding syntax is not.

**It is slower than an `if`.** Every node is an object and every evaluation a
virtual call. For three promotions on one order this is irrelevant; say so
plainly, so nobody optimises the wrong thing.

**Do not reach for it when the rules never change.** If the shop has run the
same two promotions for four years, two `if` statements are better code. The
pattern earns its keep when *shipping code* is the bottleneck.

**Interpreter vs. Composite.** Ask what the difference is; the honest answer is
intent, not structure. Interpreter *is* a Composite — same tree, same uniform
interface. Composite is about treating one thing and many things alike;
Interpreter is about meaning.

**Interpreter vs. Strategy.** A whole rule tree is often used as a Strategy: the
checkout holds a `Rule` and does not care which one. Strategy's shape wrapped
around Interpreter's insides.

## 0:58–1:00 — Wrap-Up

One sentence to leave them with:

> A rule written in code can only be run. A rule written in a language can be
> run, read, printed, checked and changed by the person who owns it.

Point at [`interpreter-pattern-explained.md`](interpreter-pattern-explained.md)
for the written version, and [`animation.html`](animation.html) for the stepped
walkthrough.

## Facilitator Notes

- **The board snippet earns its five minutes.** Reading a tree as English before
  seeing any class definition removes most of the mystique the definition
  creates, and later questions resolve back to it cheaply.
- **Do not skip running the naive version.** Reading two subtly wrong branches
  convinces nobody; watching a US order take 15% off convinces everybody.
- **Expect "isn't this over-engineering?"**, and welcome it. It is the right
  question, and the honest answer is yes — for three promotions that never
  change. Answer it with the Friday scenario rather than with a principle.
- **Expect somebody to want a rules engine.** Agree that production shops often
  use one, and point out that this project is what one looks like inside.
- **Watch for the word "recursion" scaring the room.** It never needs to be
  said. "A rule can hold rules" carries the whole idea, and is not frightening.

## Materials Checklist

- [ ] Project cloned, `./gradlew test` green (21 tests)
- [ ] `./gradlew run` output visible to the room
- [ ] Board or slide with the `AndRule` snippet
- [ ] [`class-diagram.md`](class-diagram.md) and
      [`uml-diagram.md`](uml-diagram.md) open in a tab
- [ ] [`animation.html`](animation.html) open in a browser, for the walkthrough
