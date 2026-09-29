# Reactor Pattern — Video Narration Script

## 1. Reactor

Hello, and welcome. This video explains the Reactor pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. In a reactor, one thread waits for events on many connections at once. When something happens on a connection, the thread hands that event to a short piece of code called a handler. No connection gets a thread of its own. Think of one waiter looking after a whole restaurant. They do not stand at one table while the guests read the menu. They watch the room, and go to whichever table raises a hand. In this video, the domain is an online shop's warehouse. Its stock server has a hundred shop tills connected all day, asking short questions like: how many kettles are in stock? By the end, you will hear why a thread per connection wastes threads. How a reactor serves them all with one. How handlers work. And the one rule you must never break.

## 2. The Scenario

Here is the scenario. The warehouse runs a stock server. A hundred shop tills stay connected all day. Now and then, each asks a short question. How many kettles? What does a mug cost? The server gave every connection its own thread.

## 3. Act One — A thread per connection

First demo: a thread for every connection. A hundred shop tills connect to the stock server. The server starts a thread for each one. That is a hundred threads. Almost all of them are idle, waiting for their till to ask something. Each one still holds memory. Till one asks: how many kettles are in stock? Four.

## 4. Act Two — One reactor thread

Second demo: a reactor. One thread waits on every connection at once. Java gives us a selector for this. It sleeps until some connection is ready, then says which one. A hundred tills connect. Till one asks about kettles: four. Threads running handlers: one.

## 5. Act Three — A handler per event

Third demo: each kind of event has its handler. When a new connection arrives, the accept handler registers it, so the selector will watch it. When bytes arrive, the read handler answers the line. Till two asks the price of a mug. Eight hundred pence.

## 6. Act Four — Every till, one thread

Fourth demo: every till is answered by the one thread. All hundred tills ask at the same moment. The selector reports whichever connections are ready. The one thread answers them, one after another. A hundred correct answers. Still one thread.

## 7. Act Five — The bill

Fifth demo: the bill. Till two asks for a report. Its handler takes three hundred milliseconds. Meanwhile, till three asks a quick question. It waits over two hundred milliseconds, for an answer that takes microseconds. The only thread was busy. Like the waiter who stopped to cook. So handlers must never block, and slow work goes to another thread.

## 8. The Pattern

Let's name the pattern. One thread waits on every connection at once. In Java, a selector does the waiting. When a connection is ready, the thread dispatches the event to its handler. A new connection, to the accept handler. Arriving bytes, to the read handler. And every handler must be quick.

## 9. Who Does What

Here is who does what. The selector says which connections are ready. The reactor runs the loop: wait, then dispatch. The accept handler registers new tills. The read handler answers their questions, using stock commands. And thread per connection is the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. Java's NIO selector is the reactor's building block. Netty's event loops are reactors. So are Node.js, Nginx, and Redis. And Spring WebFlux and Vert.x are built on them.

## 11. When To Use It

So, when should you use it? For servers with many connections that are mostly idle. Usually through Netty, or a framework built on it. Keep handlers short. Hand slow work to a thread pool. And for a few dozen connections, Java's virtual threads give you a thread per connection without the cost.

## 12. Thanks for Watching

That's the Reactor pattern. If you remember one sentence, make it this one. One thread watches every connection, and every handler must be quick. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Hand the slow report to a thread pool, so the other tills never wait. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
