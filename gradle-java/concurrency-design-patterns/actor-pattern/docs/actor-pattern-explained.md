# Actor, Explained

## The pattern in one sentence

An actor is an object that owns some state, has a mailbox, and handles one message at a time on its own thread, so that its state is never touched by two threads and nothing can reach in except by sending a message.

## The six acts

### State That Many Threads Can Reach

Ten in stock, and two orders, for three and for four, read the stock at the same moment. It should be three left, and it is not. One of the two reservations was lost.

```
  10 in stock. two orders, for 3 and for 4, read the stock at the same moment. it should be 3 left. it is 3 left: false. one of the two reservations was lost.
  every method looked correct. the state was open to anyone.
```

### State That One Actor Owns

Four threads each send a thousand reservations to an inventory of four thousand. Stock left: zero. There is no lock in the inventory.

```
  4 threads each send 1000 reservations of 1 mug to an inventory of 4000. stock left: 0.
  no lock in the inventory. the actor handled one message at a time, so none was lost.
```

### Ask, And Be Answered By A Message

Reserving three of five is answered with a reserved message. Reserving three more is answered with an out of stock message, saying two are left. No exception crossed between the two.

```
  reserve 3: Reserved[sku=MUG-BLUE, quantity=3].
  reserve 3 more: OutOfStock[sku=MUG-BLUE, wanted=3, left=2].
  the answer is a message too, and it can be a refusal. no exception crossed between the two.
```

### Nobody Can Reach In

The inventory actor has no public method that returns its stock. The only way to learn it is to ask, and the answer is a copy.

```
  the inventory actor has a public method that returns its stock: false.
  the only way to learn the stock is to ask, and the answer is a copy: 5.
```

### Let It Crash

A message the actor cannot handle fails, the sender is told, and the actor is restarted. The next message is handled. One bad message did not stop the actor. The restart put the stock back to its starting value.

```
  after reserving 2, stock is: 3.
  a message the actor cannot handle: the sender is told, 'a message this actor cannot handle'.
  the actor was restarted: restarts 1. the next message is handled: Reserved[sku=MUG-BLUE, quantity=1].
  one bad message did not stop the actor, or the others.
  the stock after the restart: 4 (it started at 5, and was back to 5 before that last reservation).
```

### The Bill

Two actors that each ask the other and wait for the answer never get one. There are no locks, and still a deadlock. A restart forgets state, messages are copied, mailboxes can grow, and finding where a message went takes tools.

```
  two actors each ask the other, and wait for the answer before doing anything else: no answer.
  no locks, and still a deadlock: each is waiting for a message the other can never send.
  and a restart forgets: an actor's state is gone unless it was written somewhere else. messages are copied, mailboxes can grow, and finding where a message went takes tools.
```

## The verdict

Use actors for state that many parts of a program need to change, where one owner and messages are clearer than locks: a stock count, a session, a connection. Keep messages small and immutable. Do not wait for a reply inside a handler. Decide what a restart does to the state. Use a library such as Akka or Pekko rather than writing the mailbox yourself.

## How to recognise this in code you did not write

- A class with a mailbox, a `receive` method and a single thread.
- Akka's `ActorRef` and `tell` and `ask`, Erlang processes, Elixir's GenServer.
- Message classes that are records or case classes.
- A supervisor strategy that says what to do when a child fails.

## Where you have already met this

Akka and Pekko, Erlang and Elixir systems, and Vert.x verticles, which follow the same idea.

## When this is too much

For a counter, an `AtomicInteger` is simpler. Actors earn their place when the state is more than one number, and many parts of the system need to change it.
