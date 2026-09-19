# Problem Statement

## The scenario

The payment gateway connection takes 200 milliseconds to establish. A checkout
makes payments.

## The naive version: a new connection per payment

```
ONE. A new connection for every payment.
  10 payments: 10 connections opened, 2075ms.
  every payment paid a 200ms handshake. simple, correct, and slow.
```

## The pattern: a pool

Open a few connections once, then lend them out.

```
TWO. A pool of two connections, borrowed and returned.
  10 payments: 2 connections opened, 412ms, including opening the pool.
```

## What this project must deliver

The pattern working, and then the four costs, stated up front because here the
bill is larger than the benefit in most cases.
