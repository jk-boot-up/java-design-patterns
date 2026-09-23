# Problem Statement

## Read the partner first

This project assumes [Content-Based Router](../content-based-router-pattern), which built a router by hand: a list of rules in order, a fallback for anything no rule covered, and a count of what it dropped. Nothing about the idea is lost by skipping Apache Camel, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's. An online store takes orders of several kinds at once. Some are physical goods the warehouse packs and posts. Some are digital, a gift card or a download, and there is nothing to put in a box. Some were paid for with express delivery and have to go out today. Some are worth so much that a person should look at them before anything is shipped. And a few are none of those.

## What is new

**Apache Camel**, doing the routing, over a **real RabbitMQ broker** running in a container that the demo starts and removes again.

Two things change. The first is that the rules are no longer an if chain inside a receiver; they are a route, written out once, that says where messages come from, what is asked about each one, and where each answer sends it. The second is that the message really does leave the process. It is put on a queue by one program, and taken off a different queue by another, with the broker in between.

The naive version is still the same naive version, and it still hurts:

```
  all 6 orders arrived on the warehouse's own queue. it shipped 3 and could do nothing with 3.
  the warehouse now holds an if for every kind of order, and every new kind means changing the warehouse.
```

## The failure this project exists to show

A message that no question in the route claims. In the hand-built version that message was dropped and counted, because the hand-built router counted it. Camel does not count it. If the route has no otherwise branch, the route simply ends, the broker is told the message was handled, and the order is gone from every queue in the shop. Nothing raises an alarm and nothing keeps a copy.

```
  with no otherwise branch the route simply ends. messages left anywhere in the shop: 0. the broker was told it was handled, so it is gone.
```

There is a second failure the simulation could not have. A branch of the route can fail rather than merely miss: the fraud check can be down. Camel then retries the message a fixed number of times and, if it is told where to, puts it on an errors queue instead. If it is not told where to, that message is lost the same way.

## What this project must deliver

A real broker in a container, started and stopped by the demo. Six orders routed by their content through a declared Camel route. Two orderings of the same questions giving two answers for the same order. A message no question claims, shown three ways: caught by an otherwise branch, lost when there is no otherwise branch, and kept on a queue named for the problem. A question added with no change to any sender or receiver. A renamed field that makes every question miss. And a broken branch that ends on an errors queue after a counted number of attempts.
