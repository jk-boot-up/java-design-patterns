# Problem Statement

## The scenario

The cart screen shows a total, an item count, and a checkout button that is on only when the cart is not empty.

## The naive version

Put the total, the count and the checkout rule inside the screen class, next to the widgets.

```
  to check the total and the checkout rule, a screen was needed. windows opened: 1.
  total label: £16.00, checkout enabled: true. the rules are welded to the widgets.
```

## What this project must deliver

A cart model; a fat screen that needs a window to check anything; a presenter with a passive view interface and a recording view that draws nothing; a view model with observable state and no reference to a view; a bound screen; two screens sharing one view model; and a screen that forgot to bind, which is wrong without any error.
