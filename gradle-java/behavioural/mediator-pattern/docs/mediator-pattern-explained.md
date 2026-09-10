# The Mediator Pattern, Explained

> **Define an object that encapsulates how a set of objects interact. Mediator
> promotes loose coupling by keeping objects from referring to each other
> explicitly, and it lets you vary their interaction independently.**
> — *Design Patterns*, Gamma, Helm, Johnson and Vlissides, 1994

"Keeping objects from referring to each other explicitly" is the mechanism.
"Encapsulates how a set of objects interact" is the payoff, and it is the
bigger of the two: after this refactoring there is one file you can open and
read to know what the page does.

## Five References Instead of Nine

Before — every widget holds the widgets it affects:

```java
country.wire(shipping, giftWrap, total, placeOrder);
shipping.wire(giftWrap, total, placeOrder);
giftWrap.wire(shipping, total);
```

After — every widget holds the form, and the form holds every widget:

```java
private final CountrySelector country = new CountrySelector(this);
private final ShippingSelector shipping = new ShippingSelector(this);
private final GiftWrapCheckbox giftWrap = new GiftWrapCheckbox(this);
private final TotalLabel total = new TotalLabel(this);
private final PlaceOrderButton placeOrder = new PlaceOrderButton(this);
```

Both forms behave the same on a straight run through. The difference shows up
when the shopper changes their mind, and it shows up again the day somebody
adds a sixth control.

## Everyday Analogy: The Control Tower

Aircraft near an airport do not negotiate with each other. There is no
protocol by which the inbound 737 asks the departing A320 to wait. They all
talk to the tower, the tower knows where everything is, and the tower tells
each one what to do.

That is not because pilots cannot be trusted. It is because *n* aircraft
talking to each other is *n*² conversations, and one of them will be missed.
One tower is *n* conversations, and the rules of the airspace are in one head.

`CheckoutForm` is the tower. A widget's entire vocabulary is "something about
me changed"; what that means for the rest of the form is not its business, and
it has no reference with which to make it its business.

## Participants

| Role | In the GoF book | Here |
| --- | --- | --- |
| Mediator | `Mediator` | `CheckoutMediator` — one method, `changed` |
| ConcreteMediator | `ConcreteMediator` | `CheckoutForm` — owns the widgets and all the rules |
| Colleague | `Colleague` | `FormWidget` — holds a name and a mediator, and nothing else |
| ConcreteColleague | `ConcreteColleague` | `CountrySelector`, `ShippingSelector`, `GiftWrapCheckbox`, `TotalLabel`, `PlaceOrderButton` |
| The trap | — | `NaiveCheckoutForm` — the same page, wired widget-to-widget |

## Code Walkthrough

### The mediator interface

```java
public interface CheckoutMediator {
    void changed(FormWidget source);
}
```

One method. A mediator's interface is small because colleagues are meant to
*report*, not to *ask*. If you find yourself adding `getShippingPrice()` to
this interface, the widgets have started asking questions again and the
coupling is coming back in through the front door.

### The colleague base

```java
public abstract class FormWidget {
    private final String name;
    private final CheckoutMediator mediator;

    protected void announceChange() {
        mediator.changed(this);
    }
}
```

Two fields, and the important one is the one that is not there. A widget has
no field capable of holding another widget, so the tangle is not merely
discouraged — it is unrepresentable without editing this class.

### A colleague

```java
public void select(String country) {
    this.country = country;
    announceChange();
}
```

That is the whole of `CountrySelector.select`. Compare it with
`NaiveCountry.select`, which is four statements about four other widgets and
is still missing two.

### The mediator

```java
@Override
public void changed(FormWidget source) {
    if (source == country) {
        shipping.showOptions(methodsFor(country.country()));
        giftWrap.setAvailable(isDomestic(country.country()));
    }
    refreshTotal();
    refreshButton();
}
```

Read that and you have read the behaviour of the checkout page. Two things
are worth pausing on.

**`refreshTotal()` and `refreshButton()` run on every change, unconditionally.**
Nothing works out whether they *need* to run. That is what makes the tangled
version's second bug impossible here: the mediator never has to notice that
clearing the shipping method affects the button, because it re-asks the
question every single time. Recomputing everything is cheap, and "cheap and
always right" beats "clever and sometimes stale".

**The `if` is the only branch.** Only a country change reshapes the form; the
other two only move the price. One conditional, in one method, is the entire
control flow of the page.

### Withdrawing and clearing cannot be separated

```java
void setAvailable(boolean available) {
    this.available = available;
    if (!available) {
        this.ticked = false;
    }
}
```

There is no way to withdraw gift wrapping and leave the tick behind, because
there is no method that does only the first half. This is the fix for the
tangled version's first bug, and note that it is not "we remembered to also
untick it" — it is that the two are one operation.

