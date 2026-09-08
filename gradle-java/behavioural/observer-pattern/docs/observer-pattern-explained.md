# The Observer Pattern

> **Define a one-to-many dependency between objects so that when one object
> changes state, all its dependents are notified and updated automatically.**
>
> — *Design Patterns*, Gamma, Helm, Johnson and Vlissides (1994)

In plain language: **let the thing that changed announce it, and let whoever
cares sign up.**

## One Announcement, Any Number of Reactions

Four systems care when an order ships. In this project none of them appear in
`Order`:

```java
public final class Order {

    private final List<OrderListener> listeners = new CopyOnWriteArrayList<>();
    private OrderStatus status = OrderStatus.PLACED;

    public void addListener(OrderListener listener) { ... }

    public List<ListenerFailure> moveTo(OrderStatus next) { ... }
}
```

`Order` knows it has listeners. It does not know what they do, how many there
are, or whether there are any at all — an order with an empty list still moves
to `SHIPPED` perfectly happily, and there is a test that says so.

## Remember It With a Newsletter

You subscribe to a shop's newsletter. The shop sends an issue; you get it. It
does not know your name, whether you read it, or what you do afterwards — you
might forward it, you might buy something, you might delete it unread. If a
thousand more people subscribe tomorrow, the shop does not write any new code;
it presses send exactly as before.

And crucially, **you can unsubscribe without asking the shop's permission**.
The relationship is owned by the subscriber, not the publisher.

That is the whole pattern. The publisher's job ends at "I sent it."

## The Participants

| Role | Here | Job |
| --- | --- | --- |
| **Subject** (publisher) | `Order` | Holds the state, keeps the listener list, announces changes |
| **Observer** (listener) | `OrderListener` | The one small interface every subscriber implements |
| **Concrete observers** | `InventoryListener`, `EmailListener`, `AnalyticsListener`, `WarehouseFeedListener` | Independent reactions, each knowing only itself |
| **Event** | `OrderEvent` | What happened, as an immutable value |
| **Failure report** | `ListenerFailure` | One listener that threw, reported rather than swallowed |
| **The trap** | `NaiveOrderService` | The version that calls each system by name |

## The Observer Interface

```java
public interface OrderListener {
    String name();
    void onStatusChanged(OrderEvent event);
}
```

Two methods, and notice what is *not* there. No priority. No ordering hint. No
`shouldHandle(...)` predicate. Every one of those would be a way for a listener
to make claims about the other listeners, and the point of the pattern is that
no listener knows there are any others.

`name()` has no default, so a lambda will not satisfy the interface. That is a
deliberate trade against convenience: an anonymous lambda sitting in a listener
list is untraceable in a stack trace, and this is exactly the kind of code
where a stack trace is all you get at three in the morning.

## The Event Is a Value, Not a Back-Reference

```java
public record OrderEvent(String orderId, OrderStatus from, OrderStatus to) { }
```

The listener receives this and nothing else — no reference back to the `Order`,
no way to ask it a follow-up question, no way to change it. That matters more
than it looks. A listener that can reach into the publisher can change the
publisher's state halfway through a notification, and then whether listener
three sees the old value or the new one depends on the order they were
registered in. The pattern's guarantee dies quietly at that moment.

The GoF book calls the two options *push* and *pull*: push everything the
listener could need into the event, or hand it the subject and let it pull.
This project pushes, and if you ever find yourself writing `event.order()`, be
sure you know why.

## The Notification Loop

```java
public List<ListenerFailure> moveTo(OrderStatus next) {
    if (next == status) {
        return List.of();
    }

    OrderEvent event = new OrderEvent(id, status, next);
    status = next;

    List<ListenerFailure> failures = new ArrayList<>();
    for (OrderListener listener : listeners) {
        try {
            listener.onStatusChanged(event);
        } catch (RuntimeException e) {
            failures.add(ListenerFailure.of(listener, e));
        }
    }
    return List.copyOf(failures);
}
```

Three decisions in eleven lines, each of which is a bug if made the other way.

**Moving to the status it is already in is not an event.** Fire one anyway and
every listener has to defend itself against duplicates, and the listener that
forgets is the one that sends the customer a second "your order has shipped"
email.

**The status is updated before the listeners run.** A listener that does look
at the order should see the world the event describes, not the one it replaced.

