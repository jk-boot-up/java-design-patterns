# Session Plan — The Builder Pattern

A guided session for teaching this project to people who are new to design
patterns.

- **Audience:** anyone comfortable writing a Java class. No pattern
  knowledge assumed, though having done the static factory method session
  first helps — this one builds on it.
- **Duration:** ~60 minutes
- **Format:** live coding and discussion. Slides optional; the code is the
  material.
- **Group size:** works from 1 to about 20. Beyond that, the exercises need
  pairs.

> **Optional pre-work.** Ask participants to watch the video
> ([`../video/`](../video/)) beforehand. If they do, you can compress the
> first two blocks and spend the time on the exercises instead.

## Before You Start

Check that every machine can run:

```bash
./gradlew build
```

Have open in tabs: `PurchaseOrder.java`, `PurchaseOrderPresets.java`,
`PurchaseOrderDemo.java`, `animation.html`.

## The One Thing They Should Leave With

If they remember nothing else:

> **A constructor makes you decide the whole object in one call. A builder
> lets you decide it a piece at a time, in any order, and checks it is
> complete only when you say you are done.**

Everything in the session is in service of that sentence.

## Timings

| Time | Block | Goal |
| --- | --- | --- |
| 0:00–0:08 | The constructor with nine parameters | Make them feel the wall |
| 0:08–0:20 | The fix, live | Show the technique |
| 0:20–0:30 | The rule that lives in one place | Why it is more than a rename |
| 0:30–0:38 | The Director, the Java way | Connect to the GoF book honestly |
| 0:38–0:50 | Exercises | Hands on keyboard |
| 0:50–0:58 | When *not* to use it | Honesty and boundaries |
| 0:58–1:00 | Wrap up | The one sentence |

## 0:00–0:08 — The Constructor With Nine Parameters

Open a scratch file. Type this in front of them, live:

```java
public PurchaseOrder(String orderId, String customerId, List<LineItem> items,
                      Address shippingAddress, boolean giftWrapped, String giftMessage,
                      String couponCode, boolean priority, String notes) { ... }
```

Then call it twice:

```java
new PurchaseOrder("ORD-9001", "CUST-100", items, home,
        true, "Happy birthday!", "WELCOME10", false, null);

new PurchaseOrder("ORD-9004", "CUST-103", items, home,
        false, null, null, true, "Ship same-day if received before 2pm.");
```

Ask: *"Which one is the priority order, and which is the gift?"* Let them
count. Then ask: *"What happens if I swap those two `boolean`s by
accident?"* The compiler says nothing. That silence is the whole problem.

**Do not rush this block.** The rest of the session is only interesting to
people who felt this problem.

## 0:08–0:20 — The Fix, Live

Rewrite the same two orders using the builder:

```java
PurchaseOrder.builder("ORD-9001", "CUST-100")
        .addItem(mug).addItem(book)
        .shippingAddress(home)
        .giftMessage("Happy birthday!")
        .couponCode("WELCOME10")
        .build();

PurchaseOrder.builder("ORD-9004", "CUST-103")
        .addItem(mug).addItem(book)
        .shippingAddress(home)
        .priority()
        .notes("Ship same-day if received before 2pm.")
        .build();
```

Ask: *"Now which one is the priority order?"* Instant answer. Nobody
counted anything.

Then open `PurchaseOrder.Builder` and point at `return this;` in two or
three methods. Ask: *"Why does that make the chain work?"* Let someone
explain it back to you — each call's result is the same builder, ready for
the next call.

## 0:20–0:30 — The Rule That Lives in One Place

Open `giftMessage(String message)`:

```java
public Builder giftMessage(String message) {
    this.giftMessage = message;
    this.giftWrapped = true;
    return this;
}
```

Ask: *"Why does setting a message also set gift wrap?"* Work towards: a
gift message on a box that is not wrapped makes no sense in this domain,
and the builder is the one place that rule needs to be written.

Then show `build()`:

```java
public PurchaseOrder build() {
    if (items.isEmpty()) { throw new IllegalStateException(...); }
    if (shippingAddress == null) { throw new IllegalStateException(...); }
    return new PurchaseOrder(this);
}
```

Ask: *"Why can't `addItem` check this instead?"* The answer to draw out:
`addItem` cannot know whether the caller is finished. Only `build()` marks
the moment the caller has declared themselves done, so it is the only place
that can honestly ask "is this complete?"

