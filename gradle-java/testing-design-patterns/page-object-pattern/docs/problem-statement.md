# Problem Statement

## The scenario

Browser tests for the store's checkout type a coupon, click apply and read the
total.

## The naive version

Tests that name selectors themselves read totals too soon, and all break
together when a button is renamed.

## What this project must deliver

- A raw test reading a stale total.
- A renamed button breaking every raw test.
- A page object with selectors and waiting in one place.
- Navigation returning the next page object.
- The maintenance rule: report, don't assert.
- A real test class written with the page object.
