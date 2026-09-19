# Problem Statement

## Read the partner first

This project assumes [Serverless](../serverless-pattern), which counted a platform's instances on a clock: a server paid for while idle, a function per event, scale out and back to zero, a cold start, lost memory, and the price when busy. Nothing here is lost by skipping LocalStack and AWS Lambda, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: a receipt function run for each order, in bursts with long quiet gaps.

## What is new

**LocalStack**, in Docker, answering as the real AWS Lambda API does, and running each copy of the function in a real container.

```
  in the earlier project's price units, a server costs 2 a tick. 100 ticks with 3 orders: 200. paid for 100 ticks, used for 3 orders.
```

## The failure this project exists to show

A cold start is real time, not a count. What the function keeps in memory really disappears. And the platform really stops a job that runs past its limit.
