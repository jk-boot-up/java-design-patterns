# Dependencies

This project uses LocalStack, the AWS SDK for Java and Testcontainers, which the hand-built project does not. This page says what they are, why they are here, and what they cost.

**Skipping this project loses none of the pattern.** The plain-Java Queue-Based Load Leveling project in this course teaches all of it with nothing installed.

## What SQS is

Think of a coat check at a theatre, with a twist. You hand in your coat and it goes on a rail. An attendant takes a coat off the rail to fetch it for someone. But this cloakroom is careful: when an attendant lifts a coat, it is not gone from the rail. It is only covered with a cloth for a few minutes, so no other attendant touches it. If the attendant comes back and says "done", the coat is removed for good. If the attendant never comes back, the cloth comes off by itself when the minutes are up, and the next attendant can take it.

**Amazon SQS**, the Simple Queue Service, is that rail. A **queue** is one rail. A **message** is one piece of text on it; here, an order id. An order nobody has taken is **waiting**. An order an attendant has taken but not finished is **in flight**: covered, not removed. The ticket that proves which attendant took it, needed to remove it, is its **receipt**. The minutes the cloth stays on are the **visibility timeout**, 30 seconds unless you set it. An attendant who needs longer can ask for more minutes before the time is up, which SQS calls **changing the message's visibility**. Asking "is there anything for me?" and letting SQS hold the question open for a few seconds, rather than answering "no" straight away, is **long polling**. And an order nobody ever takes is thrown away after the **retention period**, 345600 seconds, 4 days, unless you set it.

SQS hands out at most 10 messages to one request, and takes at most 10 in one send.

## What LocalStack is

A program that answers the same web requests Amazon's services answer, with the same limits and the same error messages, on your own machine. The demo's code is ordinary AWS code; pointed at Amazon instead, it would run unchanged.

**It is held at 4.14.0.** From the 2026 releases onward the LocalStack image refuses to start without a LocalStack account token. 4.14.0 is the last one that runs with no account, and this project pins it rather than ask a learner to sign up for anything.

**Where LocalStack is kinder than Amazon.** An ordinary SQS queue on Amazon promises only a rough first-in, first-out order and may hand out fewer than 10 messages to a request even when more are waiting. LocalStack keeps the exact order and always hands out the full 10. The demo's depth readings rely on that, and the tests assert only what Amazon itself promises: at most 10 a request, and every order packed.

## What Testcontainers is

A Java library that starts a container from inside your program and stops it again. It is here so that the demo owns LocalStack's lifetime: `./gradlew run` brings it up on a free port, uses it, and takes it away at the end. Testcontainers also runs a small helper container that removes anything left behind if the demo is killed part way through; it exits on its own a few seconds after the demo does.

## Why this project uses them

Because the three things this project teaches — an order that is taken but not removed, a clock that hands it out again, and a queue that outlives every process reading it — only exist in a real queue service. A simulation has whatever states and whatever clock its author wrote.

## What to install

Only a JDK, version 21, and a container runtime. Gradle downloads the rest:

| Tool | Version |
| --- | --- |
| Docker, or a Docker-compatible runtime | running; 24 or later |
| LocalStack image | `localstack/localstack:4.14.0` (held back, see above) |
| AWS SDK for Java v2 | 2.55.4 (`sqs` module, through the BOM) |
| `org.testcontainers:testcontainers-localstack` | 2.0.5 |
| `org.slf4j:slf4j-simple` | 2.0.17 |

In the Testcontainers 2 line every module's name starts with `testcontainers-`, and the LocalStack container class lives in `org.testcontainers.localstack`.

## What it costs

The first run pulls the LocalStack image, about 1.15 GB once unpacked. After that a run takes about twenty seconds, a few of them LocalStack starting and several of them the demo waiting, on purpose, for SQS's timeouts to run out.

## Where this pattern lives in a real system

In the producer's send, batched 10 at a time; in the queue's visibility timeout, set longer than the slowest piece of work; in the consumer's delete after the work and its "still working" call during long work; in a check that makes handling an order twice harmless; and in an alarm or an autoscaler that watches the queue's depth, because SQS itself will never refuse the backlog.
