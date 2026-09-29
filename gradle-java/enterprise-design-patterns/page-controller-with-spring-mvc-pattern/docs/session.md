# Session Guide — Page Controller with Spring MVC Pattern

## Learning Objectives

By the end of the session you can:

- Write one @RestController per page.
- Let Spring convert and check request parameters.
- Answer 404 with a ResponseStatusException.
- Move shared checks into a HandlerInterceptor.

## Timetable

| Start | Topic | Time |
| --- | --- | --- |
| 0:00 | The problem and the analogy | 10 min |
| 0:10 | Act 1: One handler for every page | 7 min |
| 0:17 | Act 2: A controller per page | 7 min |
| 0:24 | Act 3: Input checked by Spring | 7 min |
| 0:31 | Act 4: A new page | 7 min |
| 0:38 | Act 5: The bill, and an interceptor | 7 min |
| 0:45 | Exercises | 15 min |

## Walkthrough

Run `./gradlew run`. Open `ProductController`: one method. Open `ShopApp`: the
interceptor registered for two paths. Compare act five's 200 and 401.

## Exercises

1. Register the interceptor for every path except /product and /reviews.
2. Add a wishlist page as a new controller.
3. Return an HTML view with a template instead of plain text.
