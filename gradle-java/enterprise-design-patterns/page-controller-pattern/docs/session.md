# Session Guide — Page Controller Pattern

## Learning Objectives

By the end of the session you can:

- Explain how one shared handler lets changes leak between pages.
- Write a controller per page with its own input handling.
- Add a page without touching the others.
- Name the cost that leads to Front Controller.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: One handler for every page | 7 min |
| 0:17 | Act 2: A controller per page | 7 min |
| 0:24 | Act 3: Errors stay on their page | 7 min |
| 0:31 | Act 4: A new page | 7 min |
| 0:38 | Act 5: The bill | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run` and read act one: a change for the basket broke the
product page. Open `OneHandler` and find the line. Then open `Controllers`:
four small classes. End on act five and search the four classes for
`loggedIn`: which one is missing it?

## Exercises

1. Add the login check to CheckoutController, and a test that fails without it.
2. Move the login check into a base class. What happens to controllers that do not need it?
3. Add a `/search?q=` page that lists matching products.
