# Problem Statement

## The Scenario

You are building the payment step of an online store. When a customer
reaches the payment page they pick how they want to pay, and your code has
to run the right one:

| Payment method | What it does |
| --- | --- |
| `CreditCardPayment` | Authorises the card, then captures the amount |
| `UpiPayment` | Sends a collect request and waits for approval |
| `PayPalPayment` | Redirects to PayPal and comes back with a result |
| `NetBankingPayment` | Hands off to the customer's bank login page |

They all do the same job from the outside — take a `PaymentRequest`, give
back a `PaymentReceipt` — so they share one interface:

```java
public interface PaymentMethod {
    String displayName();
    PaymentReceipt pay(PaymentRequest request);
}
```

The choice arrives as data. It comes from a dropdown, a JSON field, a
database column — a `String` or an enum, not a Java type. Somewhere,
something has to turn that value into an object.

## The Naive Approach (and why it hurts)

Without a factory, the caller decides for itself:

```java
// Inside a web controller, a mobile API, a CLI admin tool, a batch job...
PaymentMethod method;
if (type.equals("CREDIT_CARD")) {
    method = new CreditCardPayment();
} else if (type.equals("UPI")) {
    method = new UpiPayment();
} else if (type.equals("PAYPAL")) {
    method = new PayPalPayment();
} else if (type.equals("NET_BANKING")) {
    method = new NetBankingPayment();
} else {
    throw new IllegalArgumentException("Unknown type");
}

PaymentReceipt receipt = method.pay(request);
```

This creates real problems:

- **The client knows too much.** A class whose job is "check out" now knows
  the name of every payment class in the system, and how to construct each
  one.
- **Duplication.** The web controller, the mobile API and the admin tool
  each repeat the same chain — and each can drift out of sync. One of them
  will forget to trim the string; one of them will forget PayPal exists.
- **Change ripples outward.** Add wallet payments tomorrow and you must
  find and edit *every* caller. Miss one and it fails at runtime with an
  "Unknown type" that nobody sees until a customer hits it.
- **Construction leaks.** The day `CreditCardPayment` needs a gateway URL in
  its constructor, every one of those `new` calls has to change.
- **Hard to test.** You cannot test the selection logic on its own, because
  it is welded to the checkout code around it.

Notice what is *not* the problem: the four payment classes themselves are
fine. Small, independent, easy to read. The mess is entirely in the
choosing.

## The Question This Project Answers

> How do we let the caller say **which** payment method it wants, without
> the caller knowing **how** any of them are built?

## The Goal

Move the choosing into one place:

```java
PaymentMethod method = PaymentMethodFactory.create(PaymentType.UPI);
PaymentReceipt receipt = method.pay(request);
```

...where the caller:

- names the method it wants, as **data**,
- receives something it only knows as a `PaymentMethod`,
- never writes `new CreditCardPayment()`,
- and does not change when a fifth payment method is added.

The `if`/`else` chain does not vanish — it becomes a `switch` inside the
factory. That is the honest trade: the knowledge still exists, but it lives
in exactly one file that you can open, read and change.

This is precisely the problem the **Simple Factory** idiom solves. See
[`simple-factory-pattern-explained.md`](simple-factory-pattern-explained.md)
for how, and for where it stops being enough.
