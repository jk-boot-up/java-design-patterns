# Dependency Injection, Explained

## The pattern in one sentence

A class declares what it needs in its constructor and is given it.

## The signature is the dependency list

`CheckoutService(DiscountPolicy, PaymentGateway, Notifier)`. Complete, and checked by
the compiler. `new CheckoutService()` does not compile, so a collaborator cannot be
forgotten. It never looks anything up, so nothing is hidden, and it is valid the
moment it exists. A test builds one with fakes and needs no framework and no global
set-up.

## The wiring, by hand, first

```
TWO. The wiring, by hand, before any framework.
  the whole application is built in 9 lines of plain Java (blank lines included), in one place.
```

Nine lines, in `Wiring.build()`. That is what a container does for you. A container is
an optimisation of something you can write yourself.

## Three forms, and a recommendation

**Constructor injection.** Dependencies are mandatory and visible, and the object is
valid the moment it exists. This is the recommendation.

**Setter injection.** For genuinely optional things. The notifier has a setter and a
do-nothing default, and the order works without one.

**Field injection: discouraged.** The object can be built with `new` in an invalid
state, and it cannot be built validly in a test without a framework or the same
reflection.

```
THREE. Three forms: constructor, setter, field.
  field: new FieldInjectedCheckout() compiled, and is invalid. placing an order threw NullPointerException.
  it only works once something reaches into its private fields by reflection: receipt-1
```

## A container, written here

`MiniContainer` is 86 lines. It reads each constructor's parameter types, builds
whatever each needs, and calls the constructor. It built the same graph as the hand
wiring. That is all Spring, Guice and Dagger do, plus scanning, scopes and a great
deal of polish.

```
FOUR. A container, written here, in 86 lines.
  charged [9000], the same as before.
```

## The bill

The wiring has to live somewhere, and by hand it grows with the application. A
container solves that, and costs you magic.

```
FIVE. The bill.
  could not construct CheckoutService: no bean for its parameter of type Notifier
  circular dependency: Chicken -> Egg -> Chicken
```

A container that cannot build the graph fails when it **starts**, which is better than
Service Locator's first request, and still not at compile time. A circular dependency
is a start-up failure. And a class whose constructor takes seven things has a design
problem that no injection style fixes: the long constructor is telling you the class
does too much.

## The progression

Registry put things in a known place. Service Locator made a middleman that could find
them. Dependency Injection stopped the class asking at all.

## The verdict

Use constructor injection: by hand until the wiring hurts, then a container.

## How to recognise this in code you did not write

- A constructor whose parameters are interfaces, and a class that never calls `new`
  on its collaborators.
- Spring: `@Component` or `@Service`, with the collaborators as constructor parameters.
- Guice and Dagger: `@Inject` on a constructor.
- A `main` method, or a `Config` class, that builds everything in order.

## Where you have already met this

In every Spring Boot application, where `@Autowired` and constructor parameters do
what `Wiring.build()` does by hand. This project does not run Spring: the point is
that you do not need it to have understood it.

## When this is too much

Never for the idea. A container is too much for a small application that fits in
`main`.
