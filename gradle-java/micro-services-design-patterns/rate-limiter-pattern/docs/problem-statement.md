# Problem Statement

## The scenario

The product search can serve a hundred requests a second. One client, perhaps a script, sends a thousand in a second, and everyone else waits behind them.

## The naive version

No limit. Every request is accepted until the service falls over.

```
  the product search can serve 100 requests a second. a client sends 1000 in one second.
  accepted: 1000. beyond what it can serve: 900, and every other customer waits behind them.
```

## What this project must deliver

A token bucket on a clock the demo controls; a burst allowed and then refused; a steady rate that always passes; a bucket per caller against one shared bucket; a refusal that says when to retry, exact to the millisecond; the three bills of per-server limits, memory per caller, and a page that looks like a script; and a plain verdict.
