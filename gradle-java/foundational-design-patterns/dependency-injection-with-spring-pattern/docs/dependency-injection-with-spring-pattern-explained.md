# Dependency Injection with Spring, Explained

## The pattern in one sentence

Spring reads each constructor and builds the graph, so you write the constructors and it writes the wiring.

## What is new here

The pattern is [Dependency Injection](../dependency-injection-pattern). This page is what Spring adds.

**One annotation replaces one `new`.** `@Component` on a class says Spring should build it. Its
single constructor needs no `@Autowired`: Spring reads the parameter types.

```
TWO. What each annotation replaced.
  beans Spring built: [Auditor, CheckoutService, LoyaltyPolicy, ReceiptPrinter, RecordingGateway, RecordingNotifier, Storefront]
  one annotation per class replaced 7 lines of new. the constructors are untouched.
```

## Spring's start-up failures are the real ones

A missing bean fails when the context starts, naming the parameter:

```
THREE. A bean that is missing: a real Spring start-up failure.
  UnsatisfiedDependencyException, when the context starts:
  Error creating bean with name 'checkoutService': Unsatisfied dependency expressed through constructor parameter 2 ...
```

That is the same failure the hand-written container produced, and better than a locator's: at
start-up, not on the first order. It is still not at compile time.

A circular dependency is refused by default since Spring 6:

```
FOUR. A circular dependency.
  BeanCurrentlyInCreationException: Error creating bean with name 'chicken': Requested bean is currently in creation ...
```

## Field injection

Spring can fill a private `@Autowired` field. Nothing else can: `new` gives an invalid object.

```
FIVE. Field injection: Spring can fill it, nothing else can.
  new FieldInjectedCheckout() compiled, and placing an order threw NullPointerException.
```

Spring's own guidance is constructor injection.

## What the magic costs

A container adds start-up time and a place where objects come from that is not in your code.
The cost is paid once. The verdict is unchanged: constructor injection, by hand until the wiring
hurts, then a container. Spring did not add the idea. It removed the typing.

## Where you have already met this

In every Spring Boot application. This is where the annotations you copy from tutorials come from.

## When this is too much

For a small application that fits in `main`, hand wiring is shorter and has no magic.
