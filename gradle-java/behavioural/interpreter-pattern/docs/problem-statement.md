# Problem Statement

An online shop runs promotions. A promotion is a code, a percentage, and a rule
about who gets it:

- **SAVE10** — 10% off, for UK orders over £50
- **SAVE15** — 15% off, for UK orders over £100
- **FREESHIP** — 5% off, for UK orders of three items or more

Written in Java, the first one is four lines and there is nothing wrong with it:

```java
if ("UK".equals(order.country()) && order.basketPounds() > 50) {
    return 10;
}
```

The trouble is not the first promotion. It is the fourth.

## What Actually Happens

Each new offer is added by copying the branch above it and changing the
numbers, because that is the fastest correct-looking thing to do. Copies are
exactly the kind of thing a hurried person gets *almost* right, and
`NaiveVoucherRules` contains two that are not.

**SAVE15 gives money away.** The ticket said "fifteen percent on baskets over
one hundred". That the offer was UK-only was in the paragraph above the
sentence somebody read, so no line of code was ever written for it:

```java
if (order.basketPounds() > 100) {
    return 15;
}
```

Every large overseas order now takes fifteen percent off. On a £120 order that
is £18, on every order, for as long as nobody adds it up.

**FREESHIP withholds it.** That branch was copied from a welcome offer that
retired last spring, and the first-order check came along with it:

```java
if (order.firstOrder() && "UK".equals(order.country()) && order.itemCount() >= 3) {
```

A returning UK shopper with three items is offered nothing. Nobody reports it,
because a missing discount looks exactly like a shopper who did not qualify.

Neither bug throws. Neither is logged. Both are correct-looking Java that
compiled, passed review and shipped.

## Why It Hurts

**1. Every rule change is a code change.** Marketing wants an offer live on
Friday. That is now a branch, a pull request, a review, a merge and a release —
and the person who writes the branch is not the person who understands the
offer. The gap between those two people is where both of the bugs above came
from.

**2. The rules cannot be read by the people who own them.** Nobody outside the
team can check that the code says what the campaign brief said, so the check
that would catch a misread ticket cannot happen.

**3. Nothing can say why.** When a shopper asks why they got 15% off, the only
answer available is "read the source". A number came out of a method; the
reasoning stayed in the shape of the Java it was made of.

**4. There is no place for a typo to be caught.** A mistyped condition is
valid Java. It compiles, deploys, and behaves — wrongly — at checkout. There is
no earlier moment at which anything could have objected.

**5. It grows the wrong way.** Every new promotion is a new branch in one
growing method, and each one is a fresh chance to copy the wrong condition.
The tenth promotion is riskier to add than the first, which is precisely
backwards.

## What the Pattern Has to Deliver

- A rule written as **text** — `country is UK and basket over 50` — that the
  people who own the offers can read, and that lives wherever the shop keeps
  its data rather than in a source file.
- A way to **combine** simple conditions into complicated ones, to any depth,
  without any of the combining code knowing what the conditions are about.
- A rule that can **explain itself**, so the audit log and the shopper get the
  same sentence the offer was written in.
- A **typo refused when the promotion is saved**, on a Wednesday, when it is
  cheap — and not at a checkout on Friday.
- Adding a promotion nobody anticipated must be **one line of text**: no new
  class, nothing recompiled, nothing deployed.

That is the Interpreter pattern: give the rules a small language, and give the
language a class per kind of phrase.

## See Also

- [`interpreter-pattern-explained.md`](interpreter-pattern-explained.md) — the
  pattern and the code
- [`class-diagram.md`](class-diagram.md) — the structure
- [`uml-diagram.md`](uml-diagram.md) — one rule being evaluated, message by
  message
- [`animation.html`](animation.html) — the same evaluation, stepped through
