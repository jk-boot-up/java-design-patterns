# The State Pattern, Explained

> **Intent (GoF).** Allow an object to alter its behaviour when its internal
> state changes. The object will appear to change its class.

That last sentence is the one to hold on to. Not "the object has a status
field" — *the object appears to change its class*. A `SHIPPED` order and a
`PLACED` order are the same `Order` instance, but they accept different
messages and do different work with them, which is exactly what having a
different class would mean.

## The Thing A Status Field Cannot Do

A status field spreads one lifecycle across every method that reads it. Six
methods, six chains of conditionals, each phrased in whichever direction its
author found natural:

```java
public void cancel(String reason) {
    if (status == Status.DELIVERED || status == Status.CANCELLED
            || status == Status.REFUNDED) { ... refuse ... }
    ...
}

public void refund(String reason) {
    if (status != Status.DELIVERED && status != Status.CANCELLED) { ... refuse ... }
    ...
}
```

One is a blocklist, the other an allowlist. Both are correct on the day they
are written. Neither tells you what a `SHIPPED` order can do, because the
answer to that question is scattered across six methods and can only be
recovered by reading all of them and doing the boolean algebra in your head.

So the copies drift. `cancel` quietly lets a parcel that is on a van be
refunded; `refund` was widened to include `CANCELLED` and now pays the customer
twice; and a third copy, written for the screen, is right and disagrees with
both. The demo's section 1 runs all three.

The pattern's move is to invert the axis. Instead of *one method, all states*,
write *one state, all methods*.

## Everyday Analogy: The Vending Machine

A vending machine with no coins in it and a vending machine holding £1.50 are
the same machine, and pressing the same button does something different. You
would not describe the machine as having "a mode integer". You would say it is
*waiting for money* or *ready to dispense*, and the buttons that do nothing in
one condition are the ones that work in the other.

Nobody chooses the machine's condition from outside. It arrives there because
of what it just did — a coin went in, a can came out. That is the difference
between this and Strategy, and it is worth having the image in mind before the
code.

## Participants

| Role | Here | Job |
| --- | --- | --- |
| **Context** | `Order` | Holds the current state, forwards every request to it, and offers `transitionTo` for the states to use |
| **State** | `OrderState` | Declares the six requests, and refuses all of them by default |
| **Concrete states** | `PlacedState`, `PaidState`, `PackedState`, `ShippedState`, `DeliveredState`, `CancelledState`, `RefundedState` | Override the requests that state accepts; do the work; name the successor |
| **Supporting cast** | `Ledger`, `OrderEvent`, `IllegalTransitionException` | Where the money, the audit trail and the refusals go |
| **The trap** | `NaiveOrder` | The same lifecycle as an enum and three chains, drifted |

## The Design in Three Decisions

### 1. Every request has a refusing default

```java
public interface OrderState {
    String name();
    List<String> allowedActions();

    default void pay(Order order)     { throw refuse("pay"); }
    default void pack(Order order)    { throw refuse("pack"); }
    default void ship(Order order)    { throw refuse("ship"); }
    default void deliver(Order order) { throw refuse("deliver"); }
    default void cancel(Order order, String reason) { throw refuse("cancel"); }
    default void refund(Order order, String reason) { throw refuse("refund"); }
}
```

This is the single most important line of design in the project. A state does
not list what it forbids; it lists what it allows, by overriding. Everything
else refuses automatically.

The consequence: **a rule nobody wrote is a refusal, not an accident.** In the
enum version, forgetting to add a state to a guard *opens* a transition —
which is precisely how `SHIPPED` became cancellable. Here, forgetting to
override *closes* one. The failure mode points the safe way.

`refuse` builds its own message out of `allowedActions()`, so the explanation
cannot go stale:

```
cannot refund a SHIPPED order: the only thing it will accept is deliver
cannot refund a CANCELLED order: it is final, and nothing more can happen to it
```

### 2. The context has no conditionals at all

Every public method on `Order` is one line:

