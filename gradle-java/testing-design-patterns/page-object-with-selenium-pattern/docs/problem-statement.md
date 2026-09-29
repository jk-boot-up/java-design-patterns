# Problem Statement

## The scenario

Browser tests for the shop's checkout type a coupon, click apply and read the
total, in a real browser.

## The naive version

Tests that find elements themselves read too soon and all break when a button
is renamed.

## What this project must deliver

- A raw test reading a stale total in a real browser.
- A renamed button breaking every raw test.
- A page object with selectors and WebDriverWait in one place.
- Navigation returning the next page object.
- The costs, including real browser speed.
- Every printed result asserted by a test, skipped without Docker.
