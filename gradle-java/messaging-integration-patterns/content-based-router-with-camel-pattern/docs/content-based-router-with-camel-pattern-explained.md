# Content-Based Router with Camel, Explained

## The pattern in one sentence

A content-based router looks inside each message and sends it to a different channel depending on what it contains, so that senders and receivers never have to know about each other.

## What Apache Camel changes

Nothing about the idea. Two things about the shape.

The first is that the rules stop being code you step through and become a route you declare. You write down, once, where messages come from, the list of questions to ask about each one, and the destination each answer leads to. Camel runs that description. The questions are asked in the order you wrote them, and the first one answered yes decides.

The second is what happens to a message that none of the questions claims. The hand-built router had a fallback channel, and when there was no fallback it dropped the message and *counted* it, so at least the number was visible. Camel has no counter. A route whose questions all say no, with no otherwise branch to catch it, simply ends. The broker is told the message was handled. The message is then on no queue anywhere.

## The words, in plain language first

A **queue** is a named line that messages wait in until somebody takes them. An **exchange**, to the broker, is the post box a sender drops a message into; it keeps nothing and only passes the message on. A **routing key** is the short label on the message that tells the broker which queue it belongs in.

A **route**, to Camel, is a written description of where messages come from, what is decided about them, and where they go. An **endpoint** is one end of a route: a queue to read from, or a queue to write to. An **exchange**, to Camel — a different meaning from the broker's — is the message while it travels. A **predicate** is a yes-or-no question asked about it.

An analogy that costs nothing to carry. Think of a sorting office. Letters arrive in one sack. A sorter picks up each letter, reads the address on it, and drops it into one of several pigeonholes. The sorter does not know who posted the letter and does not know who will collect it. That sorter is the router, the address is the content, and the pigeonholes are the queues. Now imagine a letter whose address matches none of the pigeonholes. If there is a tray marked "look at these by hand", the letter goes there. If there is not, and the sorter simply puts it down, it is lost, and nobody ever finds out.

## The six acts

Every figure below is the output of `./gradlew run`.

### One Queue For Everything

There is no router. All six orders are posted to the warehouse's own queue, and the warehouse is left to sort out what it can do. It can pack and post the three physical ones. It can do nothing at all with the other three, which are two digital orders and a subscription. So the warehouse grows an if for every kind of order, and every new kind of order means changing the warehouse.

```
  all 6 orders arrived on the warehouse's own queue. it shipped 3 and could do nothing with 3.
  the warehouse now holds an if for every kind of order, and every new kind means changing the warehouse.
```

### The Route Reads The Content And Chooses

Now a Camel route reads the orders queue. It asks four questions, in this order. Is this order worth a thousand pounds or more? Is it digital, with nothing to put in a box? Was express delivery paid for? Is it a physical thing at all? The first question answered yes decides, and anything none of them claims goes to the manual review queue, which is the branch Camel calls otherwise.

The very high value order goes to fraud review even though it is physical, because the value question is asked first. The two digital orders go to digital delivery. The express one goes to express shipping. The ordinary physical one goes to standard shipping. The subscription, which nothing covers, goes to manual review.

```
  ORD-1 (physical, express, UK, 49.99) -> express-shipping
  ORD-2 (digital, none, UK, 25.00) -> digital-delivery
  ORD-3 (physical, standard, EU, 1200.00) -> fraud-review
  ORD-4 (digital, none, UK, 900.00) -> digital-delivery
  ORD-5 (subscription, none, UK, 9.99) -> manual-review
  ORD-6 (physical, standard, EU, 30.00) -> standard-shipping
  {express-shipping=[ORD-1], standard-shipping=[ORD-6], digital-delivery=[ORD-2, ORD-4], fraud-review=[ORD-3], manual-review=[ORD-5]}.
  the shop's route asks 4 questions about the content in a fixed order, and nothing but the route knows the answers.
```

### The First Question Answered Yes Wins

One digital gift card, worth fifteen hundred pounds, sent through two routes that ask the same four questions in two different orders. With the high value question asked first it goes to fraud review. With the same question asked last it goes to digital delivery, because the digital question was reached first and answered yes. Same order, same broker, same four questions, different answer.

```
  a digital gift card worth 1500.00. with the high value question asked first: fraud-review. with it asked last: digital-delivery.
  the order of the questions is part of the design, and Camel does not warn you when it changes.
```

### A Message No Question Claims

A subscription order. Not high value, not digital, not express, not physical. Every question says no.

