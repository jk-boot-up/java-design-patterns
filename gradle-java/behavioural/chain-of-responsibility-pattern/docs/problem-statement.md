# Problem Statement — Checkout Screening

Before an online store accepts an order it screens it. Four questions, none of
them optional:

| Check | Question | Rejects when |
| --- | --- | --- |
| address | is this somewhere a courier goes? | outside GB/IE, or an excluded postcode |
| stock | can the warehouse pick every line? | any line wants more than is on the shelf |
| fraud-score | what does the risk model think? | score at or above 80 |
| payment-limit | will the issuer authorise this? | total above the card's limit |

Written the obvious way, that is one method:

```java
public Result validate(CheckoutRequest request) {
    if (!servedCountry(request))    return no("we do not ship to ...");
    if (excludedPostcode(request))  return no("no courier covers ...");
    if (outOfStock(request))        return no("... is out of stock");
    if (overCardLimit(request))     return no("card limit exceeded ...");
    if (request.fraudScore() >= 80) return no("we are unable to process this order");
    return OK;
}
```

Read it on its own and there is nothing wrong with it. It is short, it is in
one file, and a new joiner can tell you the whole screening policy in thirty
seconds. **For one market and a fixed set of rules this is the right answer**,
and if the store never changes, this project is over-engineering. What follows
is what happens when it does change.

## What Goes Wrong

### 1. The order of the checks is welded into the method

The payment check is written above the fraud check. Nobody decided that; it is
where somebody's cursor was in 2022.

```
  A monitor, on a £250 card, scoring 92 out of 100 for fraud:
    naive says      : REJECTED — card limit exceeded, please try another card
```

The customer is told to try another card. They do — and the second card works,
because there is nothing wrong with the *cards*. The risk model shouted 92 and
nobody was listening, because the method returned before it got there.

Fixing this means editing `validate`, which is also the file where the checks
themselves live, so the change that reorders the policy and the change that
alters a rule land in the same diff and get reviewed as one thing.

### 2. A boolean has no third answer

The risk model does not deal in yes and no. It produces a score, and the reason
the business pays for it is the middle band — the orders that should go to a
human. `Result` is a `boolean` and a `String`, so the middle band has to
be forced into one of two answers, and it is forced into the cheap one:

```
  Headphones, scoring 64 — the band risk asked us to review:
    naive says      : ACCEPTED — nothing objected
```

### 3. Variants are copies, and copies drift

Trade accounts are invoiced monthly rather than charged at checkout, so the
card limit does not apply to them. Somebody copied `validate`, deleted the card
check, and called it `validateTradeAccount`. In the same edit, the address
check went too.

```
  A trade account ordering two desks to St Helier, Jersey:
    validate()      : REJECTED — no courier covers JE2 3AB
    trade copy      : ACCEPTED — nothing objected
```

Two desks are now on their way to an island no courier serves. The two methods
are not related by anything the compiler can see. No test failed, because the
trade method's tests were copied too.

### 4. The result cannot say who decided

`Result` has exactly two components: a `boolean` and a `String`. When
support asks "which check rejected order R-2003?", the only evidence is the
message text, and the only way to answer programmatically is to match on it.
Change a message and you break a dashboard.

### 5. Testing one check means satisfying the four above it

The fraud rule is the fifth statement of the method. To reach it a test must
construct a deliverable address, a basket the warehouse can pick, and a card
with enough headroom — none of which the fraud rule cares about. Every one of
those is a chance for a test to fail for a reason that has nothing to do with
what it is testing.

## What We Actually Want

- **One class per check**, testable on its own, with nothing above it to
  satisfy first.
- **The order as configuration.** Reordering the policy should be a line in
  the wiring, not an edit inside the file where the rules live.
- **A variant built by leaving a link out**, not by copying a method.
- **A third answer**, so "a person should look at this" is expressible.
- **Evidence**: which link decided, and which links never ran.
- **A deliberate answer to "what if nobody decides?"** — because once the
  checks are separate objects, a request really can travel past all of them
  without anyone taking responsibility for it.

## What This Costs

The pattern buys all six, and this project is explicit that it is not free.
The policy that was readable top to bottom in one method is now spread across
four check classes and a line of wiring; answering "which link rejected this?"
needs the report to record who ran, which four sequential `if` statements never
did; and a handler holds its own successor, so an instance belongs to exactly
one chain.

The last thing the demo prints is the honest version of that: when the checks
and their order never change, write the four `if` statements.
