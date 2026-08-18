# The Simple Factory Pattern — Explained

## One-Line Definition

> **Simple Factory** puts the decision of *which* class to instantiate into
> one method, so callers can ask for an object by name instead of building
> it themselves.

A note on naming, because it confuses everybody at first: Simple Factory is
**not** one of the twenty-three Gang of Four patterns. It is an idiom — the
one everyone actually writes — and it is the natural first step towards the
two real creational patterns, Factory Method and Abstract Factory. Learn it
first; the others make far more sense afterwards.

## The Everyday Analogy

Think of a **coffee shop counter**.

You do not walk behind the counter, find the espresso machine, grind the
beans and steam the milk. You say *"a cappuccino, please"* and a cappuccino
arrives. You named what you wanted; somebody else knew how to make it.

Tomorrow the shop buys a better machine, or starts making the cappuccino a
different way. Your order does not change. You never knew how it was made,
so there is nothing for you to relearn.

**The counter is the factory.** In this project,
`PaymentMethodFactory.create(...)` is the counter, `PaymentType.UPI` is what
you say, and `UpiPayment` is the drink.

## The Participants

| Role | In this project | Job |
| --- | --- | --- |
| **Product** | `PaymentMethod` | The interface every result shares — what the client programs against |
| **Concrete products** | `CreditCardPayment`, `UpiPayment`, `PayPalPayment`, `NetBankingPayment` | Do the real specialised work |
| **Factory** | `PaymentMethodFactory` | Holds the one `switch`; the only class that calls `new` on a product |
| **Client** | `CheckoutService` | Names a type, uses the result through the interface |

A crucial detail: **the client never mentions a concrete product type.** It
mentions `PaymentType` (data) and `PaymentMethod` (an interface). Grep the
client for `CreditCardPayment` and you find nothing. That is the whole test
of whether you have applied the pattern correctly.

## How This Project Implements It

### The product interface

```java
public sealed interface PaymentMethod
        permits CreditCardPayment, UpiPayment, PayPalPayment, NetBankingPayment {

    String displayName();

    PaymentReceipt pay(PaymentRequest request);
}
```

`sealed` is a Java 17+ feature that names the complete set of
implementations. It buys something concrete here, explained in a moment.

### The concrete products stay simple and independent

```java
public final class UpiPayment implements PaymentMethod {

    @Override
    public String displayName() {
        return "UPI";
    }

    @Override
    public PaymentReceipt pay(PaymentRequest request) {
        System.out.println("UPI: sending a collect request to " + request.customerId());
        System.out.println("UPI: customer approved " + request.amount() + " in the payments app");
        return new PaymentReceipt(newTransactionId(), displayName(), request.amount());
    }
}
```

The other three follow the same shape. None of them knows a factory exists.
You could use any of them on its own tomorrow.

### The factory makes the choice — in one place

```java
public class PaymentMethodFactory {

    public static PaymentMethod create(PaymentType type) {
        if (type == null) {
            throw new IllegalArgumentException("Payment type must not be null");
        }
        return switch (type) {
            case CREDIT_CARD -> new CreditCardPayment();
            case UPI -> new UpiPayment();
            case PAYPAL -> new PayPalPayment();
            case NET_BANKING -> new NetBankingPayment();
        };
    }
}
```

That `switch` has no `default` branch, and that is deliberate. Because the
switch covers every constant of an enum, the compiler knows it is
exhaustive. Add a fifth `PaymentType` and this file **stops compiling**
until you handle it. A missing case becomes a build error rather than a
runtime surprise — which is exactly what you want, given that the factory's
whole job is knowing the full list.

There is also a `String` overload, because real input usually arrives as
text from a form or a JSON body:

```java
public static PaymentMethod create(String type) {
    if (type == null || type.isBlank()) {
        throw new IllegalArgumentException("Payment type must not be blank");
    }
    try {
        return create(PaymentType.valueOf(type.trim().toUpperCase().replace('-', '_')));
    } catch (IllegalArgumentException e) {
        throw new IllegalArgumentException("Unsupported payment type: " + type, e);
    }
}
```

Sloppy input handling now lives in one place too. Every caller gets the same
tolerance for case and dashes, and the same clear error message.

