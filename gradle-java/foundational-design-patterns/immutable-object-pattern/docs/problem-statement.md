# Problem Statement

## The scenario

Orders keep shipping addresses, checkout reads a shared price list, and a set
records addresses with failed deliveries. All are ordinary objects with
setters, passed around by reference.

## The naive version

`MutableAddress` and `MutablePriceList` can be changed by anyone holding them.
An order's address moves when the profile changes, a sale is seen half-applied,
and a tidied address vanishes from a hash set.

## What this project must deliver

- The three failures shown: a placed order's address changing, a £62.00 basket mid-sale, and a set that cannot find its only member.
- An immutable `Address` record with `with` methods.
- An immutable `PriceList` that copies its input, hands out a read-only view, and is replaced whole.
- The cost shown: 1000 entries copied to change one price.
- Every printed number asserted by a test.
