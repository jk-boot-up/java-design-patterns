# Serverless with LocalStack, Explained

## The pattern in one sentence

With Lambda, a function is uploaded once, and the platform starts a container for each concurrent call, keeps it warm for a while, and removes it when idle.

## What is new here

The pattern is [Serverless](../serverless-pattern). This page is only what LocalStack and AWS Lambda adds.

### A Machine That Is Always On

In the earlier project's price units, a server costs two a tick. A hundred ticks with three orders costs two hundred. It was paid for a hundred ticks, and used for three orders.

```
  in the earlier project's price units, a server costs 2 a tick. 100 ticks with 3 orders: 200. paid for 100 ticks, used for 3 orders.
```

### A Function Per Event

The function is uploaded to a real Lambda API, and run for each of three orders. Three receipts are sent, and the bill at one per call is three. Between orders nothing has to be running, and nothing is paid for.

```
  the function was uploaded to a real Lambda API, and run for each of 3 orders. receipts sent: 3. the bill at 1 per call: 3.
  between orders nothing has to be running, and nothing is paid for.
```

### Scale Out, And Back To Zero

Before any order, no copies are running. Five orders at the same moment: five distinct copies answered, and five containers are running. Five quiet seconds later, with no orders: none are running.

```
  before any order, copies running: 0.
  5 orders at the same moment: distinct copies that answered 5, copies running 5.
  5 quiet seconds later, with no orders: copies running 0.
```

### The Cold Start

The first call after a quiet time took several hundred milliseconds, and the call right after it, a few. The cold call was slower. The first call had to start a container for the function, and the second found it running.

```
  the first call after a quiet time took 696 ms, and the call right after it 9 ms. the cold call was slower: true.
  the first call had to start a container for the function, and the second found it running.
```

### No Memory Between Calls

A call to the copy that is running: it has handled three calls. After the quiet time, a different copy answers, and it has handled one. What the first copy kept in its variables went with it. Anything that must last goes in a store outside.

```
  a call to the copy that is running: it has handled 3 calls, in copy 490dc52e.
  after the quiet time: it has handled 1 calls. a different copy answered: true.
  what the first copy kept in its variables went with it. anything that must last goes in a store outside.
```

### The Bill

In the earlier project's price units, in a hundred ticks, with three calls, functions cost three and the server two hundred. With three hundred calls, functions cost three hundred, and the server two hundred. Paying per call is cheap when quiet, and dear when busy all the time. And a job that needs six seconds, with a limit of three, fails: the platform says the task timed out.

```
  in price units, 100 ticks. quiet, 3 calls: functions 3, server 200. busy, 300 calls: functions 300, server 200.
  paying per call is cheap when quiet and dear when busy all the time.
  a job that needs 6 seconds, with a limit of 3: failed true, and the platform said: Task timed out after 3.00 seconds.
```

## The verdict

Use functions for work that is short, bursty and keeps nothing between calls. Keep state outside. Expect a cold start after a quiet time, and set the time limit on purpose. Work out the price at your busiest, and keep long jobs off it.

## How to recognise this in code you did not write

- A handler that takes an event and a context.
- A function's `timeout` and `memorySize` settings.
- `InvokeRequest` calls in the AWS SDK.
- Containers or environments named for a function, starting and stopping.

## Where you have already met this

AWS Lambda, Google Cloud Functions and Azure Functions, and image resizing, receipts and webhooks.

## When this is too much

For steady heavy load, long jobs, or work that needs memory between calls, an ordinary server is cheaper and simpler.
