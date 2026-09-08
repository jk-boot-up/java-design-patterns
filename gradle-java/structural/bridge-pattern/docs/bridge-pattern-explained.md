# The Bridge Pattern — Explained

## One-Line Definition

> **Bridge** decouples an abstraction from its implementation so that the
> two can vary independently.
> — *Gang of Four, Design Patterns*

It is a **structural** pattern: it is about how two hierarchies are wired
*together*, not about how objects are created (Singleton, Prototype,
Builder) or how a tree of objects is composed (Composite).

## The One Idea That Matters: Two Small Hierarchies, One Seam

Without Bridge, "what a notification says" and "how it gets delivered" are
forced into one class per combination: `OrderConfirmationEmail`,
`OrderConfirmationSms`, `ShippingUpdateEmail`, `ShippingUpdateSms`, and so
on. Bridge splits that single tangled hierarchy into two small,
independent ones — `Notification` (the *abstraction*) and `MessageChannel`
(the *implementor*) — connected by nothing more than a field. A
`Notification` holds a `MessageChannel` reference and calls it; it never
subclasses per channel.

> If adding a new channel means writing a new class for every existing
> notification type (or vice versa), the pattern has not been applied yet.

## The Everyday Analogy

Think of a **TV remote and a television**. The remote (the abstraction)
knows about "volume up," "channel up," "power" — high-level actions. The
television (the implementation) knows how to actually change the volume on
its own specific hardware. Any remote works with any television that
speaks the same signal, and a manufacturer can redesign the television's
internals completely without changing what a single button on the remote
means. The remote and the television vary independently because neither
one is a subclass of the other — they are two separate hierarchies, joined
by one wire.

`Notification` is the remote. `MessageChannel` is the television.

## The Participants

| Role | In this project | Job |
| --- | --- | --- |
| **Abstraction** | `Notification` | Knows what a message says; holds a `MessageChannel` and delegates delivery to it |
| **Refined Abstraction** | `OrderConfirmationNotification`, `ShippingUpdateNotification`, `PasswordResetNotification` | Each composes its own subject/body; none know how delivery works |
| **Implementor** | `MessageChannel` | Declares how to deliver a subject/body pair somewhere |
| **Concrete Implementor** | `EmailChannel`, `SmsChannel`, `PushChannel` | Each knows one delivery mechanism's quirks (SMS truncates, Push drops the body) |
| **The trap** | `NaiveOrderConfirmationEmail` / `...Sms`, `NaiveShippingUpdateEmail` / `...Sms` | One class per (notification, channel) pair; channel logic duplicated across every notification type |
| **Client** | `NotificationDemo` | Mixes any notification with any channel at construction time |

## How This Project Implements It

### The abstraction holds the implementor, and only delegates

```java
public abstract class Notification {
    private final MessageChannel channel;

    protected Notification(MessageChannel channel) {
        this.channel = channel;
    }

    public final void send(String recipient) {
        channel.deliver(recipient, subject(), body());
    }

    protected abstract String subject();
    protected abstract String body();
}
```

`send` never knows whether `channel` is email, SMS, or something invented
next year. It only knows `MessageChannel` can `deliver` a subject and a
body.

### Refined abstractions add content, never delivery

```java
public final class OrderConfirmationNotification extends Notification {
    @Override protected String subject() { return "Order " + orderId + " confirmed"; }
    @Override protected String body()    { return "Your order " + orderId + " totalling $" + total + " has been confirmed."; }
}
```

Nothing here mentions email, SMS, or push. Adding a fourth notification
type — say, `BackInStockNotification` — costs exactly one new class, and it
automatically works with every channel that already exists.

### Concrete implementors own delivery quirks, once each

```java
public final class SmsChannel implements MessageChannel {
    @Override
    public void deliver(String recipient, String subject, String body) {
        String text = subject + ": " + body;
        if (text.length() > MAX_LENGTH) {
            text = text.substring(0, MAX_LENGTH - 1) + "…";
        }
        System.out.println("[SMS to " + recipient + "] " + text);
    }
}
```

The 140-character truncation rule is written exactly once, here. Every
notification type that goes out over SMS — today's three, and any added
later — gets that rule for free, because they all share this one
`SmsChannel` instance.

### The trap, for contrast