Run the demo and point at the reused-builder proof:

```
first items: 1, second items: 2
```

Ask: *"Why doesn't `first` also have 2 items?"* Answer: `List.copyOf` in
the constructor takes a snapshot. The product stops watching the builder
the moment `build()` returns.

## 0:30–0:38 — The Director, the Java Way

Open `PurchaseOrderPresets.expressOrder(...)`. Tell them plainly: the Gang
of Four book has a fourth role here, a **Director**, usually drawn as its
own interface and class. Point at this method and say: *"This is that
role. Java just doesn't bother with the class."*

Ask them to find something specific: *"Does this method touch a
`PurchaseOrder` field anywhere?"* It does not — only `Builder`'s public
methods. Ask why that matters: it means `PurchaseOrder` can change its
private fields tomorrow and not one preset needs to change.

## 0:38–0:50 — Exercises

### Exercise 1 — Add an option (about 7 minutes)

> Add a `deliveryWindow` (e.g. `"9am-12pm"`) to `PurchaseOrder`, with a
> matching `Builder.deliveryWindow(String)`.

Steps:

1. Add the field to `PurchaseOrder` and its constructor.
2. Add the field and chainable method to `Builder`.
3. Add an accessor, `Optional<String> deliveryWindow()`.
4. Run the tests — everything still passes.

The thing to draw out: **every existing call site kept compiling**,
including the ones that do not use the new option at all. That is the
opposite of what happened to the telescoping constructor.

### Exercise 2 — Break the invariant on purpose (about 5 minutes)

> Delete `this.giftWrapped = true;` from `giftMessage(...)`. Then write a
> test that asserts a gift message implies gift wrap.

Watch it fail. Ask: *"Where did that rule actually live?"* One line, now
missing. Put it back and watch the test pass. This is the clearest way to
show that a builder is not just a bag of setters — it is a place rules can
live.

## 0:50–0:58 — When *Not* to Use It

End on the boundaries, or they will over-apply it next week.

**Do not bother when there is nothing to decide.** `LineItem` and
`Address` in this project are plain records with public constructors —
two or three required fields, no options, no rules between them. Point at
them and ask: *"What would a builder buy us here?"* The honest answer is
nothing.

**A builder is a second object.** For every `PurchaseOrder` built, a
`Builder` briefly exists too. For an order placed a few times a second,
irrelevant. For something built millions of times in a hot loop, it is a
real allocation to weigh against the readability gained.

**It solves a different problem than a static factory method.** A static
factory method is about *naming and hiding* a constructor for one call. A
builder is about *spreading* a constructor's many optional arguments across
several calls. A type can have both — `PurchaseOrder.builder(...)` is a
static factory method that happens to return a builder.

## 0:58–1:00 — Wrap Up

Back to the one sentence:

> A constructor makes you decide the whole object in one call. A builder
> lets you decide it a piece at a time, and checks it is complete only when
> you say you are done.

Then send them somewhere:

- [`../README.md`](../README.md) to run it themselves
- [`animation.html`](animation.html) to step through it again slowly
- [`../video/`](../video/) if they want it narrated
- Back to
  [`../../static-factory-pattern`](../../static-factory-pattern) if they
  have not done it yet — the two compose, and this project's own
  `builder()` method is proof

## Facilitator Notes

- **The swapped-booleans moment in block one is the hook.** Let someone
  actually get it wrong before you explain why. If you just tell them,
  half the room will not feel it.
- **Expect "isn't this just a bunch of setters?"** Worth taking seriously.
  The answer is `giftMessage`: a setter only ever sets the field it is
  named after. A builder method is free to enforce a rule across several
  fields at once, and often should.
- **Expect "why not use a static factory method with named parameters
  instead?"** Java has no named parameters. A static factory method with
  nine positional parameters has exactly the same readability problem as a
  constructor with nine positional parameters — the fix there was never the
  keyword `new`, it was spreading the call across several named steps,
  which is what a builder does.
- **If you are running short**, cut the Director block (0:30–0:38). It is
  useful context but the session survives without it.
- **If you have longer than an hour**, have them build a `Builder` for a
  type of their own choosing from an earlier project in this repository,
  and see which one they pick — it usually reveals whether the idea has
  landed.
