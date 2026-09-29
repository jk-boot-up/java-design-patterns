# Session Guide — Page Object with Selenium Pattern

## Learning Objectives

By the end of the session you can:

- Drive a real browser with Selenium WebDriver.
- Write a page object with selectors and waits.
- Wait for a real condition instead of a fixed pause.
- Return the next page object from navigation.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: Selectors in the test | 7 min |
| 0:17 | Act 2: A button is renamed | 7 min |
| 0:24 | Act 3: A Page Object | 7 min |
| 0:31 | Act 4: Return the next page | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` with Docker running. Compare act one's 50.00 with act
three's 45.00. Open `CheckoutPage`: the APPLY constant and the WebDriverWait.
End on act two's 0 of 5 against act three's 5 of 5.

## Exercises

1. Add a removeCoupon method and a test for it.
2. Take a screenshot when a test fails.
3. Run the same page objects against Firefox with the standalone-firefox image.
