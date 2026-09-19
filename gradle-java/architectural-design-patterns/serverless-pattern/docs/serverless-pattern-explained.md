# Serverless, Explained

## The pattern in one sentence

Serverless runs each piece of work as a short function that a platform starts when an event arrives and throws away when it is idle, and you pay per call.

## The six acts

### A Machine That Is Always On

One hundred ticks, three orders. The bill is two hundred. It was paid for a hundred ticks, and used for three orders.

```
  100 ticks, 3 orders. the bill: 200. paid for 100 ticks, used for 3 orders.
```

### A Function Per Event

The same three orders, each running a send receipt function. Three calls, and a bill of three. Between orders nothing runs, and nothing is paid for.

```
  the same 3 orders, each one runs a send-receipt function. invocations: 3. the bill at 1 per invocation: 3.
  between orders nothing runs, and nothing is paid for.
```

### Scale Out, And Back To Zero

Before any order, no instances. Five orders at the same moment: five instances, five cold starts. Ten ticks later, with no orders: no instances again.

```
  before any order, instances: 0.
  5 orders at the same moment: instances 5, cold starts 5.
  10 ticks later, with no orders: instances 0.
```

### The Cold Start

The extra wait: first call, five ticks. A call soon after, none. A call after a long quiet, five ticks. The first call after a quiet time is slow, because an instance must be started for it.

```
  extra wait: first call 5 ticks, a call soon after 0, a call after a long quiet 5.
  the first call after a quiet time is slow, because an instance must be started for it.
```

### No Memory Between Calls

Two calls in a row: the instance remembers two, and the outside store two. After the quiet time: the instance remembers one, and the outside store three. What is kept in the function is gone. Anything that must last goes in a store outside.

```
  two calls in a row: the instance remembers 2, the outside store 2.
  after the quiet time: the instance remembers 1, the outside store 3.
  what is kept in the function is gone. anything that must last goes in a store outside.
```

### The Bill

In a hundred ticks, with three calls, functions cost three and the server two hundred. With three hundred calls, functions cost three hundred, and the server two hundred. Paying per call is cheap when quiet, and dear when busy all the time. And a job of twenty ticks against a limit of fifteen does not finish. Long work does not fit.

```
  100 ticks. quiet, 3 calls: functions 3, server 200. busy, 300 calls: functions 300, server 200.
  paying per call is cheap when quiet and dear when busy all the time.
  and a job of 20 ticks against a limit of 15: finished false. long work does not fit.
```

## The verdict

Use serverless for work that is short, comes in bursts, and keeps nothing between calls. Keep state outside. Expect a slow first call after a quiet time. Work out the price at your busiest, not your quietest. Keep long jobs off it.

## How to recognise this in code you did not write

- AWS Lambda, Google Cloud Functions, Azure Functions, Cloudflare Workers.
- A handler that takes an event and returns, with no fields.
- A trigger: an upload, a queue message, a schedule, an HTTP request.
- A setting for timeout and memory, and a bill per request.

## Where you have already met this

Image resizing on upload, sending receipts, webhooks, scheduled clean-ups, and small APIs behind a gateway.

## When this is too much

For steady heavy load, long jobs, or work that needs memory between calls, an ordinary server is cheaper and simpler. Serverless suits the quiet and the bursty.
