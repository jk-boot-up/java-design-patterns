# Problem Statement

## The feature

A customer places an order for three products. Stock is checked. Payment is
taken. A confirmation is sent.

That is the whole feature, deliberately small, and it is the same feature
every project in this category builds — layered, MVC, hexagonal and clean
architecture all place the same order, so a reader can compare the shape of
the code across the four without the scenario changing underneath them.

**The catalogue.**

| SKU | Name | Price | Stock |
| --- | --- | --- | --- |
| `ESP-001` | Espresso Machine | £249.00 | 4 |
| `GRD-014` | Burr Grinder | £89.50 | 2 |
| `BNS-220` | Coffee Beans, 1kg | £22.00 | 40 |

**The order.** Ada Okafor, `cust-8801`, buys one espresso machine, one
grinder, and two bags of beans: **£382.50**.

## The naive version, in two parts

### Part one: no layers at all

The first naive version, `EverythingOrderService`, is one class that
validates the request, holds the catalogue, does the pricing arithmetic,
charges the card, stores the order and sends the email. Seventy-four lines,
every one of them easy to read in isolation.

It has one property that no amount of tidying removes: **you cannot test the
pricing without the storage.** To assert that three lines come to £382.50 you
must construct the whole class, which means constructing its catalogue map,
its order map and its list of sent email, because they are fields of the same
object. There is no seam between "work out the total" and "remember it
happened".

### Part two: layers that exist and are skipped anyway

The second naive version is the one that matters more, because it is what
most codebases that call themselves "layered" actually are. The four
packages exist — `presentation`, `application`, `domain`, `infrastructure` —
with the right names, and a diagram of them on a wall somewhere.

Then somebody needs a screen listing a customer's past orders. The
application layer has no method for it, and adding one means a request
object, a result object and a service method — three files to return rows
that are sitting right there in the order table. So `OrderHistoryScreen`
takes the storage class directly. Ten minutes instead of an afternoon. It
compiles. The tests pass. It ships.

**Nothing in the build objects to it.** That sentence is the whole problem
with layering as it is usually practised: it is a convention, and a
convention that nothing checks decays — not all at once, but one reasonable
Tuesday at a time.

## What it costs later

Six months on, the storage layer needs to change — a real example follows in
this project: a map keyed by order id is replaced by an append-only log. Every
class that reached the store through the application layer needs nothing done
to it. `OrderHistoryScreen` does not compile, because it imported the concrete
storage class directly and that class no longer exists in the same shape. The
bill for the ten minutes arrives, with interest, on a day nobody remembers the
ten minutes.

## What the pattern must deliver

Four layers — presentation, application, domain, infrastructure — where each
one depends only on the layer directly beneath it, **and where that rule is
not a diagram but a test.** A class that reaches past its neighbour into a
layer it should not touch must fail a build, automatically, naming the class
and the layer it reached into — not wait to be noticed in a code review that
might not happen.

The pattern is judged, in this project, by one forced change: swap the entire
storage layer for a different implementation, and count what had to be
touched. The number — not the adjective "decoupled" — is the argument.
