# Message Filter with Apache Camel, Explained

## The pattern in one sentence

With Camel, a message filter is a `filter()` step with a Simple rule in front
of each receiver, and rejects can be sent to a discard channel.

## The 5 acts

### 1. Every service gets every order

Checkout sends every order to one endpoint, and Camel multicasts each order to
every service. With no filter, the gift-wrap service is handed all ten orders
and must open each one to see whether it is a gift.

### 2. A filter in front

A `filter()` step goes in front of the gift-wrap service, with the rule
`${body.gift}` in Camel's Simple language. Only ORD-2 and ORD-4, the gift
orders, get through; eight are dropped. Checkout still sends every order to
the same endpoint and does not know the filter exists.

### 3. Two conditions

The loyalty service's rule has two conditions: the customer is registered,
and the order is over the threshold of £50. Written as one Simple expression
in a `choice()`, it lets through ORD-1, ORD-4 and ORD-6.

### 4. Change the rule while running

The threshold is not written into the route. The route reads it from a
settings object as each order passes. Raising it to £60 while the routes keep
running changes the result at once: ORD-1 and ORD-4. No route was changed or
restarted.

### 5. The bill, and a discard channel

A filter drops messages, and a wrong rule drops them silently. Camel makes
the safer shape one line: `otherwise().to("direct:discard")`. The eight orders
the loyalty rule rejected are kept there and can be counted. The costs: rules
written in strings that are only checked when they run, and more than ten
library files instead of none.

## The verdict

Use Camel's filter when many services subscribe to the same messages and
rules change. Keep rules short, read changing settings at run time, and add a
discard channel so nothing is lost without a trace.

## How to recognise this in code you did not write

- `.filter(simple("..."))` in a route.
- `choice().when(...).otherwise().to("...discard")`.
- `${body.x}` and `${header.y}` expressions.

## Where you have already met this

- Camel's `filter()` and Spring Integration's `@Filter`.
- Message selectors in JMS, and subscription filters in cloud queues.
- Email rules that sort or discard incoming mail.
