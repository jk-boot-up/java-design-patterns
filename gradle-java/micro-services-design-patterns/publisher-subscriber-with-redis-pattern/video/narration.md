# Publisher-Subscriber with Redis Pattern — Video Narration Script

## 1. Publisher-Subscriber with Redis

Hello, and welcome. This video explains the Publisher Subscriber pattern in Java, using a real server called Redis. It is written and presented by Jayasekhar Konduru. Here is the plain definition, in general words. One part of a system announces that something happened, once, to a named place. Any number of other parts can listen at that place. The one announcing never learns who they are. Now the same thing in our online store. When an order is placed, the order service announces it once. Inventory, email, analytics and loyalty points each hear it and do their own work, and the order service does not have to know any of them by name. By the end you will have seen Redis copy one order to a program running in a different process, tell the publisher how many heard it, keep nothing for a listener that arrives late, and cut off a listener that falls too far behind.

## 2. The Scenario

Here is the scenario. An order is placed, and several services care about it. Inventory reserves the stock. Email sends the confirmation. Analytics counts the sale. Loyalty adds points. The hand-built partner project in this course already built this, with the topic as an object inside one Java program. This time the topic lives in Redis, a separate program, and every listener reaches it over a network connection of its own. That changes more than you might expect.

## 3. The Order Service Calls Each One

First, the version without the pattern. The order service calls inventory, then email, then analytics, each by name, and each one handles order one. It works. But the order service now knows three services by name. When a fourth one, loyalty points, wants to hear about orders, somebody has to edit the order service to add it.

## 4. Redis's Words

Redis brings a few words with it, and each one is simpler than it sounds. Think of a live radio station. The presenter speaks once, and every radio tuned in at that moment hears it. Announcing a message once is what Redis calls publishing. The frequency it goes out on is what Redis calls a channel. It is just a name. Here the name is orders dot placed. And tuning in, asking Redis to send you everything on that name from now on, is what Redis calls subscribing. One more thing about live radio. If your radio was off, there is no recording. Redis works the same way, and that will matter later.

## 5. Publish Once, Redis Fans It Out

Second, the pattern, on a real Redis server. The demo starts Redis in a container, a small sealed box it switches on and off itself. Inventory, email and analytics each open their own connection and subscribe. The order service publishes order one, once. Redis answers it with a number: three receivers. And each of the three services gets order one. Now loyalty points joins, and it is not even in the same program. The demo starts it as a second Java process, with its own memory. Order two is published, and Redis answers four receivers. The loyalty process prints order two, and exits cleanly. The order service was not changed at all.

## 6. The Publisher Gets A Number

Here is the whole of the publishing side. The order service hands one message to Redis under a channel name, and Redis answers with a single number: how many listeners it handed the message to, at that instant. That number is new. In the partner project the publisher was told nothing at all. Here it learns how many heard. It still does not learn who they were, or whether any of them finished the work.

## 7. A Subscriber That Arrives Late

Third, a subscriber that arrives late. Only email is listening, and three orders are published. Redis answers one, one and one. Then loyalty starts listening, and order four is published, to two receivers. Email saw all four orders. Loyalty saw only order four. In the partner project, a late subscriber could read the topic from the start, because the topic kept a log. Redis has no log for this. It stored none of the four orders. The number of keys in its database is zero. Orders one, two and three were never coming.

## 8. Each Takes What It Wants

Fourth, each service takes only what it wants. Email subscribes to one exact name, orders dot placed. Analytics subscribes with a star in the name, orders dot star, which matches every name that starts with orders. Redis calls that a pattern subscription. Order one is placed, and reaches two receivers. Then order one is cancelled, and that reaches only one. Email got the placed order. Analytics got both.

## 9. A Pile For Every Listener

Before the fifth act, one more idea. Picture a busy kitchen sending plates out to several tables. The kitchen never waits for a slow table. Plates that a table has not taken yet stack up on a shelf by the kitchen door, one shelf per table. Redis does exactly this. What a listener has not read yet waits in a pile that Redis keeps for that one listener. Redis calls the pile the output buffer. And the pile has a limit. Out of the box it is thirty two megabytes, or eight megabytes if that lasts for sixty seconds. Past the limit, Redis does not slow down, and it does not wait. It closes that listener's connection.

## 10. A Subscriber That Cannot Keep Up

Fifth, the headline of this video. The demo lowers the limit to one megabyte, so the point arrives in seconds. Email and analytics both listen. Then analytics stops reading, the way a stuck service would. The order service publishes orders in rounds of one thousand, a flash sale, until Redis acts. More than ten thousand orders later, Redis cuts analytics off. Its own counter of listeners cut off for falling behind reads one. The first order reached two receivers. The last reached one. Email kept up, and received every one. When analytics starts reading again, it gets some of the orders, not all, and then its connection ends. The rest were thrown away with the pile. The exact counts depend on the machine, so the demo describes them rather than printing them.

## 11. Why Redis Cuts It Off

Why would Redis do that? Because the other two choices are worse. It could wait for the slow listener, and then one stuck service would slow down every publisher in the shop. Or it could keep piling up messages until Redis itself runs out of memory, and then everyone loses. So it cuts off the one listener that fell behind, and keeps everyone else going. Notice who is not told. The publisher was never slowed down, and never warned. The only trace is a counter inside Redis, and a smaller number in the answer to the next publish.

## 12. The Bill

Sixth, the bill. Email is down when order one is placed. Redis tells the order service zero receivers. When email comes back, it gets nothing. There is nothing to catch up from. At least the publisher can see the zero. But the count only says how many connections were listening. It does not say which ones, and it does not say whether any of them finished the work. And Redis is a separate program to run and to watch. This demo needed one container and two Java processes.

## 13. What The Simulation Left Out

The hand-built partner project got the shape right. The publisher announces once and names nobody. A new subscriber joins without the publisher changing. Each subscriber picks what it hears. All of that is true on Redis. It left out three things. A listener in a different process, because everything lived in one program. A backlog: the partner project kept a log, so a late or slow subscriber could catch up, and Redis keeps none. And a limit: the partner project let a slow subscriber fall behind for ever, while Redis cuts it off.

## 14. The Verdict

Here is my verdict, plainly. Redis publishing is for news that is worth nothing if it arrives late: a live price, a stock level refresh, a signal to clear a cache. One. Subscribe before you need it, because nothing is kept for a latecomer. Two. Keep every listener reading. Hand slow work to a queue of its own, and watch the counter of listeners cut off. Three. If a missed order would matter, use a tool that keeps a log, not live radio.

## 15. What Is Real, And When Not

What is real here? The server is Redis, version eight point ten point two, the newest release, in a small Alpine Linux container that the demo starts at the beginning and stops at the end. The Java client is Jedis, version eight point zero point one. Nothing is installed and nothing is left running. You need a container runtime, such as Docker Desktop, switched on before you start. Every number in this video comes from the program's own output, and two runs one after the other print the same thing. So when is this the wrong tool? If every listener lives in one program, a topic in memory costs nothing to run. And if a lost order matters, Redis publishing is too little, because it keeps nothing.

## 16. Thanks for Watching

That's Publisher Subscriber with Redis. If you take one sentence away, take this one: Redis hands each message to whoever is listening at that instant, tells the publisher how many that was, keeps nothing, and cuts off a listener that falls too far behind. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, raise the limit in the fifth act to eight megabytes, guess whether analytics is still cut off, and then run it. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
