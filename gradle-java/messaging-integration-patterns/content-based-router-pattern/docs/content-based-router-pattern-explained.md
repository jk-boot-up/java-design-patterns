# Content-Based Router, Explained

## The pattern in one sentence

A content-based router looks inside each message and sends it to a different channel depending on what it contains, so senders and receivers never have to know about each other.

## The six acts

### One Channel For Everything

All six orders arrive on the warehouse's channel. Two are gift cards and one is neither, so the warehouse needs an if for each kind.

```
  all 6 orders arrive on the warehouse's channel. 2 are gift cards, which nothing physical can be done for, and 1 is neither.
  the warehouse now has an if for each kind, and every new kind means changing the warehouse.
```

### A Router Looks Inside

Each order goes where its content says. The physical orders go to the warehouse, the gift cards to digital delivery, the very high value one to fraud review, and the subscription, which no rule covers, to manual review.

```
  ORD-1 (physical, UK, 4999) -> warehouse
  ORD-2 (gift-card, UK, 2500) -> digital-delivery
  ORD-3 (physical, EU, 120000) -> fraud-review
  ORD-4 (gift-card, UK, 90000) -> digital-delivery
  ORD-5 (subscription, UK, 999) -> manual-review
  ORD-6 (physical, EU, 3000) -> warehouse
  {warehouse=[ORD-1, ORD-6], digital-delivery=[ORD-2, ORD-4], fraud-review=[ORD-3], manual-review=[ORD-5]}.
```

### The First Rule That Matches Wins

A gift card for fifteen hundred pounds goes to fraud review if the high value rule is first, and to digital delivery if it is last. The order of the rules is part of the design.

```
  a gift card for 1500.00. with 'high value' first: fraud-review. with it last: digital-delivery.
  the order of the rules is part of the design, and nothing warns you when it changes.
```

### Nothing Matches

A subscription order no rule covers goes to manual review when there is a fallback channel, and goes nowhere when there is not. A router with no fallback loses what it does not recognise.

```
  a subscription order, which no rule covers. with a fallback channel: manual-review.
  with no fallback: nowhere. orders dropped and counted: 1.
  a router with no fallback loses what it does not recognise, and says nothing.
```

### A New Route, And Nobody Else Changes

One rule is added, from three to four. An EU subscription now goes to a VAT check. Senders and receivers were not touched. A physical EU order still goes to the warehouse, because an earlier rule matched first.

```
  rules before: 3, after: 4. senders and receivers were not touched.
  an EU subscription, which nothing before it covers, now goes to: eu-vat-check.
  ORD-6 (physical, EU) still goes to: warehouse, because an earlier rule matched first.
```

### The Bill

The sender starts calling physical orders goods, and the router's rule for physical misses them and sends them to manual review. The router is coupled to the format of the content, and every route is a rule to test.

```
  the sender starts calling physical orders 'goods'. the router's rule looks for 'physical': manual-review.
  the router reads the content, so it is coupled to the content's format. routing on a header keeps that in the envelope, at the cost of the sender having to fill it in.
  every route is a rule to test, and rules grow: this shop has 3 today.
```

## The verdict

Use a content-based router when one stream carries messages that need different handling, and the difference is in the content. Order the rules on purpose, always have a fallback that keeps and reports what it cannot route, and prefer routing on a header that the sender sets deliberately over reaching into the body. Test every rule and the order between them.

## How to recognise this in code you did not write

- A method that returns a channel or queue name from a message.
- Apache Camel's `choice().when(...)`, Spring Integration's `router`.
- RabbitMQ topic exchanges and routing keys.
- An `if` chain that chooses a queue, in the sender.

## Where you have already met this

Enterprise service buses, API gateways that route by path, and mail rules that file messages by sender.

## When this is too much

If there is only one destination, or the sender already knows where each message goes, a router is a step for nothing.