`NaiveOrderConfirmationSms` and `NaiveShippingUpdateSms` both hardcode the
same truncation logic, independently. Fixing a bug in how SMS truncates
means finding and fixing it in every naive class that happened to copy it.

## What You Gain

- **Independent growth on both axes.** A new channel costs one class. A
  new notification type costs one class. Neither multiplies against the
  other.
- **Delivery logic lives in exactly one place per channel.** The SMS
  length limit is defined once, in `SmsChannel`, and every notification
  type that uses SMS inherits the fix automatically.
- **Runtime flexibility.** Because the connection between a `Notification`
  and its `MessageChannel` is an ordinary object reference, not an
  inheritance relationship, the same `OrderConfirmationNotification` class
  can be pointed at `EmailChannel`, `SmsChannel`, or `PushChannel` just by
  passing a different constructor argument.
- **The trap and the fix compute identical output.** `NaiveNotificationsTest`
  proves the naive classes and the bridge equivalents produce
  byte-for-byte the same delivered message — Bridge changes *how the code
  is organized*, not what it produces.

## What to Watch Out For

- **Bridge only pays off with two genuinely independent axes of
  variation.** If you will only ever have one channel, or one notification
  type, the extra interface is pure ceremony — introduce it when the
  second axis actually shows up, not preemptively.
- **The abstraction must not leak implementor details.** If
  `OrderConfirmationNotification` had to know that `SmsChannel` truncates
  at 140 characters in order to compose a shorter body, the two
  hierarchies would no longer be independent — the whole point is that
  `Notification` subclasses stay ignorant of channel mechanics.
  Confirm this by keeping `subject()`/`body()` free of any per-channel
  logic.
- **A `final` implementor field means the channel is fixed at
  construction.** That is a deliberate, simple choice for this project;
  some Bridge implementations expose a setter so an abstraction's
  implementor can be swapped after construction. Either is valid Bridge —
  the pattern only requires the *connection* to be composition, not which
  connection is mutable.

## Bridge vs. Similar Patterns

| Pattern | Intent | Key difference |
| --- | --- | --- |
| **Bridge** | Decouple an abstraction from its implementation so both vary independently | Two parallel hierarchies, connected by composition, designed in *up front* |
| **Adapter** | Make an existing incompatible interface usable by a client | Applied *after the fact*, to reconcile something you didn't design |
| **Composite** | Treat a single object and a tree of objects uniformly | One interface, recursive part-whole structure — no second hierarchy |
| **Strategy** | Swap an algorithm at runtime | Same shape as Bridge (composition over inheritance), but usually one interchangeable behavior, not a whole second hierarchy of refined types |

The shortest way to remember it: **Adapter reconciles two interfaces that
already exist and disagree. Bridge designs two hierarchies from the start
so they never have to agree on more than one seam.**

## Where You Have Already Seen It

- JDBC — `java.sql.Driver` is the implementor; your code talks to the
  `Connection`/`Statement` abstraction and never touches vendor-specific
  driver internals directly
- SLF4J and other logging facades — the logging API (abstraction) is
  separate from the logging backend (Logback, Log4j2 — the implementors)
- Cross-platform UI toolkets — a `Button` abstraction paired with a
  platform-specific `ButtonRenderer` implementor, so the same `Button`
  code runs on Windows, macOS, or the web
- Device drivers — the operating system's abstraction for "a printer"
  stays stable while manufacturers implement wildly different hardware
  underneath

## Try It Yourself

1. Run `./gradlew run` and read the output — notice the same
   `OrderConfirmationNotification` content renders differently through
   `EmailChannel`, `SmsChannel`, and `PushChannel`, with zero `if` statements
   anywhere checking which channel it is.
2. Add a `BackInStockNotification` refined abstraction. Confirm it works
   with `EmailChannel`, `SmsChannel`, and `PushChannel` immediately, with no
   changes to any of the three channel classes.
3. Add a fourth channel, `WebhookChannel`, that delivers as JSON. Confirm
   every existing notification type works with it immediately, with no
   changes to any notification class.

## See Also

- [`problem-statement.md`](problem-statement.md) — the problem this solves
- [`class-diagram.md`](class-diagram.md) — static structure
- [`uml-diagram.md`](uml-diagram.md) — runtime call flow
- [`animation.html`](animation.html) — animated walkthrough
