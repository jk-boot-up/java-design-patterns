# The Static Factory Method, Explained

## First, an Honest Note

This one is not in the Gang of Four book. There is no "Static Factory
Pattern" chapter to look up, and if you say the name in an interview you may
get a raised eyebrow.

Its actual home is Joshua Bloch's *Effective Java*, **Item 1: Consider static
factory methods instead of constructors**. It is a technique rather than a
pattern — but it is the single most widely used creational technique in Java,
it appears on nearly every page of the standard library, and it is the right
first thing to reach for. That is why it belongs in this collection.

Note also that "static factory method" has nothing to do with the Gang of
Four's **Factory Method** pattern, despite the names. They solve different
problems and the resemblance is purely verbal. There is a table below that
lays the two side by side, because the confusion is genuinely common.

## The Definition

> A static factory method is a static method that returns an instance of the
> class it lives in.
>
> — *Effective Java*, Item 1

In plainer words:

> **Instead of `new Thing(...)`, callers write `Thing.somethingDescriptive(...)`,
> and the class decides what to actually hand back.**

That is the entire mechanism. The power is not in the method being static —
it is in the fact that a method, unlike a constructor, has a **name** and is
under **no obligation to return a new object**.

## The Vending Machine

Think about a constructor as a workbench. You want a coffee, so you are
handed beans, water, a filter and a cup, and you assemble it yourself. You
need to know how coffee is made. If the recipe changes, you have to relearn
it.

A static factory method is the vending machine. You press the button marked
**Latte**. Behind the panel it might pour a fresh one, it might hand you one
it already made, it might quietly give you the decaf because the machine is
out of ordinary beans. You do not know and you do not care. You asked for
what you *wanted*, not for instructions on how to build it.

Two things follow from that, and they are the two things the pattern is for:

- The buttons have **labels**. That is why you can tell Latte from Espresso.
- The machine keeps its **internals private**. That is why the recipe can
  change without anyone relearning anything.

## The Participants

| Role | In this project | What it does |
| --- | --- | --- |
| The type | `Discount`, `Money` | The public face. Holds the factory methods. |
| Static factory methods | `Discount.percentage(int)`, `Money.pounds(double)` | Named entry points. The only way in. |
| Hidden implementations | `PercentageDiscount`, `NoDiscount`, … | Package-private. Callers cannot name them. |
| The client | `CheckoutService` | Uses the type. Never mentions an implementation. |

There is no separate factory class in that table. That is not an omission —
it is the point.

## The Code, Walked Through

### `Discount` — the type is its own factory

```java
public interface Discount {

    Money appliedTo(Order order);
    String describe();

    static Discount none() {
        return NoDiscount.INSTANCE;
    }

    static Discount percentage(int percent) {
        if (percent < 0 || percent > 100) {
            throw new IllegalArgumentException("percentage must be 0-100, was " + percent);
        }
        return percent == 0 ? none() : new PercentageDiscount(percent);
    }

    static Discount amountOff(Money amount) {
        return amount.isZero() ? none() : new AmountOffDiscount(amount);
    }

    static Discount freeShipping() {
        return FreeShippingDiscount.INSTANCE;
    }
}
```

Read `percentage` slowly, because there are three separate ideas packed into
five lines.

The **name** is doing work no constructor could. `percentage(10)` and
`amountOff(Money.pounds(10))` sit next to each other, both take one value,
and nobody has to guess. As constructors they could not have coexisted at
all.

The **validation** happens before any object exists. A `Discount` of 150% is
not a thing that gets created and then rejected — it never gets created.

The **return** is a decision. Ask for 0% and you do not get a
`PercentageDiscount` that multiplies by zero; you get the shared do-nothing
instance. The caller said what it wanted, so we were free to serve it however
we liked.

> Since Java 8, interfaces can hold `static` methods. Before that this
> technique needed an abstract class or a companion `Discounts` class. If you
> read older code and find a `Collections`-style helper class beside an
> interface, that is why.

### `NoDiscount` — the object that only needs to exist once

```java
final class NoDiscount implements Discount {

    static final NoDiscount INSTANCE = new NoDiscount();

    private NoDiscount() {
    }

    @Override
    public Money appliedTo(Order order) {
        return Money.zero();
    }
}
```

