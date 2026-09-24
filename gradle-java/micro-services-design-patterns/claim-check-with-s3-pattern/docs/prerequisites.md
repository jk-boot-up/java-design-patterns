# Prerequisites

## Required

- A container runtime, running before you start: Docker Desktop, or anything Docker-compatible, version 24 or later. The demo starts one LocalStack container and removes it again. Without a runtime the demo prints two sentences saying what to do, and stops; the tests that need LocalStack are skipped and the rest still run.
- The idea of a claim check. The plain-Java Claim Check project in this course teaches it with nothing installed. This project explains the pattern again in its own documents, so you can start here, but it spends its time on what the real services add.

## Explicitly not required

- No Amazon Web Services account, and no AWS credentials. LocalStack answers on your own machine and accepts the dummy credentials the demo gives it.
- No prior S3 or SQS. Every word they introduce — bucket, object, key, message, versioning, delete marker, lifecycle rule, retention — is said in plain language before the name for it is used.
- No LocalStack account or token. That is why the image is held at 4.14.0; see below.

## What you will need

Java 21. Gradle comes with the wrapper in this directory. The first run downloads the libraries and pulls the LocalStack image; after that it works with no network.

## Versions this project pins

| Tool | Version |
| --- | --- |
| LocalStack image | `localstack/localstack:4.14.0` (held back) |
| AWS SDK for Java v2 (`software.amazon.awssdk:bom`, `s3`, `sqs`) | 2.55.3 |
| `org.testcontainers:testcontainers-localstack` | 2.0.5 |
| `org.slf4j:slf4j-simple` | 2.0.17 |
| JUnit | 5.10.2 |
| Java | 21 |
| Gradle | 9.2.1 |

Each is the newest generally available release at the time the project was built, with one exception. **LocalStack is held at 4.14.0 because later images refuse to start without a LocalStack account token.** 4.14.0 is the last image that runs with no account, and it answers with the current SQS limit of 1048576 bytes.
