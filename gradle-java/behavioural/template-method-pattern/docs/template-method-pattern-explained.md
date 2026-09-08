# The Template Method Pattern, Explained

> **Define the skeleton of an algorithm in an operation, deferring some steps
> to subclasses. Template Method lets subclasses redefine certain steps of an
> algorithm without changing the algorithm's structure.**
> — *Design Patterns*, Gamma, Helm, Johnson & Vlissides

In plain language: **write the sequence down once, in a method nobody can
override, and leave holes.**

## The Thing Three Copies Cannot Do

Three fulfilment routes, each written out from beginning to end, have exactly
one thing wrong with them, and it is not duplication.

It is that **the order of the steps is not written down anywhere**. It exists
as a shape repeated in three method bodies, and a shape that is repeated by
hand is a shape that drifts. Nothing in the compiler, the type system or the
test suite knows those six calls have to happen in that order — so when
somebody moves two lines in one copy, everything still builds and one
customer gets an email with no licence key in it.

You cannot fix that by extracting helpers, because what is duplicated is the
*call order*, not the call bodies. A helper method cannot own an order it is
not the caller of.

The pattern's answer is to make the order into a thing: one method, in one
place, that is the sequence — and to close it.

```java
public final FulfilmentReport fulfil(Order order) {
    FulfilmentReport report = new FulfilmentReport(order.id(), routeName());
    validate(order, report);
    reserveStock(order, report);
    charge(order, report);
    pack(order, report);
    dispatch(order, report);
    notifyCustomer(order, report);
    afterFulfilment(order, report);
    return report;
}
```

That `final` is not decoration. It is the guarantee, and everything the
pattern buys follows from it.

## Everyday Analogy: The Recipe

A recipe for a cake says: cream the fat and sugar, beat in the eggs, fold in
the flour, bake, cool, ice.

The order is not up for discussion. Ice it before you bake it and you have
neither cake nor icing. But *which* fat, *which* flavouring, whether you ice
it at all — those are yours. A vegan version changes what "the eggs" means. A
loaf version skips the icing entirely.

The recipe is the base class. The steps you fill in are the abstract methods.
"Ice it, unless you'd rather not" is a hook. And the thing the recipe will
never let you do is bake first.

## Participants

| Role | In the GoF book | Here | Job |
| --- | --- | --- | --- |
| Abstract class | `AbstractClass` | `FulfilmentProcess` | Owns `fulfil`, which is `final`; declares the steps |
| Template method | `TemplateMethod()` | `fulfil(Order)` | The sequence itself |
| Primitive operations | `PrimitiveOperation()` | `reserveStock`, `charge`, `dispatch`, `routeName` | Abstract — every route must answer |
| Steps with defaults | — | `pack`, `notifyCustomer` | Concrete; a route overrides only if it differs |
| Hooks | `Hook()` | `requiresShippingAddress`, `afterFulfilment` | Exist purely so a route can opt in or out |
| Concrete classes | `ConcreteClass` | `WarehouseFulfilment`, `MarketplaceFulfilment`, `DigitalFulfilment` | Fill in the holes |
| Naive alternative | — | `NaiveFulfilment` | Three copies, kept for contrast |

## Three Kinds of Hole, and How to Choose

This is the part of Template Method that is actually hard. The sequence is
easy; deciding what each step should *be* is the design.

### Abstract — "you must answer, I have no default"

```java
protected abstract void reserveStock(Order order, FulfilmentReport report);
```

Use this when there is no behaviour that would be right for a route that
forgot to think about it. Holding stock in a warehouse and asking a
marketplace seller to confirm have nothing in common but their position in
the sequence, so a default would only ever be wrong.

The cost is real: every new route must implement it, including routes for
which the step is trivial. `DigitalFulfilment.reserveStock` exists purely to
record that there was nothing to reserve — and that is the right outcome,
because "this route has nothing to reserve" is a decision somebody should
have to make explicitly.

### Concrete with a default — "most of you want this"

```java
protected void pack(Order order, FulfilmentReport report) {
    report.step("pack", order.itemCount() + " item(s) boxed and labelled");
}
```

Use this when there is a behaviour the majority of routes want. It makes the
common route short: `WarehouseFulfilment` says nothing at all about packing
or emailing, because the base class already does what it wants.

The trap is choosing a default that is *usually* right rather than *safely*
right. A default that silently does the wrong thing for a route nobody
re-read is worse than an abstract method that forced the question.

### Hook — "here is a place to stand"

```java
protected boolean requiresShippingAddress() { return true; }

protected void afterFulfilment(Order order, FulfilmentReport report) {
    // deliberately empty
}
```

Two flavours. `requiresShippingAddress` is a **question** the base class asks
before doing something; a route answers, and does not otherwise participate.
`afterFulfilment` is a **place**: an empty method the base class calls at a
point it controls, so a route with an extra obligation has somewhere to put
it.

