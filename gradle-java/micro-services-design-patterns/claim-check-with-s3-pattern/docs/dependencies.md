# Dependencies

This project uses LocalStack, the AWS SDK for Java and Testcontainers, which the hand-built project does not. This page says what they are, why they are here, and what they cost.

**Skipping this project loses none of the pattern.** The plain-Java Claim Check project in this course teaches all of it with nothing installed.

## What S3 and SQS are

Think of the left-luggage office at a railway station. You leave a heavy suitcase at the counter, carry a small paper ticket, and later the ticket gets your suitcase back.

**Amazon S3**, the Simple Storage Service, is the left-luggage office: it stores files of any size. A named storage room in it is a **bucket**. One stored file is an **object**. The name the object is stored under, which you need to fetch it back, is its **key**. A bucket can be told to keep every version of every object rather than replace it, which S3 calls **versioning**; in such a bucket a delete by key only adds a note saying the key is deleted, a **delete marker**, and every version stays stored. A rule that removes objects a number of whole days after they were stored is a **lifecycle rule**.

**Amazon SQS**, the Simple Queue Service, is a waiting line for messages. One program puts a **message**, a piece of text, on a **queue**; another takes it off later and deletes it once it has handled it. SQS limits how long a message may be, and keeps a message nobody has taken for a set time, its **retention period**.

## What LocalStack is

A program that answers the same web requests Amazon's services answer, with the same limits and the same error messages, on your own machine. The demo's code is ordinary AWS code; pointed at Amazon instead, it would run unchanged.

**It is held at 4.14.0.** From the 2026 releases onward the LocalStack image refuses to start without a LocalStack account token. 4.14.0 is the last one that runs with no account, and this project pins it rather than ask a learner to sign up for anything.

## What Testcontainers is

A Java library that starts a container from inside your program and stops it again. It is here so that the demo owns LocalStack's lifetime: `./gradlew run` brings it up on a free port, uses it, and takes it away at the end. Testcontainers also runs a small helper container that removes anything left behind if the demo is killed part way through; it exits on its own a few seconds after the demo does.

## Why this project uses them

Because the three things this project teaches — a limit that is the service's and counts text rather than bytes, a key that can be stored twice, and a delete that keeps every byte — only exist in the real services. A simulation has whatever limit and whatever delete its author wrote.

## What to install

Only a JDK, version 21, and a container runtime. Gradle downloads the rest:

| Tool | Version |
| --- | --- |
| Docker, or a Docker-compatible runtime | running; 24 or later |
| LocalStack image | `localstack/localstack:4.14.0` (held back, see above) |
| AWS SDK for Java v2 | 2.55.3 (`s3` and `sqs` modules, through the BOM) |
| `org.testcontainers:testcontainers-localstack` | 2.0.5 |
| `org.slf4j:slf4j-simple` | 2.0.17 |

In the Testcontainers 2 line every module's name starts with `testcontainers-`, and the LocalStack container class lives in `org.testcontainers.localstack`.

## What it costs

The first run pulls the LocalStack image, about 1.15 GB once unpacked. After that a run takes about twenty seconds, a few of them LocalStack starting.

## Where this pattern lives in a real system

In the sender's upload-then-send code, often provided by a library such as Amazon's SQS Extended Client; in the bucket's versioning and lifecycle settings, usually set up with the rest of the infrastructure; in the queue's retention period; and in the receiver's check of the checksum before it trusts what it fetched.
