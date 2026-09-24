# Problem Statement

## The scenario

An order is placed, and several services care about it. Inventory reserves the stock. Email sends the confirmation. Analytics counts the sale. Loyalty adds points. Next month there will be a fifth. They are run by different teams, deployed on their own schedules, and some of them are not even written in the same program as the order service. The order service should announce the order once and not have to know any of them.

## The naive version

The order service calls each interested service, by name, one after another.

```
  inventory [ORD-1], email [ORD-1], analytics [ORD-1].
  the order service knows 3 services by name. a fourth, loyalty points, means editing it.
```

## What the partner project already did

The plain-Java Publisher-Subscriber project in this course put a topic between them: the order service publishes to it, and each service subscribes. It kept a log, so a slow subscriber caught up later and a late one could read from the start. It is a complete teaching of the idea and nothing here replaces it.

It had one comfort, though. The topic was an object inside the same Java program as every subscriber. "Slow" was a subscriber that had not asked yet, and its backlog cost nothing but a list index. So it could not show a subscriber in another process, a server that keeps nothing, or a server that refuses to hold an unlimited backlog for somebody who has stopped reading.

## What this project must deliver

The same order service and the same four services, with the topic moved into a real Redis server that the demo starts in a container and stops at the end. One publish reaching three subscribers on three connections, and a fourth running as a second Java process. The number Redis hands back on every publish. A late subscriber that sees only what was published after it joined, and a database that holds no keys afterwards. Subscriptions by exact name and by a name with a star. A subscriber that stops reading during a flash sale and is cut off by Redis when its pile of unread orders passes a limit, while the one that kept reading gets every order. And an honest bill: a count that is not a list of names, nothing to catch up from, and a server to run.

Every figure printed is Redis's own, and two runs back to back print the same thing.
