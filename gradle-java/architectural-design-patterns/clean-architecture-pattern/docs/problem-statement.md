# Problem Statement

## The feature

The same feature every project in this category builds: a customer places
an order for three products, stock is checked, payment is taken, a
confirmation is sent. Ada Okafor, `cust-8801`, buys one espresso machine,
one grinder and two bags of beans — **£382.50**.

## The naive version

The previous project in this category, Hexagonal Architecture, already
inverted the one cost Layered Architecture left behind: the use case's
storage, payment and catalogue needs became interfaces, declared by the
use case itself. This project's naive version reproduces the shortcut a
team takes when that discipline slips: `NaivePlaceOrderInteractor`, a class
that calls itself a use case, with a constructor typed as three concrete
gateway classes — not the interfaces the real use case declares.

It works. Every acceptance check passes. And it reaches straight through
the interface-adapters circle it is supposed to sit inside of, to name
classes that belong two circles further out.

## What it costs

The same two costs Hexagonal Architecture named, generalised. The use case
cannot be tested without constructing real gateways. And nothing about its
own source tells you it has broken the rule — the import compiles, the
class is short, a reviewer would not blink.

## What the pattern must deliver

**Concentric circles** — entities at the centre, use cases around them,
interface adapters around those, frameworks and drivers on the outside —
with one rule, stated once: **source code dependencies point only
inward.** Not "mostly inward". Never outward, at any boundary, for any
reason.

The pattern's single most valuable contribution has to be shown in code,
not asserted in a diagram: a use case calling `orders.save(order)` sends
control **outward**, to whichever gateway was wired in at startup — while
the **dependency**, the fact that a type named `OrderRepository` must exist
for the file to compile, points **inward**, at an interface the use case
itself declared. Control and dependency travel in opposite directions, and
that disagreement is the entire trick.

The pattern is judged by the largest forced change in the category: add an
entirely new delivery mechanism and an entirely new data source, **at the
same time**, with the two inner circles — entities and use cases — proven
untouched.
