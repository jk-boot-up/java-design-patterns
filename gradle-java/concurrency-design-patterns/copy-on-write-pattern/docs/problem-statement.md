# Problem Statement

## The scenario

Price changes are sent to a list of listeners; the list is read constantly
and changed rarely, sometimes by a listener while it is being notified.

## The naive version

A plain `ArrayList` of listeners throws `ConcurrentModificationException`
when a listener subscribes another during a notification, and the rest never
hear.

## What this project must deliver

- The ArrayList failure shown mid-notification.
- A hand-written copy-on-write list that survives it.
- Concurrent readers and writers with no failures and no reader locks.
- A reader's snapshot shown.
- The copying cost counted.
- Every printed result asserted by a test.
