# Problem Statement

## The scenario

Auditors need a masked copy of every payment message, without changes to
checkout or the payment service.

## The naive version

Logging typed into the payment service missed the refund path and wrote full
card numbers.

## What this project must deliver

- A wire tap copying every payment.
- The shared-object trap, shown.
- `onPrepare()` giving the tap its own copy.
- A stopped audit not affecting payments.
- A slow audit lagging instead of slowing payments.
- Every printed result asserted by a test.
