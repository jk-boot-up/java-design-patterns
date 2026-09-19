# Problem Statement

## The scenario

Orders wait in a queue to be processed. One worker cannot keep up, and adding a second must not mean rewriting anything, or handling an order twice.

## The naive version

One consumer. It is correct, and it is only as fast as one worker.

```
  six slow jobs, one consumer: 1 in progress, 5 waiting.
  six slow jobs, three consumers: 3 in progress, 3 waiting.
  the consumers do not talk to each other. they take from the same queue.
```

## What this project must deliver

A broker that hands each message to one consumer at a time and takes it back when a consumer fails; a pool of consumers that do not know about each other; exactly-once handling of a thousand messages; lost ordering shown with a held message; a failed message taken over; the duplicate that at-least-once delivery causes and the consumer that remembers; a shared downstream that caps useful work; and a plain verdict.
