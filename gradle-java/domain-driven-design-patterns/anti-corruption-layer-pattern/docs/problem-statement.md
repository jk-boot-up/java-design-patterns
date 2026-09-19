# Problem Statement

## The scenario

The store's stock levels come from an old inventory system. It sends every value as a string, uses one-letter codes, and cannot be changed. Its owners add new codes now and then without warning.

## The naive version

Each feature reads the old system's record directly and has learnt the codes for itself: Y and N for in stock, A, D and S for status.

```
  what the old system sends: LegacyStockRecord[ITM_CD=MUG-BLUE, QTY_ON_HND=0012, IN_STK_FLG=Y, ITM_STAT=A, LST_CNT_DT=20260114, WHSE_CD=W01, UOM=EA].
  product page: in stock. basket: true. reorder: 38. report: MUG-BLUE 12 A.
  places in the shop that have learnt the codes Y, N, A, D and S: 4.
```

## What this project must deliver

A `StockLevel` in the shop's own words; one adapter that is the only class that knows the old codes; bad data refused with the sku named; a new legacy status handled in one place; the fields the layer drops listed; and a plain verdict.