Sent through the route that has an otherwise branch, it arrives on the manual review queue, where a person will see it.

Sent through a route with no otherwise branch, the route ends. The count of messages left anywhere in the shop, on any of the ten queues, is zero. The broker was told the message had been handled, so the broker no longer has it either. Nothing was logged, nothing was counted, and nobody was told.

Sent through a route whose otherwise branch goes to a queue named for the problem, it lands on a queue called unclaimed, and that queue is the entire difference between an order that is lost and an order that is known about.

```
  a subscription order, which no question covers. with an otherwise branch it goes to: manual-review.
  with no otherwise branch the route simply ends. messages left anywhere in the shop: 0. the broker was told it was handled, so it is gone.
  an otherwise branch that names the problem sends it to: unclaimed, where somebody can look at it. that queue is the whole difference between a lost order and a known one.
```

### A New Question, And Nobody Else Changes

A fifth question is added, asked after the other four: is this order from inside the European Union, so the tax has to be worked out before it ships? The route goes from four questions to five. No sender was changed. No receiving queue was changed. Only the route was.

An order that is a subscription from the European Union used to fall through to manual review. It now goes to the VAT check. But the ordinary physical order from the European Union still goes to standard shipping, because the physical question is asked earlier and is answered yes first.

```
  questions before: 4, after: 5. the senders and the receiving queues were not touched; only the route was.
  an EU subscription used to go to manual-review. it now goes to: eu-vat-check.
  ORD-6, physical and from the EU, still goes to: standard-shipping, because an earlier question was answered yes first.
```

### The Bill

Three costs.

The first is coupling to the content. The sender starts calling physical orders goods instead of physical. The route's question still looks for the word physical, so it is answered no, and the order lands on manual review without a word being said about why.

The second is failure, which is not the same as no match. The fraud branch is broken: the service behind it does not answer. Camel tried it three times, which is the first attempt plus the two redeliveries it was told to make, and then put the order on an errors queue, which ended up holding one message. A route can fail as well as choose, and somebody has to say in advance where the failures go — or they go the same way an unclaimed message goes, which is nowhere.

The third is the running cost. The routing is now a broker and a route to keep running: one container, one exchange and ten queues.

```
  the sender starts calling physical orders goods. the route's question still looks for physical, so ORD-9 lands on: manual-review, quietly.
  the fraud branch is broken. Camel tried it 3 times and then put the order on router-errors, which now holds 1. a route can fail as well as choose, and somebody has to say where the failures go.
  and the routing is now a broker and a route to keep running: this demo needed 1 container, 1 exchange and 10 queues.
```

## What the simulation got right, and what it left out

**Right.** The idea, exactly. Rules in a deliberate order. The first match winning. A fallback. The insight that a router which reads the body is coupled to the body's format. Adding a rule without touching anybody else. All of that survives contact with the real tool unchanged, which is the best thing you can say about a teaching model.

**Left out.** Four things.

One: the router in the simulation was a method you called, so the rules and the callers were in one process and one thread. Here the message genuinely leaves the process, and the destination is a queue that some other program will read at some other time.

Two: the simulation counted what it dropped. Camel does not. A dropped message in the simulation was a number you could assert on; a dropped message here is silence, and you only find out when a customer asks where their order went.

Three: the simulation's rules could not fail. A predicate either matched or did not. In a real route a branch calls something that can be down, and the question of what happens to a message whose handling failed is a separate design decision from the question of what happens to a message that matched nothing.

Four: the simulation had no operational cost. Here there is a broker to run, queues to declare, a route to deploy, and a second way of describing behaviour that every reader of the codebase has to learn.

## The verdict

Use a content-based router when one stream carries messages that need different handling and the difference is in the content. With Camel in particular: write the questions in a deliberate order and test that order, because nothing will warn you when somebody reorders them. Always write an otherwise branch, and send it somewhere named for the problem rather than into a general inbox. Always configure an error handler, because a branch that fails is not the same as a branch that does not match. And prefer asking a question about a header the sender filled in on purpose over reaching into the body, at the cost of the sender having to fill it in.

## How to recognise this in code you did not write

- Camel's `choice().when(...).otherwise(...)` in a `RouteBuilder`.
- Spring Integration's `router`, and a `@Router` annotated method.
- A RabbitMQ topic exchange with several bindings, doing the same job in the broker instead.
- An `if` chain inside a message listener that decides which service to call next.
- A queue with a name like `unroutable`, `parking-lot` or `manual-review`, which is somebody's otherwise branch.
