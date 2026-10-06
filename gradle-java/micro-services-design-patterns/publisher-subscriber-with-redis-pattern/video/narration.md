# Publisher-Subscriber with Redis Pattern — Video Narration Script

## 1. Publisher-Subscriber with Redis

Hello, and welcome. This video explains the Publisher-Subscriber pattern in Java, using a real server called Redis. This video is presented by Jayasekhar Konduru. First, a simple definition. One part of a system announces that something happened, once, to a named place. Any number of other parts can listen at that place. And the one announcing never learns who they are. In our online store, when an order is placed, the order service announces it once. Inventory, email, analytics, and loyalty points each hear it, and do their own work. The order service does not need to know any of them by name. By the end, you will hear Redis pass one order to a program running separately. Tell the publisher how many heard it. Keep nothing for a listener that arrives late. And cut off a listener that falls too far behind.

## 2. The Scenario

Here is the scenario. An order is placed, and several services care about it. Inventory reserves the stock. Email sends the confirmation. Analytics counts the sale. Loyalty adds points. The plain Java version built this with the topic as an object inside one Java program. This time, the topic lives in Redis, a separate program. And every listener reaches it over its own network connection. That changes more than you might expect.

## 3. The Order Service Calls Each One

First demo: without the pattern. The order service calls inventory, then email, then analytics, each by name. Each one handles order one. It works. But the order service now knows three services by name. When loyalty points wants to hear about orders, someone must edit the order service.

## 4. Redis's Words

Redis brings a few words with it. Each is simpler than it sounds. Think of a live radio station. The presenter speaks once, and every radio tuned in at that moment hears it. Announcing a message once is what Redis calls publishing. The frequency it goes out on is called a channel. It is just a name. Here, the name is orders dot placed. And tuning in, to hear everything on that name from now on, is called subscribing. One more thing about live radio. If your radio was off, there is no recording. Redis works the same way, and that will matter later.

## 5. Publish Once, Redis Fans It Out

Second demo: publish once, and Redis passes it on. The demo starts Redis in a container, a small sealed box it switches on and off by itself. Inventory, email, and analytics each connect, and subscribe. The order service publishes order one, once. Redis answers with a number: three receivers. And each of the three services gets order one. Now loyalty points joins. And it is not even in the same program. The demo starts it as a second Java program, with its own memory. Order two is published, and Redis answers: four receivers. The loyalty program receives order two. And the order service was not changed at all.

## 6. The Publisher Gets A Number

Here is the whole of the publishing side. The order service hands one message to Redis, under a channel name. And Redis answers with one number. How many listeners it handed the message to, at that moment. That number is new. In the plain Java version, the publisher was told nothing. Here, it learns how many heard. But it still does not learn who they were. Or whether any of them finished the work.

## 7. A Subscriber That Arrives Late

Third demo: a subscriber that arrives late. Only email is listening. Three orders are published. Redis answers: one receiver each time. Then loyalty starts listening. And order four is published, to two receivers. Email saw all four orders. Loyalty saw only order four. In the plain Java version, a late subscriber could read from the start, because the topic kept a history. Redis keeps no history here. It stored none of the four orders. Orders one, two, and three were never coming.

## 8. Each Takes What It Wants

Fourth demo: each service takes only what it wants. Email subscribes to one exact name: orders dot placed. Analytics subscribes with a star in the name: orders dot star. That matches every name starting with orders. Redis calls that a pattern subscription. Order one is placed, and reaches two receivers. Then order one is cancelled, and that reaches only one. Email got the placed order. Analytics got both.

## 9. A Pile For Every Listener

Before the fifth demo, one more idea. Picture a busy kitchen sending plates to several tables. The kitchen never waits for a slow table. Plates a table has not taken yet stack up on a shelf by the door. One shelf per table. Redis does exactly this. Messages a listener has not read yet wait in a pile that Redis keeps for that one listener. Redis calls it the output buffer. And the pile has a limit. By default, thirty-two megabytes. Past that limit, Redis does not slow down, and it does not wait. It closes that listener's connection.

## 10. A Subscriber That Cannot Keep Up

Fifth demo, and this is the headline of the video. The demo lowers the limit to one megabyte, so the effect shows up in seconds. Email and analytics are both listening. Then analytics stops reading, just as a stuck service would. The order service publishes orders in rounds of a thousand, like a flash sale. More than ten thousand orders later, Redis cuts analytics off. The first order reached two receivers. The last reached only one. Email kept up, and received every order. When analytics starts reading again, it gets some of the orders, not all. Then its connection ends. The rest were thrown away with the pile. The exact counts depend on the machine, so the demo describes them instead of printing them.

## 11. Why Redis Cuts It Off

Why would Redis do that? Because the other two choices are worse. It could wait for the slow listener. Then one stuck service would slow down every publisher in the shop. Or it could keep piling up messages, until Redis itself runs out of memory. Then everyone loses. So it cuts off the one listener that fell behind. And it keeps everyone else going. Notice who is not told. The publisher was never slowed down, and never warned. The only trace is a counter inside Redis. And a smaller number in the answer to the next publish.

## 12. The Bill

Sixth demo: the bill. Email is down when order one is placed. Redis tells the order service: zero receivers. When email comes back, it gets nothing. There is nothing to catch up from. At least the publisher can see the zero. But the count only says how many were listening. Not which ones. And not whether any of them finished the work. And Redis is one more program to run and watch.

## 13. What The Simulation Left Out

The plain Java version got the shape right. The publisher announces once, and names nobody. A new subscriber joins without the publisher changing. And each subscriber picks what it hears. All of that is true on Redis. But it left out three things. First, a listener in a different program, because everything lived in one program. Second, the history. The plain version kept a history, so a late or slow subscriber could catch up. Redis keeps none. And third, a limit. The plain version let a slow subscriber fall behind forever. Redis cuts it off.

## 14. The Verdict

So, here is the verdict. Redis publishing is for news that is worthless if it arrives late. A live price. A stock level refresh. Or a signal to clear a cache. One. Subscribe before you need it, because nothing is kept for a latecomer. Two. Keep every listener reading. Hand slow work to a separate queue. And watch the counter of listeners that were cut off. Three. If a missed order would matter, use a tool that keeps a history. Not live radio.

## 15. What Is Real, And When Not

A quick, honest note about this demo. The server is Redis, version eight point ten point two, the newest release. It runs in a container that the demo starts and stops by itself. The Java client is called Jedis. You just need Docker switched on first. Every number you heard comes from the program's own output. So, when is this the wrong tool? If every listener lives in one program, a topic in memory costs nothing to run. And if a lost order matters, Redis publishing is too little, because it keeps nothing.

## 16. Thanks for Watching

That's Publisher-Subscriber, with Redis. If you remember one sentence, make it this one. Redis hands each message to whoever is listening at that moment, tells the publisher how many that was, keeps nothing, and cuts off a listener that falls too far behind. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Raise the limit in the fifth demo to eight megabytes. Guess whether analytics is still cut off, and then run it. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
