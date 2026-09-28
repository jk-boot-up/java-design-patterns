# Actor Pattern — Video Narration Script

## 1. Actor

Hello, and welcome. This video explains the Actor pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. An actor is an object that owns some data, has a mailbox, and handles one message at a time, on its own thread. Its data is never touched by two threads at once. And nobody can reach inside it, except by sending it a message. Think of a bank teller behind a window. Customers queue, and pass notes through the window. Only the teller ever touches the cash drawer. In our online store, many threads want to change the stock of a product. In this video, shared stock will lose an update. Then one actor will own it, and lose nothing. We will hear answers come back as messages, and a bad message restart the actor. And finally, the costs.

## 2. The Scenario

Here is the scenario. Many threads place orders in an online store. Every order reserves some stock. The stock count must never go wrong, however many orders arrive at the same moment. So here is the question. Do we protect it with locks, or with something else?

## 3. State That Many Threads Can Reach

First demo: data that many threads can reach. There are ten in stock. Two orders arrive, for three and for four. Both read the stock at the same moment. There should be three left. But there are not. One of the two reservations was lost. Every method looked correct. The problem was that the data was open to anyone.

## 4. The Pattern

Now, the pattern. An actor owns some data. It has a mailbox, and one thread, which takes one message at a time. Nobody else can touch the data. Everyone else sends messages. And if they want an answer, they get a reply message back.

## 5. State That One Actor Owns

Second demo: data that one actor owns. An inventory actor starts with four thousand in stock. Four threads each send one thousand reservations. Stock left: zero, exactly right. There is no lock inside the inventory. The actor handled one message at a time, so nothing was lost.

## 6. Ask, And Be Answered By A Message

Third demo: ask, and get a message back. There are five in stock. Reserve three, and the reply says: reserved. Reserve three more, and the reply says: out of stock, only two left. The answer is a message too. And it can be a refusal. No exception crosses between the two sides.

## 7. Nobody Can Reach In

Fourth demo: nobody can reach inside. The inventory actor has no public method that returns its stock. The only way to learn the stock is to ask. And the answer is a copy. Nobody holds the real value. So nobody can change it behind the actor's back.

## 8. Let It Crash

Fifth demo: let it crash. After reserving two, the stock is three. Then the actor receives a message it cannot handle. The sender is told what went wrong. The actor is restarted. And the next message is handled normally. One bad message did not stop the actor. But notice: after the restart, the stock went back to five. The restart reset its data.

## 9. The Bill

Finally, the costs. Two actors each ask the other a question, and wait for the answer. Neither ever gets one. There are no locks, and yet it is a deadlock. Each is waiting for a message the other can never send. Also, a restart forgets the actor's data, unless it was saved somewhere else. Messages are copied. Mailboxes can grow. And tracing where a message went needs special tools.

## 10. How To Recognise It

How can you spot this in code someone else wrote? Look for a class with a mailbox, a receive method, and a single thread. Look for Akka's actor references, with tell and ask. Or Erlang processes, and Elixir's Gen Server. Look for message classes that are records. And a supervisor that decides what to do when an actor fails.

## 11. The Verdict

So, here is the verdict. Use actors for data that many parts of a program need to change, where one owner and messages are clearer than locks. A stock count, a user session, or a network connection. Keep messages small, and unchangeable. Never wait for a reply inside a message handler. Decide what a restart should do to the data. And use a library such as Akka or Pekko, rather than writing mailboxes yourself.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every number you heard comes from the program's own output. And nothing depends on the clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? For a simple counter, an Atomic Integer is easier. Actors earn their place when the data is more than one number, and many parts of the system need to change it.

## 14. Thanks for Watching

That's the Actor pattern. If you remember one sentence, make it this one. An actor removes locks by giving data one owner, and the price is messages, and a restart that forgets. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Make the actor keep its stock across a restart. And decide where that stock should be kept. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
