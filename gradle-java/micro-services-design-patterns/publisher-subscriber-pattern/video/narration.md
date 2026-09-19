# Publisher-Subscriber Pattern — Video Narration Script

## 1. Publisher-Subscriber

Hello, and welcome. This video explains the Publisher-Subscriber pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: publisher subscriber lets a service announce an event once, to a topic, and lets any number of other services listen, without the publisher knowing who they are. This is another project in the microservices category, whose subject is how many small services stay reliable when they talk to each other. In our online store, one thing happens, an order is placed, and several services care. By the end you will see an order service that calls three others by name, see it publish once instead, see subscribers go at their own pace and take only what they want, see a late subscriber miss history unless the log is kept, and see the bill, which is that the publisher never knows who got the event.

## 2. The Scenario

Here is the scenario. When an order is placed in the online store, inventory must reserve stock, email must send a confirmation, and analytics must count it. Next month, loyalty points want to know as well. The question: who calls whom?

## 3. The Order Service Calls Each One

First, the order service calls each one. Inventory, email, analytics. It works. But the order service knows three other services by name, and when loyalty points want to know, someone must edit the order service.

## 4. The Pattern

The pattern. The publisher appends an event to a topic. Subscribers read the topic, each at its own position and its own pace. And the publisher does not know who is listening.

## 5. The Order Service Only Publishes

Second, the order service only publishes. It publishes the event once. Inventory, email and analytics each get it. Then a fourth subscriber, loyalty points, is added, and gets it too. The order service was not changed.

## 6. Each At Its Own Pace

Third, each at its own pace. Five orders are published. Email handles all five. Analytics handles one, and has a backlog of four. Later, analytics catches up. A slow subscriber held up neither the fast one, nor the publisher.

## 7. Each Takes What It Wants

Fourth, each takes what it wants. Email asks only for placed orders, and gets one. Analytics asks for everything, and gets a placed and a cancelled event. Each subscriber says what it wants. The publisher publishes one stream.

## 8. A Subscriber That Arrives Late

Fifth, a subscriber that arrives late. Three orders were published before loyalty was added, and one after. A subscriber that joins live sees only the last one. One that reads from the start sees all four, because the log was kept. Keeping the log is what makes a late subscriber possible, and it has to be kept somewhere.

## 9. The Bill: Nobody Knows Who Got It

Last, the bill. Email is down when the order is placed, and the publisher is told nothing. When email comes back, it catches up, because its place in the log was kept. But the publisher still cannot ask whether the email went out. It published, and it does not know who listened.

## 10. How To Recognise It

How do you recognise this in code you did not write? A publish call with a topic name and no reference to any consumer. Kafka topics and consumer groups, SNS topics, Google Pub/Sub, RabbitMQ fanout exchanges. ApplicationEventPublisher and @EventListener in Spring, inside one process. A subscription with a filter or a routing key.

## 11. The Verdict

Here is my verdict, plainly. Use publish and subscribe when one thing happens and several independent parties care, and when new parties will come along. Keep the events small and named for what happened. Keep the log long enough for a late or absent subscriber. Make every subscriber safe to run twice. Do not use it when the publisher needs an answer.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? If one known service needs the result, a direct call is clearer. A topic is for facts that many may want, and that you do not want to track.

## 14. Thanks for Watching

That's Publisher-Subscriber. If you take one sentence away, take this one: publish-subscribe lets a service say what happened without knowing who cares, and the price is that it never learns who acted. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add a subscriber that only wants cancelled orders, and see whether the publisher changes. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