```java
public void ship() { attempt("ship", state -> state.ship(this)); }

private void attempt(String action, Consumer<OrderState> request) {
    String from = state.name();
    try {
        request.accept(state);
    } catch (IllegalTransitionException e) {
        history.add(OrderEvent.refused(action, from, e.reason()));
        throw e;
    }
}
```

`Order` does not know there are seven states, does not know their order, and
contains no `if` that mentions a status. What it *does* own is the audit
trail: a refusal is recorded on the way past and then rethrown, so "somebody
tried to cancel this after it shipped" is in the history whether or not it
succeeded.

### 3. States name their successors

```java
// PackedState
public void ship(Order order) {
    String consignment = "CON-" + order.id();
    order.recordConsignment(consignment);
    order.transitionTo(ShippedState.INSTANCE, "ship",
            "courier collected, consignment " + consignment);
}
```

The transition is the last thing the method does, after the work. The order
becomes shipped *because* a courier collected it — the state change is a
consequence, not a setting.

`transitionTo` is package-private. From outside, an order's state changes only
as the result of asking it to do something.

## Behaviour, Not Just Permission

If the states differed only in which calls they allowed, this would be an
over-engineered enum. Look at `cancel` in three of them:

```java
// PlacedState — nothing was ever taken
order.transitionTo(CancelledState.INSTANCE, "cancel",
        reason + " — nothing had been charged");

// PaidState — give the money back
Money back = order.ledger().charged().minus(order.ledger().refunded());
order.ledger().refund(back);
order.transitionTo(CancelledState.INSTANCE, "cancel",
        reason + " — refunded " + back + ", nothing had shipped");

// PackedState — give the money back and undo the packing
order.ledger().refund(back);
order.transitionTo(CancelledState.INSTANCE, "cancel",
        reason + " — refunded " + back + ", box opened and stock returned");
```

Three different bodies for one verb. In the enum version these are three
branches of one method that were, at some point, one branch — and the day
somebody merges them again "because they are nearly the same", the stock stops
going back on the shelf.

`ShippedState` then refuses `cancel` outright, with a reason a support agent
can read:

```java
@Override
public void cancel(Order order, String reason) {
    throw refuse("cancel", "it is already with the courier — the customer "
            + "must refuse delivery or return it");
}
```

Note that this one *is* an explicit override. The default refusal would have
said "the only thing it will accept is deliver", which is true but unhelpful.
When a refusal has a reason worth telling a human, write it down.

## The Screen and the Endpoint Agree

`allowedActions()` is on the state, next to the methods it describes:

```java
// PackedState
public List<String> allowedActions() { return List.of("ship", "cancel"); }
```

```
PLACED     [pay, cancel]
PAID       [pack, cancel]
PACKED     [ship, cancel]
SHIPPED    [deliver]
DELIVERED  [refund]
REFUNDED   []
```

In the naive version this list is a *third copy* of the rules, and it is the
copy that disagrees: it correctly says a shipped order can only be delivered,
while `cancel()` accepts the call. The button is not drawn and the endpoint
takes it anyway.

Here they cannot disagree, and `OrderLifecycleTest` proves it rather than
asserting it — it walks all seven states and all six actions, and checks that
`canDo(action)` predicts whether the call throws, forty-two times:

```java
boolean offered  = order.canDo(action);
boolean accepted = accepts(order, action);
assertEquals(offered, accepted,
        state.name() + " offers " + action + "=" + offered + " but accepts=" + accepted);
```

## The Eighth State

The demo declares a state that does not exist in `src/main`:

```java
OrderState awaitingCollection = new OrderState() {
    public String name() { return "AT-LOCKER"; }
    public List<String> allowedActions() { return List.of("deliver"); }
    public void deliver(Order order) {
        order.transitionTo(DeliveredState.INSTANCE, "deliver",
                "collected from the Bristol locker");
    }
};
```

It refuses `pay`, `pack`, `ship`, `cancel` and `refund` without a line of code
saying so, and `Order` — compiled before it existed — accepts it. That is the
open/closed argument, made concretely.

Read the cost in the same breath, though: adding a real `AT-LOCKER` means
editing whichever state hands over to it. New states are cheap; new *arrows*
are not.

