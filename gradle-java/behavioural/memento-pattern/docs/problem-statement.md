# Problem Statement

## The Scenario

You are building the shopping basket of an online shop, and the ticket says
"add an undo button". Shoppers keep removing the wrong line and then have to
find the product again, so one step back would save them a lot of irritation.

The basket is small. It holds two things:

| State | What it is |
| --- | --- |
| The lines | each one a product, its price, and a quantity |
| The voucher code | applied to the basket as a whole, worth £5 off |

And the shopper can do four things to it: add a line, remove a line, apply a
voucher, and clear the voucher. Undo has to put back whatever the last of those
changed.

That is the entire feature. It sounds like an afternoon's work, and this is one
of those cases where the obvious afternoon's work is subtly wrong.

## Attempt One: Save the State in a Field

The obvious thing is to keep a "before" copy in a field, and put it back when
undo is pressed:

```java
private final List<BasketLine> lines = new ArrayList<>();
private List<BasketLine> savedLines;

public void save() {
    savedLines = lines;
}

public void undo() {
    lines.clear();
    lines.addAll(savedLines);
}
```

Read those two methods and they look like opposites. They are not. You can run
this — `NaiveBasket` is in this project, and `NaiveBasketTest` holds its
behaviour in place.

## Why That Hurts

**`savedLines = lines` does not copy anything.** It writes down *where* the
list is, not *what is in it*. The saved list and the live list are the same
list, so every later add and remove edits the save as well. Then `undo()`
clears the live list — which is also the saved list — and copies the now-empty
saved list back over it. The shopper presses undo and their basket is empty.
Nothing throws.

**The voucher was never saved at all.** Nobody decided not to save it. It
simply was not on anyone's mind on the day undo was written, so undo restores
the lines and silently leaves the voucher wherever it happened to be. There is
no line of code you could review to find that out, because the bug is the
absence of a line.

**Every new field is a new chance to forget.** Add a delivery date next month
and undo goes quietly half-right again, and it will keep doing that once per
field, forever, because nothing connects "the basket's state" to "what undo
saves".

**Or you make the basket's insides public to fix it.** The other common
attempt is to let the undo code reach in — expose the list, expose the
voucher, copy them from outside. That works, and it means anything at all can
now edit a basket's lines. You have bought undo with the basket's
encapsulation, which is a bad trade you only notice much later.

**"Undo by doing the opposite" is worse than it sounds.** Removing a line
undoes an add; what undoes a remove? You have to know which line, and where it
was, and what the voucher was doing at the time. Every new operation needs its
own inverse, and any operation that loses information has no inverse at all.

## The Question This Project Answers

> How do you let something outside the basket save and restore the basket's
> state, without that thing being able to see the state, and without the basket
> having to expose its insides to anyone?

## The Goal

Make undo look like this, and make it keep working when the basket grows a
third field:

```
Basket  ──save()──►  BasketSnapshot  ──held by──►  BasketHistory
   ▲                                                    │
   └──────────────── restore(snapshot) ◄────────────────┘
              (the history never opens it)
```

One class knows what the basket's state is — the basket. One class holds the
copies — the history. Neither has to know anything about the other's job.
