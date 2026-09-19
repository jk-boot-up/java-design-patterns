# Actor Pattern — Video Narration Script

## 1. Actor

Hello, and welcome. This video explains the Actor pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: an actor is an object that owns some state, has a mailbox, and handles one message at a time on its own thread. Its state is never touched by two threads, and nothing can reach in except by sending it a message. This is another project in the concurrency category, whose subject is how threads share work and state without corrupting either. In our online store, the state that many threads want to change is the stock of a product. By the end you will see shared stock lose an update, see one actor own it and lose nothing, see answers come back as messages, see that nobody can reach inside, see a bad message restart the actor, and see the bill, which is a deadlock with no locks, and state that a restart forgets.

## 2. The Scenario

Here is the scenario. Many threads place orders in the online store, and every order reserves stock. The stock must never go wrong, however many orders arrive at the same moment. The question: do we guard it with locks, or with something else?

## 3. State That Many Threads Can Reach

First, state that many threads can reach. Ten in stock. Two orders, for three and for four, read the stock at the same moment. It should be three left. It is not. One of the two reservations was lost. Every method looked correct. The state was open to anyone.

## 4. The Pattern

The pattern. An actor owns some state. It has a mailbox, and one thread that takes one message at a time. Nobody else can touch the state. Everyone else sends messages, and, if they want an answer, gets a reply message back.

## 5. State That One Actor Owns

Second, state that one actor owns. Four threads each send a thousand reservations, to an inventory of four thousand. Stock left: zero. There is no lock in the inventory. The actor handled one message at a time, so none was lost.

## 6. Ask, And Be Answered By A Message

Third, ask, and be answered by a message. Reserve three of five: the reply is reserved. Reserve three more: the reply is out of stock, with two left. The answer is a message too, and it can be a refusal. No exception crossed between the two.

## 7. Nobody Can Reach In

Fourth, nobody can reach in. The inventory actor has no public method that returns its stock. The only way to learn the stock is to ask, and the answer is a copy. Nobody holds the real thing, so nobody can change it behind the actor's back.

## 8. Let It Crash

Fifth, let it crash. After reserving two, the stock is three. Then a message the actor cannot handle. The sender is told what went wrong, and the actor is restarted. The next message is handled as normal. One bad message did not stop the actor. But the restart put the stock back to five. The state was reset.

## 9. The Bill

Last, the bill. Two actors that each ask the other, and wait for the answer, never get one. There are no locks, and still a deadlock: each is waiting for a message the other can never send. A restart forgets state, unless it was written somewhere else. Messages are copied. Mailboxes can grow. And finding where a message went takes tools.

## 10. How To Recognise It

How do you recognise this in code you did not write? A class with a mailbox, a receive method and a single thread. Akka's ActorRef and tell and ask, Erlang processes, Elixir's GenServer. Message classes that are records or case classes. A supervisor strategy that says what to do when a child fails.

## 11. The Verdict

Here is my verdict, plainly. Use actors for state that many parts of a program need to change, where one owner and messages are clearer than locks: a stock count, a session, a connection. Keep messages small and immutable. Do not wait for a reply inside a handler. Decide what a restart does to the state. Use a library such as Akka or Pekko rather than writing the mailbox yourself.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? For a counter, an AtomicInteger is simpler. Actors earn their place when the state is more than one number, and many parts of the system need to change it.

## 14. Thanks for Watching

That's Actor. If you take one sentence away, take this one: an actor takes locks out of the story by giving state one owner, and the price is messages, and a restart that forgets. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, make the actor keep its stock across a restart, and decide where to keep it. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
