# Dependencies

This project uses gRPC, which the plain Java version of Hedged Requests does
not. Skipping it loses none of the pattern: the plain version teaches all of
it with nothing installed.

## What gRPC is

gRPC is a framework for calling methods on another server. A channel is the client's connection. A method descriptor names a method and says how to turn requests and replies into bytes; here a simple text marshaller, instead of the usual Protocol Buffers. A service config is a set of policies for a channel; its hedgingPolicy gives the maximum attempts and the delay before each extra attempt, and applies only to the services or methods it names. enableRetry turns on this retry and hedging support. When an attempt loses, gRPC cancels it, and the server can check Context.current().isCancelled().

## Why this project uses them

The plain version shows the idea with futures. This version shows hedging as
the framework feature most teams actually use: a policy, not code.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the version is pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| gRPC Java (netty-shaded, stub) | 1.84.0 |

## What it costs

- A policy that must be scoped to safe methods.
- Extra server load, to be capped with throttling.
