# Problem Statement

## The scenario

Gold customers get 10% off, a coupon gives £5 off baskets over £40, and the
two do not add up.

## The naive version

The web checkout and the phone app each hold a copy of the rule. The app's
older copy adds both discounts, charging £49.00 where the web charges £54.00.

## What this project must deliver

- The two copies shown disagreeing.
- A stateless PricingService used by both.
- A price explained in the shop's words.
- Five cases priced by one service object.
- The subtotal kept on the basket, where it belongs.
- Every printed result asserted by a test.