## Why the Tests Are the Proof

`NaiveOrderTest` is the unusual one. Its tests **pass**, and what they assert
is the bug:

```java
@Test
void andTheShopPaysTheCustomerTwice() {
    NaiveOrder order = order();
    order.pay();
    order.cancel("out of stock");

    order.refund("support ticket 4471");

    assertEquals(2, order.ledger().refundCount());
    assertEquals(TOTAL.times(2), order.ledger().refunded());
}
```

Each such test is paired with the same scenario run through `Order`:

```java
@Test
void theSameScenarioIsRefusedByTheStateVersion() {
    order.pay();
    order.cancel("out of stock");

    assertThrows(IllegalTransitionException.class,
            () -> order.refund("support ticket 4471"));
    assertEquals(1, order.ledger().refundCount());
}
```

Two tests, same story, different endings. That pairing is the argument for the
pattern, and it is executable.

## What You Gain

* **One place per state.** Everything true about `PACKED` is in one file.
* **Refusal by default.** The rule you forgot to write is the safe one.
* **Behaviour, not just guards.** Different states can do genuinely different
  work for the same verb, and that is visible rather than buried in a branch.
* **One answer for the screen and the endpoint.**
* **A new state without touching the context.**
* **Refusals that explain themselves**, built from the state's own data.

## What to Watch Out For

* **The transition table is gone.** In the enum version you could read the
  whole lifecycle in one screen. Here it is distributed across seven files,
  one arrow at a time. If your machine is small and stable, that is a real
  loss and the enum may simply be better. This project says so in its own
  demo.
* **States that need data.** These are stateless, hence one shared `INSTANCE`
  each. The moment a state needs a field, that goes away and you are
  allocating a state per order — check that it is worth it.
* **Persistence.** You store `"PACKED"`, not an object. Something has to map
  the stored name back to a state, and that mapping is a place where a new
  state can be forgotten.
* **Class explosion.** Seven classes for seven states is honest here because
  the behaviour differs. Seven classes that each override one method
  identically is not.
* **States knowing too much about each other.** Every state referencing every
  other is a fully connected graph. Keep each one pointing only at where it
  can actually go.

## State vs. Strategy vs. Command

| | State | Strategy | Command |
| --- | --- | --- | --- |
| What varies | What the object will accept, and what it does | How one job is done | Which request is made |
| Who chooses | The object, as a consequence | The caller | The caller |
| Changes over time | Yes, that is the point | Rarely | Each call is a new object |
| Implementations reference each other | Yes | No | No |

State and Strategy have **the same class diagram**. Any explanation that
distinguishes them by structure is wrong, because there is no structural
difference to find. The difference is intent and control: a Strategy is chosen
by the caller and does not change itself; a State is entered as a consequence
of what the object did, and states hand control to one another.

## Where You Have Already Seen It

* `java.lang.Thread.State` is the enum version of exactly this problem, and
  the JDK's thread implementation is the class version of it.
* `Matcher` behaves differently before and after `find()`.
* HTTP client builders that refuse `body()` on a `GET`.
* Any workflow engine, order management system or payment gateway — the
  lifecycle above is not a teaching example, it is the actual shape of the
  domain.

## Try It Yourself

1. Add a `RETURN_REQUESTED` state between `DELIVERED` and `REFUNDED`. Notice
   what you have to edit: the new class, and `DeliveredState`. Nothing else.
2. Give `ShippedState` a `lose()` transition to a new `LOST` state that
   refunds. Then find every place the enum version would have needed a branch.
3. Delete the `default` bodies from `OrderState` and make the methods
   abstract. Count how many methods you now have to write, and decide whether
   the compiler's help was worth it.
4. Persist an order: write `String` out, read it back, and see where the
   name-to-state mapping wants to live.

## See Also

* [Problem statement](problem-statement.md) — the drift, with the ledger
* [Prerequisites](prerequisites.md) — including the State/Strategy table
* [Class diagram](class-diagram.md) and [sequence diagram](uml-diagram.md)
* [Strategy pattern](../../strategy-pattern/README.md) — same picture, other
  intent
