# Leader/Followers Pattern — Video Narration Script

## 1. Leader/Followers

Hello, and welcome. This video explains the Leader Followers pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A pool of threads takes turns. One thread, the leader, waits for the next message. When it gets one, it hands leadership to another thread, and then handles that message itself. Think of a taxi rank. The taxi at the front waits for a passenger. When someone gets in, it drives off, and the next taxi moves up. The car that picks you up is the car that takes you home. In this video, the domain is an online shop's order service. It receives a stream of order messages, and a pool of threads handles them. By the end, you will hear what a dispatcher costs. How leader and followers take turns. How leadership passes on. And why order is not kept.

## 2. The Scenario

Here is the scenario. The order service receives a stream of order messages. A dispatcher thread received each message. Then it passed it, through a second queue, to one of four worker threads.

## 3. Act One — A dispatcher that hands off

First demo: a dispatcher receives every message, and hands it to a worker. One dispatcher thread, and four workers. The dispatcher takes each order message, and passes it through a second queue to a worker. Twenty orders. Twenty hand-offs between threads. And the dispatcher itself handled no orders at all.

## 4. Act Two — Leader and followers

Second demo: leader and followers. Four threads, and no dispatcher. At any moment, one thread is the leader. Only the leader waits for the next message. The others are followers, waiting their turn to lead. Twenty orders are handled. And never more than one thread waits for a message at the same moment.

## 5. Act Three — Receive, promote, handle

Third demo: receive, promote a follower, then handle. The leader takes a message. At once, it passes leadership to a follower. Then it handles the message itself. Leadership passes twenty times, once per order. Every order is handled by the thread that received it. Zero hand-offs.

## 6. Act Four — Every thread works

Fourth demo: every thread in the pool does real work. The twenty orders were handled by several different pool threads. None of them sat as a pure dispatcher, only receiving and passing on.

## 7. Act Five — The bill

Fifth demo: the bill. Two messages for the same order arrive: place the order, then cancel it. The first leader takes place order, and promotes a follower. The follower takes cancel, which is quicker. Cancel finishes first. Then place. Messages that must stay in order need to go to the same thread.

## 8. The Pattern

Let's name the pattern. One thread is the leader. Only it waits for the next message. The other threads are followers. They wait to become leader. When the leader receives a message, it promotes a follower, and then handles the message itself.

## 9. Who Does What

Here is who does what. Leader followers is the pool of threads. Leadership is a lock. The thread holding it is the leader. The source is the queue of incoming messages. Record notes who received each message, and who handled it. And dispatcher workers is the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern in fast servers. It was described for high-performance C++ servers. Some event loops let several threads take turns on the same selector. And several threads calling accept on the same server socket are, in effect, taking turns as leader.

## 11. When To Use It

So, when should you use it? In very high-throughput servers, where a hand-off per message is a real cost. For most applications, a plain executor service is simpler, and fast enough. And either way, messages that must stay in order should go to the same thread.

## 12. Thanks for Watching

That's the Leader Followers pattern. If you remember one sentence, make it this one. Take turns to wait, and handle what you receive yourself. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Send messages for the same order to the same thread, so place always finishes before cancel. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
