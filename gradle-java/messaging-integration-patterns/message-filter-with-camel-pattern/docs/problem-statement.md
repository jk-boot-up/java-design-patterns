# Problem Statement

## The scenario

Checkout announces ten orders; the gift-wrap and loyalty services each want
only some of them.

## The naive version

Handing every order to every service makes each one check and ignore most
messages itself.

## What this project must deliver

- Every order multicast to every service.
- A `filter()` with a Simple expression.
- A two-condition rule in `choice()`.
- A threshold changed while routes run.
- A discard channel counting rejects.
- Every printed result asserted by a test.
