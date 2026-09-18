# Clean Architecture with Spring, Explained

## What this project is, in one sentence

[`clean-architecture-pattern`](../clean-architecture-pattern)'s identical
object graph — same entities, same use cases, same adapters, copied
unchanged — assembled by a Spring `ApplicationContext` instead of by a
`main()` method, so the one contrast this project owns can be shown
directly: **hand-wiring fails at compile time; container wiring fails at
startup.**

This document does not re-teach Clean Architecture. See
[`../clean-architecture-pattern/docs/clean-architecture-pattern-explained.md`](../clean-architecture-pattern/docs/clean-architecture-pattern-explained.md)
for the pattern itself.

## Recognition: `@Bean` is those twenty lines

Read `AppConfig` next to `clean-architecture-pattern`'s
`PlaceAnOrderDemo.shop()` method:

```java
// clean-architecture-pattern — by hand
InMemoryProductRepository products = InMemoryProductRepository.seeded();
InMemoryOrderRepository orders = new InMemoryOrderRepository();
InMemoryNotificationGateway notifications = new InMemoryNotificationGateway();
PlaceOrderInteractor interactor =
        new PlaceOrderInteractor(products, orders, payments, notifications);
```

```java
// clean-architecture-with-spring — by container
@Bean
public PlaceOrderInputBoundary placeOrderInputBoundary(ProductRepository products,
        OrderRepository orders, PaymentGateway payments, NotificationGateway notifications) {
    return new PlaceOrderInteractor(products, orders, payments, notifications);
}
```

Same four arguments, same constructor, same class. The difference is who
calls it: there, a line in `main()`, when the program starts. Here, Spring,
once, when the context refreshes — matching each `@Bean` method's
parameter types against other `@Bean` methods' return types, in whatever
order satisfies them.

**`@Component` is not magic. It is those twenty lines**, discovered and
called by a container instead of typed by a person. A reader who has seen
both stops treating annotations as weather.

## The one contrast this project owns

Delete the `notifications` argument from the hand-wired call above, and the
project does not build. `javac` refuses it, in your editor, before you have
saved the file.

Delete the equivalent `@Bean` method — `notificationGateway()` — from
`AppConfig`, and nothing refuses anything. The file compiles. Every other
`@Bean` method compiles. The mistake is invisible until something actually
asks the context to build a `PlaceOrderInputBoundary`, at which point Spring
discovers, at runtime, that one of its four constructor parameters has
nothing to satisfy it, and throws `UnsatisfiedDependencyException` —
seconds into what looked like an entirely normal startup.

```
STARTUP FAILED: No qualifying bean of type
'com.jk.explore.cleanspring.usecases.NotificationGateway' available:
expected at least 1 bean which qualifies as autowire candidate.
```

`WiringContrastTest` proves both halves: the real configuration builds a
working `PlaceOrderInputBoundary`, and the broken one throws that exact
exception, naming the missing type.

**That is the whole cost of the convenience, honestly priced.** The
container will happily accept a graph with a hole in it, and tell you only
once it tries to use the hole.

## What this project does not do

It does not re-teach Clean Architecture — every entity, use case and
adapter here is `clean-architecture-pattern`'s file, unchanged, and its own
explained document is the authority on all of them. It does not teach
dependency injection from first principles either; that is
[Dependency Injection](../../foundational-design-patterns), a different
project. This one owns exactly one question — what changes when a
container does the assembling — and stops once it has answered it.

## When this is worth the extra dependency

Worth it the moment a real application has enough objects that hand-wiring
them all in one method stops being readable — which, in practice, is most
real applications past a handful of classes. Not worth it for learning the
architecture itself: that lesson is complete, and arguably clearer, with no
framework in the way at all — which is exactly why
`clean-architecture-pattern` is a separate project rather than a single
scene inside this one.