### The client stays blissfully ignorant

```java
public PaymentReceipt checkout(PaymentRequest request, PaymentType type) {
    PaymentMethod method = PaymentMethodFactory.create(type);

    System.out.println("Checkout: paying for " + request.orderId() + " with " + method.displayName());
    PaymentReceipt receipt = method.pay(request);
    System.out.println("Checkout: done, transaction " + receipt.transactionId());

    return receipt;
}
```

One line to obtain the object, then ordinary polymorphism. Change the type
and every line after the first is unchanged.

### Java 21 records as the data carriers

`PaymentRequest` and `PaymentReceipt` are `record` types — immutable data
holders with automatic constructors, accessors, `equals`, `hashCode` and
`toString`:

```java
public record PaymentReceipt(String transactionId, String method, double amount) { }
```

They keep the product interface clean: one object in, one object out.

## What You Gain

- **One place to change.** New payment method? One file to edit, and the
  compiler tells you where.
- **Loose coupling.** Clients depend on an interface and an enum, never on a
  concrete class.
- **Hidden construction.** The day a product needs configuration in its
  constructor, only the factory learns about it.
- **Testability.** The selection logic is a static method you can test
  directly — see `PaymentMethodFactoryTest`.
- **Consistent validation.** Bad input fails the same way everywhere.

## What to Watch Out For

- **It violates the Open/Closed Principle, and that is the point.** Adding a
  product means *modifying* the factory. Say this out loud when you teach
  it. Simple Factory does not remove that cost — it centralises it. When
  centralising is no longer good enough, you reach for Factory Method.
- **Do not let the factory grow logic.** Its job is to choose and construct.
  The moment it starts validating amounts or calling a payment gateway, it
  has become something else.
- **A giant switch is a smell, eventually.** Four cases is fine. Forty cases
  that change weekly means you want a registry (`Map<PaymentType,
  Supplier<PaymentMethod>>`) or `ServiceLoader` instead.
- **Static methods are hard to substitute.** `PaymentMethodFactory.create`
  is static, which is convenient and untestable-in-isolation at the same
  time. If clients need to swap the factory in tests, make it an instance
  and inject it.
- **Do not hide something that is not complex.** If there is only one
  implementation, `new` is clearer than a factory.

## Simple Factory vs. the Real Factory Patterns

| Pattern | Who decides the class | Mechanism | Adding a product |
| --- | --- | --- | --- |
| **Simple Factory** | One static method | `switch` on data | Edit the factory |
| **Factory Method** | A subclass | Subclasses override a creation method | Add a subclass |
| **Abstract Factory** | An injected factory object | One factory creates a *family* of related products | Add a factory implementation |
| **Static Factory Method** | The class itself | Named constructor, e.g. `List.of`, `Optional.of` | Not about polymorphism at all |

The shortest way to remember it: **Simple Factory chooses with a `switch`.
Factory Method chooses with inheritance. Abstract Factory chooses a whole
family at once.**

## Where You Have Already Seen It

- `java.util.Calendar.getInstance()` — returns a locale-appropriate subclass
- `java.nio.charset.Charset.forName("UTF-8")` — a name in, an object out
- `DriverManager.getConnection(url)` — the URL decides the driver
- `NumberFormat.getCurrencyInstance(locale)`
- Nearly every `XxxFactory.create(...)` in a Spring codebase

## Try It Yourself

1. Run `./gradlew run` and read the output — the checkout lines are
   identical for all four methods; only the payment lines differ.
2. Add `WALLET` to `PaymentType` and try to compile. Read the error. That
   error is the pattern protecting you.
3. Then write `WalletPayment`, add it to the `permits` clause and to the
   `switch`. Notice `CheckoutService` and `SimpleFactoryDemo` need **zero**
   changes.
4. Replace the `switch` with a `Map<PaymentType, Supplier<PaymentMethod>>`
   and decide for yourself which you prefer.

## See Also

- [`problem-statement.md`](problem-statement.md) — the problem this solves
- [`class-diagram.md`](class-diagram.md) — static structure
- [`uml-diagram.md`](uml-diagram.md) — runtime call flow
- [`animation.html`](animation.html) — animated walkthrough
