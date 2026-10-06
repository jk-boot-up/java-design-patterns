# Publisher-Subscriber Pattern — Video Narration Script

## 1. Publisher-Subscriber

Hello, and welcome. This video explains the Publisher-Subscriber pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A service announces an event once, to a named channel called a topic. Any number of other services can listen. And the service that announced it does not know who they are. Think of a radio station. It broadcasts once. Anyone can tune in, and the station never knows who is listening. In our online store, one thing happens, an order is placed, and several services care about it. By the end, you will hear an order service that calls three others by name. Then the same service publishing once instead. Listeners working at their own pace, and taking only what they want. A late listener missing history, unless it is kept. And the bill.

## 2. The Scenario

Here is the scenario. When an order is placed in the online store, three things must happen. Inventory must reserve the stock. Email must send a confirmation. And analytics must count it. Next month, a loyalty points service wants to know as well. So here is the question. Who calls whom?

## 3. The Order Service Calls Each One

First demo: the order service calls each one. Inventory. Email. Analytics. It works. But the order service knows three other services by name. And when loyalty points wants to know, someone has to edit the order service.

## 4. The Pattern

Now, the pattern. The publisher adds an event to the end of a topic. The services that listen are called subscribers. Each subscriber reads the topic from its own position, at its own pace. And the publisher does not know who is listening.

## 5. The Order Service Only Publishes

Second demo: the order service only publishes. It publishes the event once. Inventory, email, and analytics each receive it. Then a fourth subscriber is added: loyalty points. It receives the event too. And the order service was not changed at all.

## 6. Each At Its Own Pace

Third demo: each at its own pace. Five orders are published. Email handles all five. Analytics handles one, and has four still waiting. Later, analytics catches up. The slow subscriber held up neither the fast one, nor the publisher.

## 7. Each Takes What It Wants

Fourth demo: each takes what it wants. Email asks only for placed orders, and gets one. Analytics asks for everything. So it gets both a placed order and a cancelled order. Each subscriber says what it wants. The publisher just publishes one stream.

## 8. A Subscriber That Arrives Late

Fifth demo: a subscriber that arrives late. Three orders were published before loyalty points was added. And one was published after. A subscriber that joins live only sees the last order. One that reads from the beginning sees all four. Because the history of events was kept. Keeping that history is what makes a late subscriber possible. And it has to be stored somewhere.

## 9. The Bill: Nobody Knows Who Got It

Finally, the bill. Email is down when an order is placed. And the publisher is told nothing. When email comes back, it catches up, because its place in the topic was kept. But the publisher still cannot ask whether the email went out. It published. And it does not know who listened.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for a publish call with a topic name, and no mention of who receives it. Look for Kafka topics, Amazon S N S topics, Google Pub Sub, or RabbitMQ fan-out exchanges. Inside one Spring program, look for an event publisher, and event listener annotations. Or a subscription with a filter.

## 11. The Verdict

So, here is the verdict. Use publish and subscribe when one thing happens, and several independent services care. Especially when new services will come along later. Keep the events small, and name them for what happened. Keep the history long enough for a late or absent subscriber. And make every subscriber safe to handle the same event twice. Do not use it when the publisher needs an answer.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every number you heard comes from the program's own output. Nothing depends on a real clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? If only one known service needs the result, a direct call is clearer. A topic is for facts that many services may want, and that you do not want to keep track of.

## 14. Thanks for Watching

That's the Publisher-Subscriber pattern. If you remember one sentence, make it this one. Publish and subscribe lets a service say what happened without knowing who cares, and the price is that it never learns who acted. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a subscriber that only wants cancelled orders. Then check whether the publisher had to change. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
