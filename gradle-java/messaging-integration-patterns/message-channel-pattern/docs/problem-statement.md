# Problem Statement

## The scenario

When an order is placed, checkout must tell the warehouse to pick it. The warehouse system is taken down for maintenance every so often.

## The naive version

Checkout calls the warehouse system directly. If it is down, the call fails, and so does the checkout.

```
  the warehouse system is down for maintenance. orders placed: 3. checkouts that failed: 3.
  the shop cannot sell while another system is away, though selling does not need it to answer yet.
```

## What this project must deliver

A channel with a type and a limit; an envelope of headers and a body; messages that wait while the receiver is down and arrive in order; a channel that refuses the wrong type; a full channel that refuses honestly; the loss of the sender's answer; and a plain verdict.
