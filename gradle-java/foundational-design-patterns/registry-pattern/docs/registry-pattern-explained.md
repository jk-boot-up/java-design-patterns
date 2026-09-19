# Registry, Explained

## The pattern in one sentence

A well-known object that other objects find things in.

## How it works

`Registry.register(PaymentGateway.class, gateway)` puts a thing in. `Registry.get(PaymentGateway.class)`
takes it out, from anywhere. `RegistryCheckout` takes nothing in its constructor.

```
TWO. The pattern — a well-known place to ask.
  RegistryCheckout's constructor takes nothing. six constructors became none.
```

The friction is gone.

## The bill, and it arrives fast

A registry is a global variable with better manners.

**The dependencies become invisible.**

```
THREE. The bill: the dependencies are invisible.
  new RegistryCheckout() compiled and ran. its signature says it needs nothing.
  the first call failed: nothing is registered for DiscountPolicy
```

**Tests share global state, so one fails because of the order they ran in.**

```
FOUR. The bill: a test fails because of the order the tests ran in.
  order one: [checkoutChargesTheRealGateway: passed, refundTestLeavesItsGatewayBehind: passed]
  order two: [refundTestLeavesItsGatewayBehind: passed, checkoutChargesTheRealGateway: FAILED ...]
```

Neither test changed. The order did. This is the symptom teams meet first.

**"What is in it right now" cannot be read from any one file.**

```
FIVE. The bill: what is in it, right now?
  at start-up:            []
  after one class ran:    [DiscountPolicy]
  after two more:         [DiscountPolicy, Notifier, PaymentGateway]
```

**Thread safety becomes a question.** A static map shared by every thread has to
be a concurrent one.

## The verdict

Use a registry narrowly: for a very few things that are truly application-wide,
set up once at start-up and never changed. Not for collaborators that vary, or that
tests need to replace.

## The progression

Registry put things in a known place. [Service Locator](../service-locator-pattern)
makes a middleman that can find them. [Dependency Injection](../dependency-injection-pattern)
stops the class asking at all.

## How to recognise this in code you did not write

- A class with static `get`, `lookup` or `getInstance` methods, keyed by type or name.
- `System.getProperties()`, `Locale.getDefault()`, and static logger factories.
- A `Context` or `Environment` object passed everywhere, or reachable statically.
- `@BeforeEach` methods that clear something static, because tests leaked into each other.

## Where you have already met this

Every static `getInstance()` or `Context.get()` is a relative.

## When this is too much

For nearly everything that is not truly application-wide.
