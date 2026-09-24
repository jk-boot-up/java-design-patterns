# Problem Statement

## The scenario

The shop takes orders, and every order becomes a pick order for the warehouse. On a busy day they arrive faster than one picker can pick them, so the queue of pick orders grows. The warehouse wants to add pickers without rewriting anything: each new picker should simply start taking orders from the same queue, no order should be picked twice, and none should be lost when a picker's handheld crashes half-way down an aisle.

## The naive version

One picker. It is correct, and it is only as fast as one picker.

```
  12 orders, one picker taking one at a time. being picked: 1. waiting: 11.
  the same 12, three pickers on the same queue. being picked: 3. waiting: 9.
```

## What the plain-Java project already did

The plain-Java Competing Consumers project in this course put several consumers on one queue and showed the whole shape: each message goes to one consumer, capacity grows with the number of consumers, a failed message is given back and taken over, and at-least-once delivery means a consumer may see the same message twice. It is a complete teaching of the idea and nothing here replaces it.

It had one comfort, though. Its broker was a list inside the same Java program, and each consumer reached in and took one message when it was free. So a consumer could never be holding more than the one message it was working on, the broker always knew exactly which message had failed, and the broker always waited to be told a message was finished.

## What this project must deliver

The same shop and the same pickers, with the queue moved into a real RabbitMQ broker that the demo starts in a container and stops at the end. A slow picker that starts first with no limit set and is handed every waiting order while a fast picker stands idle. The same two pickers with a limit of ten and a limit of one, and the difference counted. A picker holding five that dies half-way through the third, and the broker handing back all three it was holding, each marked as seen before. The same crash with automatic acknowledgement, and the three orders lost. A poison order that crashes every picker and never leaves the queue. And the split across three equal pickers, which the broker decides and which changes from run to run, described honestly as a range.

Every exact figure printed is the broker's own, and two runs back to back print the same thing.