The empty body is the point. It gets called for every route, including the
three that do nothing with it, because the one route that needs it —
`MarketplaceFulfilment`, posting its commission — must not have to negotiate
for a call site.

## Code Walkthrough

### The step that is private, and why

```java
private void validate(Order order, FulfilmentReport report) {
    if (order.lines().isEmpty()) throw new FulfilmentException(...);
    if (order.customerEmail() == null || order.customerEmail().isBlank()) throw ...;
    if (requiresShippingAddress() && !order.hasShippingAddress()) throw ...;
    ...
}
```

`validate` is the one step no route may replace. Making it `protected` would
have been the obvious choice and would have quietly handed every future
subclass permission to write `@Override protected void validate() { }` — which
is how orders ship into the void.

Instead it is `private`, and the only influence a route has over it is
answering one boolean. Look at what `DigitalFulfilment` got: permission to
skip the address check, and nothing else. Its orders still have to have lines
and an email address, and there is no override it could write to change that.

**That narrowness is the design.** Every hook you add is a permission you are
granting for the lifetime of the class. Grant the smallest one that solves the
problem.

### The route that overrides nothing optional

```java
public final class WarehouseFulfilment extends FulfilmentProcess {
    protected String routeName() { return "warehouse"; }
    protected void reserveStock(...) { ledger.reserve(...); }
    protected void charge(...) { ... }
    protected void dispatch(...) { ... }
}
```

Four methods. No `pack`, no `notifyCustomer`, no hooks. When the ordinary
route is this short, it is a sign the split between abstract, default and
hook was drawn in the right place — the base class's defaults were written
for the common case, and the common case is getting them for free.

### The route that justifies every hook

```java
public final class DigitalFulfilment extends FulfilmentProcess {
    protected boolean requiresShippingAddress() { return false; }
    protected void reserveStock(..) { report.step("reserve", "nothing to reserve, ..."); }
    protected void pack(..)         { report.step("pack", "nothing to pack"); }

    protected void dispatch(Order order, FulfilmentReport report) {
        String key = LicenceKeys.mint(order);
        report.dispatchedAs(key);
        report.step("dispatch", "licence key issued: " + key);
    }

    protected void notifyCustomer(Order order, FulfilmentReport report) {
        report.notified(order.customerEmail() + ": Order " + order.id()
                + " is ready to download. Key: " + report.dispatchReference());
        ...
    }
}
```

Two things to notice.

**The empty steps still record themselves.** `reserveStock` and `pack` have
nothing physical to do, and they do not vanish — they write "nothing to
reserve" and "nothing to pack" onto the report. The digital route produces
six steps like everything else. "This step had nothing to do" is a fact worth
printing, and it keeps the reports comparable.

**`notifyCustomer` reads what `dispatch` wrote**, and this is where the
`final` on `fulfil` cashes out. These two methods are on the same class,
written by the same author, and one depends on the other having run. In
`NaiveFulfilment` the identical two lines produce
`Key: (not dispatched)`, because nothing was guaranteeing the order. Here the
guarantee is structural: no subclass, present or future, can put `notify`
before `dispatch`.

### The route that uses the after-hook

```java
protected void afterFulfilment(Order order, FulfilmentReport report) {
    Money commission = order.subtotal().percent(COMMISSION_PERCENT);
    report.note("seller ledger: " + commission + " commission posted against ...");
}
```

`MarketplaceFulfilment` has an obligation the other routes do not: the
commission has to be posted somewhere. It is not one of the six steps, it is
not something the base class should know exists, and it has to happen after
everything else succeeded. The empty hook is exactly the right size of hole
for it.

Note that it records a **note**, not a step. Notes are kept apart from steps
on the report precisely so that a route using this hook cannot change the
sequence a test asserts on.

## Why the Tests Are the Proof

`FulfilmentProcessTest` never mentions warehouses, sellers or licence keys.
It defines `RecordingRoute` — a route whose steps do nothing but append their
own names to a list — and then reads that list back:

```java
assertEquals(
    List.of("reserveStock", "charge", "pack", "dispatch", "notifyCustomer",
            "afterFulfilment"),
    route.calls);
```

That is the pattern's central claim, checked directly: the base class called
the steps, in its order, on a subclass it has never heard of.

Two more that are worth reading:

- `aThrowingStepStopsTheRest` — when `charge` throws, `dispatch` and
  `notifyCustomer` are never reached. A later step must never run on the
  assumption that an earlier one succeeded.
- `hookOnlyAnswersOneQuestion` — a route that answers
  `requiresShippingAddress() == false` still cannot get an empty order
  through. The hook grants one permission, not general amnesty.

And `NaiveFulfilmentTest` holds the comparison. Each drift is pinned as a
*passing* test that asserts the wrong behaviour:

```java
assertEquals(List.of("validate", "reserve", "charge", "pack", "notify", "dispatch"),
        naive.fulfilDigital(digitalOrder()).stepNames());
```

The difference the pattern makes is a diff between two test files rather than
a claim in a README.