No `public`. Outside this package the class does not exist as far as the
compiler is concerned — you cannot import it, name it, or extend it.

It has no fields, so every instance would be identical, so there is no reason
to have more than one. `new` could never have expressed that. `Discount.none()`
expresses it exactly, and callers get the saving without knowing about it.

### `Money` — the same trick on a value type

```java
public final class Money {

    private static final Money ZERO = new Money(0);

    private final long pence;

    private Money(long pence) {
        this.pence = pence;
    }

    public static Money zero() {
        return ZERO;
    }

    public static Money pence(long pence) {
        return pence == 0 ? ZERO : new Money(pence);
    }

    public static Money pounds(double pounds) {
        return pence(Math.round(pounds * 100));
    }
}
```

`Money.pounds(5)` is £5.00. `Money.pence(5)` is £0.05. Same argument type,
eighty-fold difference, and the names make it impossible to get wrong. This
is the single most valuable thing static factories do in real codebases, and
it costs nothing.

Note that `pounds` delegates to `pence`, which routes zero to the shared
constant. Every path in, however it arrived, benefits from the caching. With
a public constructor there is no such thing as "every path in".

### `CheckoutService` — the client that never chooses

```java
public Receipt checkout(Order order, Discount discount) {
    Money off = discount.appliedTo(order);
    Money total = order.subtotal().plus(order.shipping()).minus(off);
    ...
}
```

Search this class for `PercentageDiscount`, or for `new`, or for an `if` on
the kind of discount. There is nothing. Whether the customer gets 10% off, £5
off, free shipping, the better of two offers, or nothing at all, these lines
run unchanged — because all the choosing already happened, inside a factory
method, before this code was ever reached.

### `Discount.forCoupon` — where it all pays off

```java
static Discount forCoupon(String code) {
    return switch (code.trim().toUpperCase()) {
        case "SAVE10"   -> percentage(10);
        case "SAVE25"   -> percentage(25);
        case "FIVEROFF" -> amountOff(Money.pounds(5));
        case "FREESHIP" -> freeShipping();
        case "BESTDEAL" -> bestOf(percentage(10), amountOff(Money.pounds(5)));
        case ""         -> none();
        default -> throw new IllegalArgumentException("unknown coupon code: " + code);
    };
}
```

Five coupon codes, five different classes coming back, one return type. The
storefront calls `Discount.forCoupon(code)` and gets a `Discount`. It cannot
tell them apart and has no reason to want to.

`bestOf` is the sharpest example. It returns a `BestOfDiscount` that holds
two other discounts and picks the better one *per order* — so the same object
can behave differently for different customers. A caller could not have
written that without knowing all three classes. Through the factory method it
knows none of them.

## What You Gain

**Names.** The biggest win and the least glamorous. `Money.pounds(5)` versus
`new Money(5)`. Multiply that across a codebase and it is the difference
between code you can read and code you have to decode.

**Freedom not to allocate.** `Discount.none()` and `Money.zero()` return the
same instance every time. `Boolean.valueOf(true)` in the JDK does exactly
this, and so does `Integer.valueOf` for small numbers. Constructors are
forbidden from this optimisation by definition.

**Freedom to choose the class.** `percentage(0)` returns `NoDiscount`. Nobody
notices, nobody can notice, and if you later add a `SmallPercentageDiscount`
optimised for the common case, still nobody notices.

**Freedom to hide the classes entirely.** Five implementations, none public.
They can be renamed, merged, split or deleted without touching a caller,
because no caller ever knew their names. This is the deepest benefit and the
easiest to overlook.

**A place to validate.** `percentage(150)` throws before an object exists.
There is never a half-valid `Discount` in memory.

**Freedom to return something that does not exist yet.** `forCoupon` could
one day return a class loaded from a plugin jar. The method signature would
not change. This is how `ServiceLoader` and most of the JDBC API work.

## What to Watch Out For

Three real costs. They are smaller than the benefits, which is why this
technique is everywhere, but they are not zero.

**Classes with no public constructor cannot be subclassed.** If `Money`'s
constructor is private, nobody outside can extend `Money`. Usually this is a
feature — value types should be final anyway — but if you were relying on
inheritance, it is gone. The standard advice is that this pushes you towards
composition, which is generally the better design regardless.

