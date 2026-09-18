# Problem Statement

## The feature

The same feature every project in this category builds: a customer places an
order for three products, stock is checked, payment is taken, a confirmation
is sent. Ada Okafor, `cust-8801`, buys one espresso machine, one grinder and
two bags of beans — **£382.50**.

This project's demonstration sits at the moment just after that: the order
summary a customer sees on screen, and the confirmation email that follows
it. Both have to say the same thing.

## The naive version, in two parts

### Part one: no separation at all

`EverythingOrderScreen` checks stock, takes payment and formats the screen
text in one method. It works, and because there is only one method there is
nothing yet for two outputs to disagree about — its problem is a different
one: you cannot test "does the summary read correctly" without also running
a full checkout, because the two are the same fourteen lines.

### Part two: a second view that computes its own answer

A real screen exists — `ScreenSummaryView`, reading a computed
`OrderSummaryModel` — and it works. Then somebody is asked for a
confirmation email. The model has no method yet for "unit prices rounded to
the nearest pound, for a tidier-looking line", so rather than ask for one,
the new email view reaches into the product catalogue itself and rounds each
unit price before multiplying.

It compiles. It is not a hack — a reviewer would see a small, self-contained
view doing its own formatting. And it prints a different total:

```
the screen says £382.50. the email says £383.00.
```

The burr grinder's eighty-nine pounds fifty rounds to ninety before it is
multiplied by one, and the fifty pence never comes back. **Nothing in the
build objects.**

## What it costs

A customer sees one number at checkout and a different one in their inbox
thirty seconds later. There is no exception, no failed test, no log line —
both views ran correctly, by their own separate arithmetic. The bug is not
that either calculation is wrong in isolation; it is that there were two
calculations at all.

## What the pattern must deliver

A single **Model** that computes an order's total exactly once. A **View**
interface so narrow that a view cannot be handed anything except the
finished model — no product, no price, no quantity it could multiply for
itself. A **Controller** that is the only thing allowed to call the
application layer and build the model. And the rule enforced as a test:
no class in the view package may depend on the infrastructure package,
because that dependency is precisely how a view gets the ingredients to
compute a number of its own.

The pattern is judged by one forced change: add a second view — the real
email, this time reading the model like the screen does — and show that it
cannot disagree, because neither view is capable of adding anything up.
