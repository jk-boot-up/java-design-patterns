# Money, Explained

## The pattern in one sentence

Money keeps a price as a whole number of the smallest coin plus its currency,
so arithmetic is exact, currencies cannot be mixed, and rounding only happens
when someone decides it should.

## The 6 acts

### 1. Prices as doubles

The naive cart keeps every price in a `double`. A 10p sticker and a 20p sticker
come to `0.30000000000000004`, which is not equal to `0.30`. A double stores
numbers in binary, and one tenth has no exact binary form, just as one third
has no exact decimal form. Adding ten pence a thousand times gives
`99.9999999999986`, and a careless conversion to pence, cutting off the
fraction, gives 9999 pence instead of 10000. Nothing crashed, and every small
test passed. And ten dollars plus ten pounds is simply `20.0`: a double has no
idea which currency it holds.

### 2. Prices as Money

`Money` stores a whole number of the smallest unit and a currency: £19.99 is
1999 and GBP. Whole numbers add and multiply exactly, so 10p plus 20p is
exactly £0.30, and a thousand ten-pences are exactly £100.00, stored as 10000
pence. A cart of three mugs at £9.49, a teapot at £24.99 and two coasters at
£4.99 comes to £63.44, with no rounding anywhere.

### 3. Currencies travel with the amount

Because each Money carries its currency, adding pounds to dollars is refused
with a clear message instead of producing a meaningless number. The currency
also knows its digits: pounds have two after the point, yen have none, so
¥1500 prints as ¥1500. And an amount with more digits than the currency allows,
such as £9.999, is refused at the door instead of being quietly rounded.

### 4. Rounding is a choice, made once

Some sums do fall between two pennies: 20% of 99p is 19.8p. Money will not
round that by itself; the caller must say how. And *where* you round matters.
Rounding the VAT on each of ten lines gives 20p ten times, £2.00. Rounding once,
on the £9.90 total, gives £1.98. Neither is wrong, but they differ by two
pence, and a shop must pick one rule and use it everywhere. Money makes that
choice visible in the code instead of leaving it to whatever a double does.

### 5. Splitting without losing a penny

Dividing £10 by three gives £3.33 each, and £3.33 three times is £9.99: a penny
disappears. `allocate` splits by ratio instead. Each share is rounded down, and
the pennies left over are handed out one at a time, so £10 becomes £3.34, £3.33
and £3.33, which add back to exactly £10.00. The cart uses the same method to
spread a £5.00 basket discount across its lines in proportion to their value:
£2.25, £1.97 and £0.78, exactly £5.00. Refunds, tax lines and split payments
all need this.

### 6. The bill

Money is not free. A price is now a class, so every database table, message
and screen must convert it: £19.99 is stored as 1999 and GBP. And Money says
nothing about exchange rates: converting pounds to dollars needs a rate and a
date, which is a different concern, deliberately left out. Both costs are
small compared with a shop whose totals are off by a penny.

## The verdict

Use Money for every price, cost, fee and balance. Store whole minor units and a
currency code, round only at a decided point with a named rule, and split with
`allocate`. Reach for a library (Moneta, Joda-Money) in production; write one
yourself once, to understand it.

## How to recognise this in code you did not write

- A class or record named `Money`, `Amount` or `Price` with an amount and a currency.
- Fields like `amountMinor`, `priceInPence` or `cents` stored as `long`.
- `BigDecimal` with an explicit `RoundingMode`, never `double`, near prices.
- A method that splits an amount and hands out the remainder.

## Where you have already met this

- `java.math.BigDecimal`, the usual building block for money in Java.
- JSR 354, the Java Money and Currency API, and its reference implementation Moneta.
- Payment APIs such as Stripe, which take amounts as whole numbers of the smallest unit (`amount: 1999`, `currency: "gbp"`).
- Database columns like `price_pence INTEGER` next to a `currency CHAR(3)` column.
