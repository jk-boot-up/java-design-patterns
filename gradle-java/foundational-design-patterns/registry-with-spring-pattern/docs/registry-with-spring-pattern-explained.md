# Registry with Spring, Explained

## The pattern in one sentence

Spring's `ApplicationContext` is a registry: things are found by type.

## What Spring fixes

**Registration is declared, not scattered.** `@Component` on a class replaces `Registry.register(...)`
calls in unknown places. **A missing bean fails at start-up**, not on the first call. And the
best use of the registry is never to call it: constructor injection means a class is *given* what
it needs.

```
TWO. Used well, nobody calls it. Used badly, it is the hand-built registry again.
  InjectedCheckout is given its collaborators: receipt-1
  LocatorStyleCheckout calls context.getBean three times: receipt-2
  new LocatorStyleCheckout() compiled, and threw NullPointerException: it needs Spring to hand it the context.
```

A `getBean` inside a business class is a [Service Locator](../service-locator-pattern) with all its
costs: a constructor that takes nothing, and dependencies invisible again.

## The failure of its own: shared state through the context cache

Spring's test support caches a context and reuses it across tests with the same configuration. The
gateway is a singleton, so it remembers.

```
THREE. The failure of its own: shared state, through the context cache.
  test A ran on the shared context and charged once. the gateway is a singleton, so it remembers: [9000]
  test B, on the same cached context, starts by expecting a clean gateway. it sees: [9000]
  a fresh context (what @DirtiesContext gives) sees: [], at the price of starting Spring again.
```

This project's tests prove it with real Spring: `SharedContextLeakTest` has a second test that
passes only because the first ran before it. `@DirtiesContext` is the fix, and costs a new context.

## The Environment is a registry of strings

```
FOUR. The Environment is a registry of strings.
  checkout.curency (a typo) = null, where the right answer was GBP. no error, no warning.
  a required @Value with the same typo fails when the context starts:
  Could not resolve placeholder 'checkout.curency' in value "${checkout.curency}"
```

The untyped lookup is silent. The injected one is not.

## Asking by type is ambiguous with two

```
FIVE. Asking by type is ambiguous the moment there are two.
  context.getBean(Notifier.class) with two Notifiers: NoUniqueBeanDefinitionException
```

A run-time error at the call site, not a compile error.

## The verdict

Spring's context is the registry done well: declared, checked at start-up, and mostly never called.
Keep `getBean` to `main`, to tests and to framework glue. In business code, inject. And keep singleton
state out of anything a test shares.

## Where you have already met this

Every `@Autowired` lookup goes through it. Every `@SpringBootTest` shares one.

## When this is too much

Never for the context itself: you already have one. The cost is in calling it.
