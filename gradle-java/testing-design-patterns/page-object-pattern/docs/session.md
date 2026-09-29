# Session Guide — Page Object Pattern

## Learning Objectives

By the end of the session you can:

- Explain why selectors in tests make them fragile.
- Write a page object with intent-named methods.
- Hide waiting for page updates inside the page object.
- Return the next page object from navigation methods.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Tests click selectors | 7 min |
| 0:17 | Act 2: A button is renamed | 7 min |
| 0:24 | Act 3: A Page Object | 7 min |
| 0:31 | Act 4: Return the next page | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and compare act two's 0 of 5 with act three's 5 of 5. Open
`CheckoutPage`: the `APPLY` constant and the wait in `applyCoupon`. Then read
`CheckoutPageTest`: no selectors at all.

## Exercises

1. Add a `removeCoupon()` method and a test for it.
2. Move the coupon box into its own `CouponPanel` component object.
3. Replace `FakeBrowser` with Selenium's `WebDriver` against a real page.
