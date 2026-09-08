# The Builder Pattern, Explained

## First, an Honest Note

Unlike the static factory method next door, this one really is in the Gang
of Four book, in the creational chapter, right alongside Abstract Factory.
It is also *Effective Java*'s **Item 2: Consider a builder when faced with
many constructor parameters** — the two describe the same technique from
two different angles, twenty years apart, and they agree completely. That
double billing is why it belongs early in this collection: it is both the
formal pattern and the practical advice.

One thing to set aside before we start: the GoF book frames Builder around
a **Director** that drives a builder through a fixed sequence of steps, so
different builders can produce different representations from the same
director. Real Java code almost never writes that as a class. It writes it
as a static method — which is exactly what
[`PurchaseOrderPresets`](../src/main/java/com/jk/explore/builder/PurchaseOrderPresets.java)
in this project does. Same idea, no ceremony.

## The Definition

> Separate the construction of a complex object from its representation, so
> that the same construction process can create different representations.
>
> — *Design Patterns* (Gamma, Helm, Johnson, Vlissides)

In plainer words:

> **Instead of one constructor call carrying every fact at once, assemble
> the object across several small calls — one per piece — and finish with a
> `build()` that checks everything is in order.**

## The Telescoping Constructor, One More Time

`docs/problem-statement.md` showed the wall: a `PurchaseOrder` with two
required facts and five optional ones has thirty-two legitimate
combinations, and no fixed argument list reads well for all of them. The
builder's answer is to stop insisting the whole object arrive in one call.

## The Participants

