# Problem Statement

## The scenario

The store posts parcels, letters and gift cards, each a different class with
nothing in common except that it can be posted.

## The naive version

`CopiedPostage` keeps one copy of the sum per kind of item. A price change
reached one copy and missed two, so letters and gift cards were charged £2.50
instead of £2.80.

## What this project must deliver

- The drifted copies shown: £6.00, £2.50, £2.50.
- A `Shippable` interface with only what shipping needs.
- A stateless `ShippingServant` that prices and labels any Shippable.
- A new item type shipped with no new shipping code.
- The servant tested with a made-up item.
- Every printed result asserted by a test.
