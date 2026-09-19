# Chain of Responsibility with Spring, Explained

## The pattern in one sentence

In Spring, the links are beans of one interface, and the container hands you the list in order.

## What is new here

The pattern is [Chain of Responsibility](../chain-of-responsibility-pattern). This page is only what Spring Boot adds.

### Spring Builds The Chain

Spring injects the four links sorted by their order numbers, which live on four different classes.

```
  order: [address, stock, fraud, payment-limit].
  the order comes from @Order numbers on four different classes.
```

### Five Requests

Five requests go through. Each is answered by one link, and the report lists the links that never ran.

```
  asha   APPROVED  by fallback       no check had an opinion
  erin   REJECTED  by address        the address does not exist
         never ran: [stock, fraud, payment-limit]
  ben    REJECTED  by stock          an item is out of stock
         never ran: [fraud, payment-limit]
  carol  REJECTED  by fraud          fraud score 90
         never ran: [payment-limit]
  dev    REFERRED  by payment-limit  over the single-payment limit
```

### The Order Is The Cost

With the cheap checks first, only three of five requests reach the paid fraud service. With it first, all five do.

```
  paid fraud-service calls for five requests, cheap checks first, as @Order has it: 3.
  the same checks with the paid one first [fraud, address, stock, payment-limit]: 5.
```

### A Link That Throws

When the fraud service is down, the link throws. The chain catches it and refers the order to a person.

```
  asha   REFERRED  by fraud          fraud check failed: fraud service unavailable
  the chain turned an exception into a referral, and the caller saw no error.
```

### Switched Off By A Property

A property removes the fraud link from the chain. The risky customer is approved.

```
  order: [address, stock, payment-limit].
  carol  APPROVED  by fallback       no check had an opinion
  no code changed, and the risky customer is no longer stopped.
```

### Nobody Answers

If no link answers, a fallback does. It is a named setting.

```
  asha   APPROVED  by fallback       no check had an opinion
  asha   REFERRED  by fallback       no check had an opinion
  the fallback is a named setting, screening.fallback, not an accident.
```

## The verdict

Put cheap and decisive links first. Decide what a throwing link means. Print the order at startup. Test the chain as a whole.

## How to recognise this in code you did not write

- `List<SomeInterface>` in a constructor, with `@Order` on the implementations.
- A loop that stops at the first non-empty answer.
- `@ConditionalOnProperty` on one of the links.

## Where you have already met this

Servlet filters, Spring Security's filter chain, and validation pipelines.

## When this is too much

For two checks that never change, an if statement is clearer than a chain.