## What You Gain

1. **The sequence exists.** It is a method, not a convention, and it is in one
   place.
2. **It cannot be reordered**, by anyone, ever — that is what `final` means.
3. **Later steps can rely on earlier ones.** `notifyCustomer` can quote what
   `dispatch` produced without checking whether it ran.
4. **The common route is short.** Defaults mean `WarehouseFulfilment` is four
   methods.
5. **A fourth route is one new class.** `FulfilmentDemo` adds click-and-collect
   without opening `FulfilmentProcess`, and gets the same six steps in the
   same order for nothing.
6. **The sequence is observable**, because every step records itself. Four
   unrelated routes print identical step names, and no route chose that.

## What to Watch Out For

**Inheritance, and you only get one.** Every route is welded to
`FulfilmentProcess` and can extend nothing else. This is the pattern's real
price and the reason composition is usually the better modern default. Pay it
when the *order* is what you are protecting.

**The fragile base class.** Adding a seventh step to `fulfil` changes the
behaviour of every route at once, including ones in other repositories you
cannot see. The template method is public API, and its sequence is part of the
contract.

**Too many hooks.** Every hook is a permission granted forever. A base class
with a hook before and after every step is not protecting a sequence any more;
it is a very complicated way of writing a callback list. If you find yourself
adding a hook per subclass, the steps probably wanted to be strategies.

**Steps that call each other.** A subclass step calling another subclass step
directly re-creates the drift the pattern removed, because now there are two
places that know about ordering. Steps talk to the receiver and the report,
not to each other.

**Overriding a default without calling `super`, when you meant to add.**
`@Override` protects you from typos, not from intent. If your override should
extend the default rather than replace it, `super.pack(order, report)` has to
be there — and nothing will remind you.

## Template Method vs. Factory Method vs. Strategy vs. Command

| | Varies | Bound at | Owns the order? |
| --- | --- | --- | --- |
| **Template Method** | Several steps of one algorithm | Compile time, by subclassing | **Yes** — one `final` method |
| **Factory Method** | Which object to create — exactly one step | Compile time, by subclassing | Yes, but there is only one hole |
| **Strategy** | A whole algorithm | Run time, by composition | No |
| **Command** | What action to run, and when | Run time, by object | No — the invoker just runs what it is given |

The one worth being precise about is **Factory Method**, because this
repository teaches it too, and it is also described as "a workflow with a hole
in it". The line: Factory Method's hole is *which object to create*, there is
exactly one of them, and it returns a product. Template Method's holes are
*how several steps behave*, they return nothing in particular, and some of
them are optional. **Factory Method is Template Method narrowed to object
creation.**

The one worth being honest about is **Strategy**. For many problems it is
simply better: run-time swappable, no inheritance, testable in isolation. Use
Template Method when a fixed *order* is the invariant you need, and Strategy
when independently varying *behaviour* is.

## Where You Have Already Seen It

- `java.util.AbstractList` — implements `iterator()`, `indexOf()`,
  `equals()` and more in terms of the two methods you must supply, `get(int)`
  and `size()`.
- `java.io.InputStream.read(byte[], int, int)` — a loop written once, on top
  of the single abstract `read()`.
- `HttpServlet.service()` — dispatches to `doGet`, `doPost` and friends, all
  of which are hooks with a "405 Method Not Allowed" default.
- JUnit's `@BeforeEach` / `@AfterEach` — a fixed lifecycle around your test
  method, with hooks at points the framework controls.
- Spring's `JdbcTemplate`, `RestTemplate` and every other `*Template` class in
  the ecosystem. The name is not a coincidence.

## Try It Yourself

1. **Add a fifth route.** Subscription renewal: nothing to reserve, charge a
   stored card, nothing to pack, extend the licence period. How many methods
   did you have to write, and did you open `FulfilmentProcess`?
2. **Try to break the order.** Add `@Override public FulfilmentReport
   fulfil(Order order)` to any route and read the compiler error. That error
   is the pattern.
3. **Add a fraud check** as a seventh step between validate and reserve. Do it
   in `FulfilmentProcess`, then count how many routes you had to edit. Then do
   the same to `NaiveFulfilment`.
4. **Move the check the other way.** Make `validate` `protected` and override
   it in one route to skip the address check. Then ask yourself what stops the
   next person doing that to the email check.
5. **Rewrite it as Strategy.** Six functional interfaces, composed. Get it
   working, then work out what you would have to add to make it impossible to
   supply them in the wrong order.

## See Also

- [`problem-statement.md`](problem-statement.md) — the drift, in detail
- [`class-diagram.md`](class-diagram.md) — the structure
- [`uml-diagram.md`](uml-diagram.md) — one `fulfil` call, step by step
- [`animation.html`](animation.html) — the same call, animated
- [Factory Method](../../../creational/factory-method-pattern/README.md) — the
  narrowed version, for comparison
- [Strategy](../../strategy-pattern/README.md) — the composed alternative
