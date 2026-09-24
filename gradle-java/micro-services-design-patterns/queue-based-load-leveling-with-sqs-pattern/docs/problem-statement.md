# Problem Statement

## The scenario

The shop runs a sale, and in its first second 100 orders arrive at once. Checkout takes the order and the payment. A separate program, the packing service, picks the items and packs the parcel. The packing service has a fixed pace: 10 orders a round, however many are waiting. Most of the day that is plenty. In the first second of a sale it is a tenth of what is needed.

## The naive version

Checkout calls the packing service directly, for every order, and waits for the answer. The packing service can take 10; the other 90 customers are told to try again, at the busiest moment the shop has. The plain-Java Queue-Based Load Leveling project in this course prints exactly that: processed 10, refused 90.

## What the partner project already did

That project taught the whole pattern with nothing installed: put a queue between the burst and the worker, let the worker keep its pace, and accept that the price is waiting. It showed a burst of 100 spread over 10 rounds, a queue that grows for ever when fed faster than it is drained, a queue with a limit that refuses the rest, and, in its last act, an in-memory queue that loses 70 orders when its process stops. It is a complete teaching of the idea and nothing here replaces it.

It had one comfort, though. An order in its queue was either waiting or done; there was no third state. Its worker could never be too slow for its own queue, because the queue had no clock. And the queue lived in memory, so the only answer to "what if the process stops?" was "the orders are gone".

## What this project must deliver

The same sale and the same packing service, with the queue on Amazon SQS, played by LocalStack in one container the demo starts and stops. The burst's depth read from SQS itself, and the ceiling of 10 per request that SQS sets and states in its own words. An order that is taken but not deleted, hidden and then handed out again when its time runs out. A slow packer that gets an order packed twice, and the "still working" call that prevents it. A packer whose process stops half way through a round, with nothing lost. A queue that cannot be given a limit, and a backlog nobody refuses. And the bill, counted as requests SQS actually received.

Every figure printed is SQS's own, and two runs back to back print the same thing.
