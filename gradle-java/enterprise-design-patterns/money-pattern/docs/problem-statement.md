# Problem Statement

## The scenario

The online store adds baskets, charges VAT, spreads discounts across lines and
sells in three currencies. Prices were kept as `double`s, and a report showed
one thousand 10p stickers as £99.99.

## The naive version

`NaiveCart` stores each price as a `double` and adds them up. It is short and
reads naturally, and small tests pass. It is wrong in three ways: binary
doubles cannot hold most decimal prices exactly, a double has no currency, and
it rounds silently wherever the arithmetic lands.

## What this project must deliver

- The double failures shown with exact printed values: 0.30000000000000004, 99.9999999999986 and 9999 pence.
- A `Money` class holding whole minor units and a currency, adding, multiplying and comparing exactly.
- Mixing currencies refused; amounts with too many digits refused.
- Rounding only when asked, with the per-line versus once-on-the-total difference shown.
- `allocate` splitting by ratio with shares that always add back to the whole, checked over a range.
- Every printed number asserted by a test.
