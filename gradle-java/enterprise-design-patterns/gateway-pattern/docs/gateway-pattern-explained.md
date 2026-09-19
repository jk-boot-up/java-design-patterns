# Gateway, Explained

## The pattern in one sentence

A gateway is one class that wraps access to an outside system, so the rest of the program speaks its own language and can be tested without the real thing.

## The six acts

### The Provider's Client, Everywhere

Checkout, renewal and gift card each build the provider's request and read its codes. Three network calls. The gift card top-up forgot the currency field, and nobody has noticed.

```
  checkout: paid, receipt AC-4999. renewal: renewed. gift card: topped up.
  three places build the provider's request fields and read its result codes. network calls made: 3.
  one of them forgot the currency field. nobody has noticed yet.
```

### One Door

The shop asks twice through the gateway. The first is approved and the second declined, and checkout has no field name and no result code in it.

```
  the shop asks: paid, receipt AC-4999.
  the shop asks again: card declined.
  Checkout has no field name and no result code in it. it speaks approved, declined and unavailable.
```

### Tests That Never Leave The Process

A fake gateway, told what to answer, gives approved, declined and unavailable, with no network calls at all.

```
  paid, receipt FAKE-1; card declined; payment provider unavailable, try again.
  asked of the fake: 3 times. network calls made: 0.
  the fake can be told to decline, or to be down, on demand. a real provider cannot.
```

### One Place For The Network's Habits

The gateway retries a single timeout once, so the shop is told paid. It made two network calls. After two timeouts it says unavailable. The rule lives in one class.

```
  the provider times out once, then answers. the shop is told: paid, receipt AC-4999.
  network calls: 2. log: [acme timed out on attempt 1].
  timing out twice: payment provider unavailable, try again.
  the retry rule lives in one class. the three naive callers would each have needed their own.
```

### Another Provider, The Same Shop

The same checkout runs on Acme and on a second provider with a completely different client. It was given a different gateway, and not changed.

```
  on Acme: paid, receipt AC-4999. on BetaPay: paid, receipt BP-4999.
  a large amount, on BetaPay: card declined.
  Checkout was not changed. it was given a different gateway.
```

### The Bill: What The Door Cannot Say

Acme can hold a payment and capture part of it later, and the interface has only charge. Adding it means a new method on the interface and on all three gateways, and BetaPay cannot do it at all.

```
  Acme can hold a payment and capture part of it later. the gateway interface has one method, charge.
  to use partial capture, a method is added to the interface, and to all 3 gateways: Acme, BetaPay and the fake.
  and BetaPay cannot do it at all, so the interface must say what happens then.
```

## The verdict

Put a gateway in front of any outside system your program depends on: a payment provider, a mail server, a remote API. Keep it small and in the program's own words. Put the system's habits in it: codes, retries, timeouts. Give tests a fake. Expect the interface to be the common ground, and decide on purpose what to do about features that only one provider has.

## How to recognise this in code you did not write

- An interface named for what the program needs, with an implementation named for the vendor.
- A `Fake` or `InMemory` implementation used in tests.
- A class that imports the vendor's SDK, which nothing else does.
- A wrapper around `RestTemplate`, `WebClient`, or a mail sender.

## Where you have already met this

Every payment, email, storage or search integration written by a careful team, and the reason Spring's `JavaMailSender` and `Repository` are interfaces.

## When this is too much

For a call made in one place to a system that will never change, a wrapper is one more class to read. It earns its place with several callers, or a need for a fake.
