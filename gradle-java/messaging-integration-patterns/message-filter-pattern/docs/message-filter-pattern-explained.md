# Message Filter, Explained

## The pattern in one sentence

A message filter stands between a channel and a receiver and passes on only
the messages that match its rule, so the receiver sees only what it wants.

## The 5 acts

### 1. Everything to everyone

`GiftWrapUnfiltered` subscribes to the orders channel and is handed all ten
orders. It checks each one and wraps the two gift orders, ORD-2 and ORD-4.
Eight deliveries were opened only to be ignored, and every other service
repeats checks of its own.

### 2. A filter

A `MessageFilter` with the rule "gift orders only" subscribes to the channel
in front of the gift-wrap service. The service receives exactly ORD-2 and
ORD-4; the filter dropped eight. Checkout still sends every order and knows
nothing about the filter.

### 3. Chained filters

Two filters are chained in front of the loyalty service: registered customers
only, then orders over £50. It receives ORD-1, ORD-4 and ORD-6. The first
filter dropped three guest orders, the second four orders under £50.

### 4. A changed rule

The bonus threshold rises to £60. Only the filter's rule changes; now the
loyalty service receives ORD-1 and ORD-4. Checkout and the loyalty service
were not touched.

### 5. The bill

Across the filters in this demo, fifteen messages were dropped and none was
kept anywhere. If a rule is wrong, real orders vanish without an error. Count
the drops, or send dropped messages to a discard channel, like a spam folder.

## The verdict

Use filters to give receivers on a shared channel only what they need. Keep
each rule small, chain them for combinations, and always count or keep what
they drop.

## How to recognise this in code you did not write

- `filter(...)` steps in Camel routes, Spring Integration flows or Kafka Streams.
- Subscription filters on cloud topics.
- Wrappers around consumers that check a condition before passing on.

## Where you have already met this

- Apache Camel's `filter` and Spring Integration's `<int:filter>`.
- Subscription filters in cloud messaging, such as SNS or Azure Service Bus.
- Kafka Streams' `filter` step.
- Email rules and spam filters.