**One listener throwing does not stop the next.** This is the fix for the
outage in [`problem-statement.md`](problem-statement.md). Letting the exception
escape means a bug in analytics silently prevents the warehouse feed. Catching
it and doing nothing means the same bug is invisible for weeks. Returning the
failures lets the caller decide, and lets a test assert on it.

## Why `CopyOnWriteArrayList`

Not for threads — for one-shot subscriptions.

A listener is entirely within its rights to remove itself while it is being
notified. "Email me when this ships, then forget me" is the obvious case, and
there is a test for it. Iterating an `ArrayList` while a listener calls
`removeListener` throws `ConcurrentModificationException` from inside the
notification loop, which is a spectacular way to discover a design assumption.
Copy-on-write iterates a snapshot, so a listener added or removed during a
notification simply takes effect from the next one.

It is a real cost — every `addListener` copies the array — and it is the right
one here, because subscriptions are set up once and events fire many times.

## What This Costs

This is the honest part, and it is the part most write-ups skip.

**The call graph becomes invisible.** Under the naive design, reading
`markShipped` tells you the four things that happen. Under this one, reading
`moveTo` tells you *nothing at all* about what happens when an order ships. To
find out you have to find every `addListener` call, and your IDE cannot help
because the call sites are all typed as the interface. That is a genuine loss
of legibility, paid in exchange for a genuine gain in independence.

**Debugging gets harder in exactly the way it always does.** A stack trace from
inside `EmailListener` shows `Order.moveTo` as the caller and gives no clue why
email was on the list. This is why `OrderListener` has a `name()`, and why
`ListenerFailure` reports it.

**Notification order is not a contract.** It happens to be registration order
in this implementation, and a listener that relies on that is broken — it just
does not know yet. If two reactions really must be sequenced, they are one
reaction, and they belong in one listener.

**Memory leaks are the classic failure.** A long-lived subject holding a strong
reference to a short-lived listener keeps it alive forever. In a UI or a
server this is the leak everyone eventually meets. If subscriptions outlive
their subscribers, you need explicit removal or weak references — and this
project's `removeListener` is the whole of its answer.

## When To Use It

Reach for Observer when **one state change has several independent
consequences, and the list of consequences will grow**. If there are two
consequences and there will always be two, call them directly; you will thank
yourself.

The tell is not the number of reactions but their independence. Four things
that must happen in order, where the third needs the second's result, are not
four observers — they are one workflow, and that is the Template Method or
Chain of Responsibility chapter.

## Observer Compared

| Pattern | What varies | Who is in charge |
| --- | --- | --- |
| **Observer** | Who reacts, and how many | The subscribers — they attach themselves |
| **Strategy** | How one job is done | The caller — it picks one and passes it in |
| **Mediator** | Who talks to whom | A central object that knows all the parties |
| **Chain of Responsibility** | Which handler deals with it | The chain — one handler usually stops it |

Observer versus Mediator is the pair worth pinning down. In Observer the
publisher knows nothing and the subscribers know the publisher. In Mediator
there is a hub that knows everyone, on purpose, so that it can coordinate them.
Observer decouples; Mediator centralises.

## Sightings in Real Code

- **`java.util.concurrent.Flow`** — the JDK's reactive-streams API, with
  back-pressure added; `Flow.Subscriber` is `OrderListener` grown up.
- **Spring's `ApplicationEventPublisher`** and `@EventListener` — the same
  shape, with the subscription list assembled by the container.
- **Every UI toolkit ever written** — `addActionListener`, `onClick`,
  `addEventListener`. The pattern is so embedded in UI programming that most
  people learn it without being told its name.
- **`java.util.Observer`** — the JDK's own version, and **deprecated since
  Java 9**. It is worth knowing why: it was not type-safe (`update(Observable,
  Object)`), `Observable` was a class so you had to inherit from it, and it
  said nothing about notification order or thread safety. The pattern was never
  the problem; that implementation of it was.

## Try It Yourself

1. Add a `SupplierListener` that writes a line only for drop-shipped items.
   Note that `Order.java` does not change — that is the whole exercise.
2. Now do the same thing to `NaiveOrderService`. Count the files you touch.
3. Make `EmailListener` remove itself after the delivery message and confirm
   the listener count drops. Then try it with an `ArrayList` in `Order` and
   watch it throw.
4. Give `moveTo` a legal-transition check that refuses `DELIVERED -> PAID`.
   When it starts to feel like the wrong place for it, you have found the
   State pattern.
