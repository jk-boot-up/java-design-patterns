# Problem Statement — Undo in a Shopping Cart

## The Scenario

An online shop wants its cart to behave like every other piece of software
a customer has ever used: **an edit can be taken back.**

The edits are ordinary.

| Edit | What it does |
| --- | --- |
| Add an item | Puts a product in the cart, or increases a line that is already there |
| Remove an item | Takes a whole line out |
| Change a quantity | Sets a line to a different number |
| Apply a coupon | Puts a discount code on the cart — at most one applies |

Support asks for something else at the same time: when a customer phones
about a total they did not expect, they want to see **what was done to that
cart, in order**.

## The Obvious First Move

Edit the cart directly, and push a note of what you just did onto a stack so
you can reverse it later.

```java
public void addItem(String sku, String name, Money unitPrice, int quantity) {
    cart.putLine(new CartLine(sku, name, unitPrice, cart.quantityOf(sku) + quantity));
    changes.push(new Change("add", sku, quantity));
}

public boolean undo() {
    Change change = changes.pop();
    switch (change.kind()) {
        case "add" -> cart.removeLine(change.sku());
        case "coupon" -> cart.setCoupon(null);
        ...
    }
}
```

Be fair to this. It is short, it is obvious, and for a cart that only ever
gains new lines it is *correct*. This is what a competent developer writes
first, and it ships.

## Where It Breaks

The bug is not in the switch. It is in the note.

**The note records what was asked for. Undo needs to know what was there
before.** Those are the same thing right up until an edit's effect depends on
the state it found — and then they are not.

### The customer who loses three headphones

```
cart: 3 x Wireless headphones
add 2 more            ->  cart: 5 x Wireless headphones
undo                  ->  cart: (empty)
```

`"add"` undoes to `removeLine`, which is right when the line was new and
catastrophic when it was not. The customer asked to take back *their two* and
lost the three they chose ten minutes ago. Nothing throws. The total is
simply wrong, and the only person who notices is the customer.

### The customer who loses a discount

```
cart: coupon WELCOME10
apply BLACKFRIDAY     ->  cart: coupon BLACKFRIDAY
undo                  ->  cart: no coupon
```

A cart holds one coupon, so applying the second *replaced* the first.
Undoing by clearing it is correct nine times in ten and silently expensive
the tenth.

### And the audit trail nobody can read

`Change("add", "H-100", 2)` is not "what happened to this cart". Rendering
it for support means a second `switch`, in a different file, that has to be
kept in step with the first.

## Why the Obvious Fixes Do Not Hold

**"Put more fields on the note."** Add `previousQuantity`. Add
`previousCoupon`. Add `previousPosition` for removals. The note becomes a
union of every field any edit might need to reverse itself, most of them
null on any given instance, and each new kind of edit widens it for
everybody.

**"Add a case to the switch."** There is now one switch to apply and one to
undo, plus one to render, and they must agree. A new edit means finding all
three. The compiler will not remind you: a missing case is a `default`, and
the honest default is to do nothing.

**"Snapshot the whole cart before each edit."** This genuinely works and is
worth knowing — it is the Memento pattern. It costs a full copy per
keystroke, gives you no record of *what changed*, and cannot be replayed
against a different cart. For a cart it is defensible; for the general case
it is why undo is usually built the other way.

## What Is Actually Missing

Every one of these problems has the same root: **the edit is not a thing.**
It is a method call, and a method call that has returned cannot be asked
anything. It cannot describe itself, it cannot reverse itself, and it cannot
be put in a list.

## What the Design Must Deliver

1. **An edit is an object** that carries out the change and knows how to
   reverse it.
2. **Undo is exact**, including when the edit merged into an existing line or
   replaced an existing coupon.
3. **Undo restores position**, not just content — a line that was second
   comes back second.
4. **The thing that runs the edits never names any of them.** No switch, no
   `instanceof`, no list of kinds.
5. **A fifth kind of edit is one new class**, compiled against nothing but
   the interface, with no change to the cart or to the history.
6. **The audit trail falls out of the design**, because the edits are already
   objects that can say what they are.

That is [the Command pattern](command-pattern-explained.md).
