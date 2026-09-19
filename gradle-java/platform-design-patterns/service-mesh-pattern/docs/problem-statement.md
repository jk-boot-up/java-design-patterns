# Problem Statement

## The scenario

The checkout, refunds and reports services all call the payment service. The payment service is having a bad day and refuses its first two calls.

## The naive version

Let each service carry its own retry code, and its own way of counting and checking.

```
  the payment service refuses its first 2 calls. checkout retries 3 times: true. refunds never retries: false. reports retries once: false.
  three services, three copies of the retry code, three different behaviours.
```

## What this project must deliver

A flaky payment service; three library clients with different retry counts; a mesh of proxies with one retry policy; the policy changed in one place; a rule about who may call the payment service; counts per caller and callee; and the costs of multiplied load, extra ticks and extra processes.