**They are harder to find.** Constructors have a dedicated section in Javadoc
and your IDE offers them when you type `new`. A static factory method is just
another method in the list. This is exactly why the naming conventions below
matter so much — `of`, `from` and `valueOf` are how the ecosystem compensates.

**They are not a pattern, so they do not scale to structure.** A static
factory method is a better front door. It is not a way to swap whole
implementations at runtime, and it does not let a subclass or a configuration
decide what gets built. When you need *that*, you have outgrown this
technique and want Factory Method or Abstract Factory.

## The Naming Conventions

Java has settled on a shared vocabulary. Follow it and your API will feel
familiar to people who have never seen it.

| Name | Means | JDK example |
| --- | --- | --- |
| `of` | An instance holding these values | `List.of(a, b)`, `Set.of(x)` |
| `from` | A type conversion, one argument in | `Instant.from(temporal)` |
| `valueOf` | A more verbose `from`; often cached | `Integer.valueOf("42")` |
| `getInstance` | The instance, possibly a shared one | `Calendar.getInstance()` |
| `newInstance` | Guaranteed a fresh one each call | `Array.newInstance(type, len)` |
| `parse` | Built from a string representation | `LocalDate.parse("2026-08-19")` |
| `copyOf` | An independent copy of the argument | `List.copyOf(other)` |

This project uses `pounds`, `pence`, `percentage`, `amountOff`, `zero`,
`none`, `freeShipping`, `bestOf` and `forCoupon` — domain words rather than
the generic ones, which is right when the domain has a better word available.
`Money.parse` uses the conventional name because it does the conventional
thing.

## Where You Have Already Used This

You have been calling static factory methods since your first Java lesson,
probably without a name for it:

| Call | What is really happening |
| --- | --- |
| `List.of("a", "b")` | Returns one of several hidden classes, chosen by size |
| `Integer.valueOf(5)` | Returns a cached instance; `valueOf(1000)` does not |
| `Optional.of(x)` / `Optional.empty()` | `empty()` returns a shared singleton |
| `LocalDate.now()` | No sensible constructor arguments exist at all |
| `String.valueOf(anything)` | Overloads that a constructor could not express |
| `Stream.of(...)` / `Collectors.toList()` | Implementation classes you have never seen |

`List.of(...)` is worth dwelling on. Depending on how many arguments you pass
it, you get back a different class — there are specialised ones for zero, one
and two elements. You have never noticed, never needed to, and the JDK team
can change the whole arrangement in the next release without breaking your
code. That is the pattern, working exactly as intended.

## How This Relates to the Other Factories

| | Static Factory Method | Simple Factory | Factory Method | Abstract Factory |
| --- | --- | --- | --- | --- |
| In the GoF book? | No | No | Yes | Yes |
| Where creation lives | On the product's own type | A separate factory class | A method subclasses override | An interface with several creators |
| Who decides | The method, from its arguments | The factory, from a parameter | The subclass, at compile time | The chosen factory family |
| Extra classes needed | None | One | One per variant | One per family |
| The question it answers | "Give me one that…" | "Which one?" | "Which one — decided by my subclass?" | "Which matching set?" |
| Reach for it when | Almost always, as a first step | A parameter picks the type | A workflow has a hole in it | Products must match each other |

The honest summary: **start here**. Most creation problems are solved by
giving the type a well-named static factory method and stopping. The GoF
patterns are what you graduate to when the decision has to move somewhere
else — into a subclass, or into a family — and not before.

## Try It Yourself

1. **Add a coupon.** Add `"HALFPRICE"` to `forCoupon`, returning
   `percentage(50)`. Note that you wrote one line and no new class.
2. **Add a new kind of discount.** Write a package-private
   `TieredDiscount` — 5% under £50, 15% over — and expose it as
   `Discount.tiered()`. Now check `CheckoutService`: it did not change, and
   it cannot name your new class.
3. **Try to break in.** From a test in a *different* package, write
   `new PercentageDiscount(10)`. Watch it fail to compile. That is the
   boundary being enforced for you.
4. **Prove the caching.** Add an assertion that
   `Money.pounds(0) == Money.pence(0)` — reference equality, not `equals`.
   Then try to write the equivalent with a public constructor.
5. **Feel the alternative.** Make `PercentageDiscount` public with a public
   constructor and use it directly in `CheckoutService`. Then try to change
   its constructor's signature, and count the places you have to edit.