| Role | In this project | What it does |
| --- | --- | --- |
| Product | `PurchaseOrder` | The complex, immutable object being assembled |
| Builder | `PurchaseOrder.Builder` | One chainable method per optional (and required) piece |
| Director *(GoF's term)* | `PurchaseOrderPresets` | Drives the builder through a fixed recipe — as static methods, not a class |
| Client | `PurchaseOrderDemo` | Uses either the builder directly or a preset |

## The Code, Walked Through

### `PurchaseOrder.builder(...)` — a static factory that returns a builder

```java
public static Builder builder(String orderId, String customerId) {
    return new Builder(orderId, customerId);
}
```

The two facts that every order needs — an id and a customer — are taken
here, as constructor-style required arguments, rather than as chained
methods. This is deliberate: **required fields belong in the step that
starts the builder, optional fields belong in the steps that follow.**
Mixing the two — making `orderId` just another chained call — would let a
caller build an order and forget it entirely, and nothing would catch that
until `build()`, if ever. This is also the point where the builder pattern
and the static factory method pattern meet: the door into a `Builder` is
itself a named static method, not a `new Builder(...)` call.

### `PurchaseOrder.Builder` — one method per piece, all returning `this`

```java
public Builder addItem(LineItem item) { items.add(item); return this; }
public Builder shippingAddress(Address address) { this.shippingAddress = address; return this; }
public Builder giftWrap() { this.giftWrapped = true; return this; }
public Builder giftMessage(String message) {
    this.giftMessage = message;
    this.giftWrapped = true;   // a message implies wrapping
    return this;
}
public Builder couponCode(String code) { this.couponCode = code; return this; }
public Builder priority() { this.priority = true; return this; }
public Builder notes(String notes) { this.notes = notes; return this; }
```

Every method returns `this`, which is what makes the calls chain:

```java
PurchaseOrder order = PurchaseOrder.builder("ORD-9001", "CUST-100")
        .addItem(mug)
        .addItem(book)
        .shippingAddress(home)
        .giftMessage("Happy birthday!")
        .couponCode("WELCOME10")
        .build();
```

Read that call site against the telescoping version from the problem
statement. Nobody counts commas. Every line names the thing it is setting.
An order with none of the options reads as five lines instead of nine, with
no trailing `null, null, false, null` to explain.

Look at `giftMessage` closely: it sets **two** fields, because a gift
message without gift wrap makes no sense in this domain, and that rule now
lives in exactly one place. A telescoping constructor would have had to
trust every caller to pass `true` alongside the message, or bury a
correcting `if` in its body that silently overrides what it was handed.
Here, the builder's own method enforces the rule as the value goes in.

### `build()` — where the required fields are finally checked

```java
public PurchaseOrder build() {
    if (items.isEmpty()) {
        throw new IllegalStateException("a purchase order needs at least one item");
    }
    if (shippingAddress == null) {
        throw new IllegalStateException("a purchase order needs a shipping address");
    }
    return new PurchaseOrder(this);
}
```

A builder is filled in gradually, in whatever order the caller finds
natural — items first, address first, it does not matter. That means the
two remaining required facts, at least one item and a shipping address,
cannot be checked as they arrive; they can only be checked once the caller
declares they are finished, which is what calling `build()` means. Nothing
is checked too early, and nothing is checked too late — there is never a
half-valid `PurchaseOrder` in memory, only a `Builder` that has not
finished yet.

### `PurchaseOrder` — immutable once built

```java
private PurchaseOrder(Builder builder) {
    this.items = List.copyOf(builder.items);
    ...
}
```

The constructor is private — a `Builder` is the only way in — and
`List.copyOf` takes a snapshot rather than holding the builder's own list.
Reuse the builder to assemble a second order, and the first one does not
change underneath you:

```java
PurchaseOrder.Builder reused = PurchaseOrder.builder("ORD-9005", "CUST-104")
        .addItem(mug).shippingAddress(home);
PurchaseOrder first = reused.build();
reused.addItem(book).priority();
PurchaseOrder second = reused.build();
// first.items().size() == 1, second.items().size() == 2
```

Without the copy, `first` and `second` would share one mutable list, and
`first` would silently grow a second item it was never asked for. This is
the detail that separates a real builder from a bag of setters: **the
product does not keep watching the builder after `build()` returns.**

### `PurchaseOrderPresets` — the Director, written the Java way

```java
public static PurchaseOrder expressOrder(String orderId, String customerId,
                                         List<LineItem> items, Address address) {
    PurchaseOrder.Builder builder = PurchaseOrder.builder(orderId, customerId)
            .shippingAddress(address)
            .priority()
            .notes("Ship same-day if received before 2pm.");
    items.forEach(builder::addItem);
    return builder.build();
}
```

This is the GoF Director's job — drive a builder through a fixed sequence
so callers do not need to know the recipe — done as one static method
instead of a class implementing a `Director` interface. Notice what it does
*not* touch: no `PurchaseOrder` field, no `List.copyOf`, nothing from
`PurchaseOrder`'s private insides. It only calls public methods on
`Builder`. That is what makes it safe for `PurchaseOrder` to change its
internal representation later without anyone needing to touch a preset.

## What You Gain

**Readable call sites.** Every value at the call site is named by the
method that receives it. There is nothing left to decode by position.

**Options that default themselves.** An order with none of the five extras
chained on simply has all five off. No caller writes `false, null, null,
false, null` to say so.

**A single place to enforce cross-field rules.** `giftMessage` implying
`giftWrapped` lives once, in the builder, rather than being a rule every
caller must remember or a correction the constructor makes silently.

**Validation at the natural moment.** `build()` runs after every piece has
arrived, which is the only point at which "is this order complete" can
honestly be answered.

**Immutability without a constructor nobody can call.** `PurchaseOrder`'s
fields are all `final`. A builder is the on-ramp; once you are off it, nothing
can be changed, including by the builder that built you.

## What to Watch Out For

**A second object exists during construction.** For a moment, there are two
things in memory — the builder and, once `build()` runs, the product. For a
`PurchaseOrder` this costs nothing worth mentioning; for something built a
million times a second in a hot loop, it is a real allocation to weigh.

**It is more typing for a simple type.** `LineItem` and `Address` in this
project are plain records with public constructors, on purpose. They have
two or three fields, all required, and nothing to decide — a builder there
would be ten lines of ceremony around a one-line problem. Reach for a
builder when the *option count* is the problem, not whenever a class has
more than one field.

**Required fields still need a place to live.** This project puts
`orderId` and `customerId` on the entry to `builder(...)` rather than as
chained methods, precisely so the compiler — not a runtime check — refuses
to let you forget them. Some builders instead check every required field
in `build()`, the way `items` and `shippingAddress` are checked here; both
are legitimate, and the choice is about how early you want the mistake
caught.

## How This Relates to the Other Creational Patterns

| | Builder | Static Factory Method | Simple Factory | Abstract Factory |
| --- | --- | --- | --- | --- |
| In the GoF book? | Yes | No | No | Yes |
| The problem it solves | Many optional pieces, one object | Naming and hiding a constructor | Which one? | Which whole matching set? |
| What the caller writes | A chain of calls, one per piece | One named call | One call to a factory class | One call, gets a family back |
| Extra classes needed | One builder | None | One | One per family |

The honest summary: these solve *different* problems and are not
alternatives to each other. A type can easily have both a static factory
method and a builder — `PurchaseOrder.builder(...)` in this project is
exactly that, a named static entry point that hands back a builder instead
of a finished object.

## Try It Yourself

1. **Add an option.** Give `PurchaseOrder` a `deliveryWindow` (a `String`
   such as `"9am-12pm"`), with a matching `Builder.deliveryWindow(String)`.
   Note that every existing call site — the hand-built order, all three
   presets, every test — keeps compiling unchanged.
2. **Add a preset.** Write `PurchaseOrderPresets.subscriptionRenewal(...)`
   that always sets a fixed coupon code and a fixed note. Check that it
   never mentions a `PurchaseOrder` field directly.
3. **Break the invariant on purpose.** Delete the `this.giftWrapped = true`
   line from `giftMessage(...)`, then write a test asserting that a gift
   message with no gift wrap is nonsense. Watch it fail, and see exactly
   which line of the builder was carrying that rule.
4. **Feel the alternative.** Make every `PurchaseOrder` field settable
   through a public constructor instead, in the order they are declared.
   Then add a sixth optional field and count how many existing call sites
   you must edit to keep compiling.