### Push, don't pull

`showOptions`, `setAvailable`, `show` and `setEnabled` are package-private.
The mediator pushes state into the widgets; nothing outside the package can,
so no caller can put the form into a state the mediator did not sanction. The
public methods — `select`, `tick` — are the shopper's, and every one of them
ends in `announceChange()`.

## Why the Tests Are the Proof

**The isolation is asserted, not claimed.** `WidgetIsolationTest` walks every
field of every widget by reflection and fails if any of them has a `FormWidget`
type. A comment saying "widgets must not reference each other" survives
exactly as long as the first person in a hurry; this does not.

**The naive bugs are pinned in place.** `NaiveCheckoutFormTest` asserts the
*wrong* answers — £42 including phantom gift wrap, an enabled button with no
courier — with messages saying so. Fixing `NaiveCheckoutForm` breaks its own
tests, which is the intended behaviour: the cost of that design is meant to be
stated out loud by the build.

**The same scenario is run through both forms.** The last test in that file
puts the mediated form through the identical clicks and asserts it gets both
right, so the comparison is not rhetoric in a README.

## What You Gain

- **The rules are in one place.** One method to read, one place to change,
  one place to review.
- **Linear wiring.** A sixth control adds one reference, not five.
- **Widgets become testable and reusable.** `CountrySelector` needs a
  mediator, not four siblings.
- **No circular dependencies.** All the arrows point the same way.
- **Whole-form invariants become expressible.** "The button is enabled only
  when the form is complete" is a sentence you can write in one method,
  because one object can see the whole form.

## What to Watch Out For

**The mediator becomes a god object.** This is the real cost and it is not
hypothetical. Every rule you take out of the widgets goes into the mediator,
and a large form can produce a very large one. Split it — one mediator per
logical section of the page — before it becomes the class nobody wants to
open.

**Don't let colleagues start asking.** The moment a widget calls a getter on
the mediator to find out about another widget, you have the old coupling with
an extra hop. Colleagues report; the mediator decides.

**Beware of change storms.** If a mediator's reaction to a change sets a
widget in a way that announces another change, you can loop. This project
avoids it by having the mediator's push methods be package-private and silent
— `showOptions` deliberately does not call `announceChange()`.

**Don't reach for it on a form with two controls.** Two widgets that affect
each other, and will never be joined by a third, are clearer wired directly.
The pattern earns its keep somewhere around four or five interacting parts,
which is exactly where it stops being possible to hold the wiring in your head.

## Mediator vs. Observer vs. Facade

| | What it does | Who knows whom |
| --- | --- | --- |
| **Mediator** | Centralises the *interaction* between peers | Colleagues know the mediator; the mediator knows all of them |
| **Observer** | Broadcasts an event to whoever is listening | Publisher knows nothing about subscribers |
| **Facade** | Simplifies a subsystem for outside callers | Facade knows the subsystem; the subsystem knows nothing |

Mediator and Observer are often confused because both remove direct
references. The distinction is direction and knowledge: an
[Observer](../observer-pattern) publisher deliberately knows *nothing* about
its subscribers, whereas a mediator knows all its colleagues on purpose —
that knowledge is what lets it enforce rules that span several of them. A
publisher could not disable a button because a drop-down was cleared; a
mediator can, and that is the job.

A [Facade](../../structural/facade-pattern) also sits in front of several
objects, but it faces outwards: it exists to simplify life for a *caller*
outside the subsystem. A mediator faces inwards, and its colleagues are the
ones it serves.

## Where You Have Already Seen It

Every GUI framework. Swing's `ActionListener` on a dialog is usually a
mediator wearing a different hat — the dialog listens to its own controls and
updates the others. Android's `ViewModel` and Redux's store are the same idea
at a larger scale. `java.util.Timer` mediates between tasks and threads. Chat
servers are the textbook case: participants do not hold each other, the room
holds all of them.

## Try It Yourself

1. Add a voucher-code field that takes £5 off, and make gift wrap free when a
   voucher is applied. Count how many files you touch here, then count how
   many you would touch in `NaiveCheckoutForm`.
2. Give `CountrySelector` a field of type `TotalLabel` and run the tests.
   `WidgetIsolationTest` should name the offending field.
3. Make `showOptions` call `announceChange()` and watch what happens. That is
   the change storm, and it is worth seeing once.
4. Split `CheckoutForm` into a delivery mediator and a payment mediator, and
   decide how the two should talk to each other.

## See Also

- [`problem-statement.md`](problem-statement.md) — the problem in full
- [`class-diagram.md`](class-diagram.md) — static structure
- [`uml-diagram.md`](uml-diagram.md) — the call sequence for one click
- [Observer](../observer-pattern) — the pattern this is most often confused with
- [Facade](../../structural/facade-pattern) — the other "one object in front of
  many", facing the other way
