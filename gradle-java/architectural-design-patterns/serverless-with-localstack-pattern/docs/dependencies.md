# Dependencies

This project uses LocalStack and AWS Lambda, which the hand-built projects do not. This page says what it is, why it is here, and what it costs. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [Serverless](../serverless-pattern) teaches all of it with plain Java.

## What LocalStack and AWS Lambda is

AWS Lambda runs a function for each event, in an execution environment that it starts and stops. LocalStack is a local emulator of AWS services. Its Lambda service starts a Docker container per execution environment, from the same runtime images AWS publishes, and removes idle ones after a keep-alive time.

## Why this project uses it

The cold start, the separate copies and the lost memory are real containers doing real things, behind the same API calls that the real service takes.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Docker | running; 24 or later |
| LocalStack image | `localstack/localstack:4.14.0` |
| Lambda runtime image | `public.ecr.aws/lambda/python:3.12` |
| AWS SDK for Java | 2.55.1 |

LocalStack 4.14.0 is the newest release that runs without an account. From the 2026 releases onward the image needs a LocalStack auth token, so this project pins the last one that does not. The demo mounts the Docker socket so that LocalStack can start the function containers, and removes them all at the end.

## What it costs

The first run pulls about a gigabyte of images. The demo takes about half a minute. The function is written in Python, because the runtime image is small and starts quickly; only the handler is not Java.

## Where this pattern lives

In the platform's function settings: memory, timeout, concurrency limits and keep-alive, and in the event sources that trigger the function.
