# Problem Statement — Fulfilling an Order Three Different Ways

## The Scenario

An online shop fulfils every order through the same six steps, in the same
order, whatever it is selling.

| Step | What it means |
| --- | --- |
| Validate | Refuse anything that cannot be fulfilled at all |
| Reserve | Make sure the goods are actually available |
| Charge | Take the customer's money |
| Pack | Get the goods ready to leave |
| Dispatch | Hand them over, and produce a reference the customer can chase |
| Notify | Tell the customer, quoting that reference |

The order of those six is not a style choice. Charging before reserving means
taking money for goods you cannot supply. Notifying before dispatching means
sending an email about a consignment number that does not exist yet.

What *does* vary is the middle of each step, and it varies a lot. The store
has three fulfilment routes:

| Route | Reserve | Charge | Pack | Dispatch |
| --- | --- | --- | --- | --- |
| Own warehouse | Hold stock at Reading | Full subtotal | Box and label it | Courier consignment |
| Marketplace seller | Ask the seller to confirm | Subtotal, minus 12% commission | The seller's job | Queue a job for them |
| Digital download | Nothing to reserve | Full subtotal | Nothing to pack | Mint a licence key |

And one of them does not even have a shipping address to validate.

## The Obvious First Move

Write each route out. Three methods, or three classes; either way, each one
says what it does from beginning to end and can be read without looking
anywhere else.

```java
public FulfilmentReport fulfilDigital(Order order) {
    // validate
    // reserve  -- nothing to reserve
    // charge
    // pack     -- nothing to pack
    report.notified("... ready to download. Key: " + report.dispatchReference());
    report.dispatchedAs(LicenceKeys.mint(order));
}
```

Be fair to this. It is a third of the code of the alternative, it needs no
vocabulary to read, and on the day it was written it was almost certainly
correct. Three copies of a six-step sequence is not, on its own, a crisis.

## Where It Breaks

The sequence exists only as a **convention**, repeated by hand in three
places. Nothing in the language, the compiler or the test suite knows the six
steps have an order at all. So the copies drift — not dramatically, but one
line at a time, in whichever copy somebody last edited in a hurry.

### The customer who is emailed a key that does not exist

Look again at the snippet above. The last two lines are the wrong way round.
The email is composed before `dispatchedAs` has run, so it quotes the
placeholder:

```
sam@example.com: Order D-9001 is ready to download. Key: (not dispatched)
```

The key is minted a microsecond later and is perfectly correct. Nobody is
ever told what it is. Nothing throws, nothing fails to compile, and the
order is marked fulfilled.

### The customer who is charged for an order that is refused

In the marketplace copy, the charge moved above the seller confirmation.

```
charge   £42.00 taken
reserve  Acme Optics will not confirm T-410   -> FulfilmentException
```

The exception is correct and the refusal is correct. The money has already
gone.

### And a seventh step that has to be added three times

The day the store adds a fraud check, somebody has to find all three copies
and insert it in the same place in each. The compiler will not help: a copy
that is missing the step is not an error, it is just a route that does not
run it.

## Why the Obvious Fixes Do Not Hold

**"Extract the common bits into helper methods."** Worth doing, and it is
not enough. Helpers remove the duplicated *bodies*; the thing that is
actually duplicated and actually drifting is the **call order**, and a helper
cannot own that.

**"Write a test that checks all three do the same steps."** Better — and this
project has exactly that test. But a test tells you the order broke after
somebody broke it. It does not stop a fourth route being written with the
steps in a new order by an author who never saw the test.

**"Put the whole sequence in one method with an `if` per route."** Now the
order is in one place, which is the right instinct. But every route's
specifics are in there with it, the method grows a branch per route, and
adding click-and-collect means editing a method that already works for three
other routes — the exact change the open/closed principle exists to avoid.

**"Compose it: pass in six lambdas."** This genuinely works and is worth
knowing — it is Strategy, and for many problems it is the better modern
answer. It costs you the thing being bought here, though: nothing forces a
caller to supply all six, in this order, and there is no natural home for a
step whose default is "do the usual". Where the sequence is the invariant and
the steps are not independently swappable at runtime, inheritance expresses
it more directly.

## What Is Actually Missing

Every one of these problems has the same root: **the sequence is not owned by
anybody.** It is a shape that lives in three method bodies and in the head of
whoever wrote them. Nothing can enforce it, because nothing *is* it.

## What the Design Must Deliver

1. **The sequence is written once**, in one method, and that method is the
   only thing that decides the order.
2. **A route cannot change the order**, however much it might want to — not
   by overriding, not by accident.
3. **Steps that genuinely differ are holes** the route must fill in.
4. **Steps with a sensible default cost a route nothing** if it wants the
   usual behaviour.
5. **A route can opt out of behaviour it cannot support** — an order with no
   address — without weakening that behaviour for every other route.
6. **A fourth route is one new class**, with no change to the base class and
   no change to any existing route.

That is [the Template Method pattern](template-method-pattern-explained.md).
