# Callback, Explained

## The pattern in one sentence

A callback is a piece of code you hand to someone else, to be called when something you asked for has happened.

## The six acts

### Ask, And Keep Asking

The answer arrived on the fifth look. Five looks were made, and four of them found nothing. And the caller could do nothing else in that time.

```
  the answer arrived on the 5th look. looks made: 5, 4 of them found nothing.
  and the caller could do nothing else in that time.
```

### Say What To Do, And Go On

The charge is requested, and the caller goes on. The caller does other work. Then the callback runs: order one, paid.

```
  [charge requested, and the caller goes on, caller does other work, callback: ORD-1 paid].
```

### What Happened Decides What To Do

One callback, told the result. Order one was paid: ship it. Order two was declined: ask for another card.

```
  one callback, told the result: [ORD-1: ship it, ORD-2: ask for another card].
```

### When The Callback Fails

The first callback threw an error. The gateway went on, and order two was paid. The error was recorded: order one, the mail server was down. The one who asked never sees that exception, because it happened in someone else's call.

```
  the first callback threw. the gateway went on: [ORD-2 paid]. recorded: [ORD-1: the mail server was down].
  the one who asked never sees that exception, because it happened in someone else's call.
```

### Answers In Another Order

Remembering the order in a field: both callbacks say order two. Each callback holding its own order id: order two paid, order one paid. The answers came in the other order, and each is right.

```
  remembering the order in a field: [ORD-2 paid, ORD-2 paid]. both say ORD-2.
  each callback holding its own order id: [ORD-2 paid, ORD-1 paid]. the answers came in the other order, and each is right.
```

### The Bill

Pay, then reserve, then ship: three callbacks, each inside the one before, three levels deep. The lines run in one order, but are written in another: in the code, the line that asks stock is written below the block that ships, and it runs first. Every level needs its own handling for a failure. And each answer arrives with no stack that shows who asked.

```
  pay, then reserve, then ship: three callbacks, each inside the one before, three levels deep.
  the order the lines run in: [1. all asked for, first step only, 2. paid, 3. stock asked, 4. reserved, 5. next step asked, 6. shipped]. in the code, the line that asks stock is written below the block that ships, and it runs first. that is not the order they are written in.
  and every level needs its own handling for a failure, and each answer arrives with no stack that shows who asked.
```

## The verdict

Use a callback when you ask for something that takes a while, and want to go on. Pass the result to it. Let each callback carry what it needs, not read shared fields. Decide who handles a failure in the callback. When steps chain, move to futures or an async style, so the code reads in order.

## How to recognise this in code you did not write

- A parameter named `onSuccess`, `onComplete` or `handler`.
- `CompletableFuture.thenAccept(...)`, and `whenComplete(...)`.
- Event handlers in a browser or in Swing, and Node.js style callbacks.
- `Consumer<Result>` passed to an async method.

## Where you have already met this

Every GUI toolkit's button handlers, Node.js's I/O API, payment and webhook integrations, and `CompletableFuture`.

## When this is too much

For work that is quick, a plain return value is simpler. For chains of steps, futures or coroutines read better than nested callbacks.
