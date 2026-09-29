# Problem Statement

## The scenario

Every order is published to an orders channel read by several services, each
interested in only some of the orders.

## The naive version

Every service is handed every order and checks each one itself: the gift-wrap
service opened ten orders to wrap two.

## What this project must deliver

- Wasted deliveries counted without a filter.
- A filter passing only gift orders.
- Chained filters for the loyalty service.
- A rule changed without touching sender or receiver.
- Drops counted, and the risk of silent loss shown.
- Every printed result asserted by a test.
