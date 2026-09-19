# Service Locator, Explained

## The pattern in one sentence

A middleman that knows how to find or create what you ask for.

## The bill, as evidence

Service Locator is widely regarded as an anti-pattern. Here is why, shown rather
than asserted.

**The dependencies are still hidden, and the compiler says nothing.**

```
THREE. The bill: the compiler says nothing while a dependency is missing.
  production is configured, and somebody forgot the notifier.
  new LocatorCheckout() compiled, and constructed. the build was green.
  then, at run time, on a real order: no service is configured for Notifier
  and the customer was already charged: [9000] pence.
```

The failure arrives in production, after the money moved, not in the build.

**Every class now depends on the locator.**

```
FOUR. The bill: every class now depends on the locator.
  classes that call ServiceLocator: [Auditor, LocatorCheckout, ReceiptPrinter]
```

Each is otherwise pure domain logic, now coupled to infrastructure everywhere.

**Testing needs the locator configured**, so a unit test is never quite a unit test.

**A missing registration is a runtime error**, and act three produced it.

## Where it is still right

Plug-in systems, where what is available is not known until run time. Java's own
`java.util.ServiceLoader` is this pattern in the standard library, and it is nobody's
mistake.

```
FIVE. Where it is still right: what is available is not known until run time.
  java.util.ServiceLoader found these payment plug-ins, listed in META-INF/services: [card, bank transfer]
```

## The verdict

Prefer the alternative. For business logic, do not ask; be given. Keep a locator for
plug-in systems, and for the composition root of a small application.

## The moment it hands over

The whole difficulty is the word *ask*. The class asks, so nobody outside it knows
what it needs. [Dependency Injection](../dependency-injection-pattern) removes the asking.

## How to recognise this in code you did not write

- `find`, `lookup`, `getBean` or `resolve` called from inside business classes.
- `ServiceLoader.load(...)`, `InitialContext.lookup(...)` (JNDI).
- `applicationContext.getBean(X.class)` inside a class that is itself a bean.
- A class with a no-argument constructor that plainly needs several collaborators.

## Where you have already met this

Spring's `ApplicationContext.getBean()`, when called from a class Spring created, is a
locator inside a container.

## When this is too much

For business logic. It is right for plug-ins and for the composition root.
