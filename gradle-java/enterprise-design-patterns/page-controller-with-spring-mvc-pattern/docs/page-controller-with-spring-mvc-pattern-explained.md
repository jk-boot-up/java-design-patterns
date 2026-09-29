# Page Controller with Spring MVC, Explained

## The pattern in one sentence

With Spring MVC, a page controller is a @RestController per page, found by
annotation, with shared checks in a HandlerInterceptor.

## The 5 acts

### 1. One handler for every page

One handler serves every page under /old. Quantity parsing was added at the
top for the basket, which works, but it now runs for every page: the product
page, which has no quantity, crashes with 500.

### 2. A controller per page

Now each page has its own `@RestController` with its own `@GetMapping`. The
product page shows the steel kettle at £30.00; the basket page adds two mugs.
Neither knows about the other.

### 3. Input checked by Spring

An unknown product, SOFA-9, gets 404: the controller throws a
ResponseStatusException and Spring turns it into the response. A quantity of
"two" gets 400 without any code in the basket page: Spring could not convert
it to the int the method asks for.

### 4. A new page

A reviews page is added as one new class, ReviewsController. Spring finds it
by its annotation, and /reviews shows 4.5 stars from twelve customers. No
other controller was opened.

### 5. The bill, and an interceptor

The checkout page's author forgot the login check that the basket repeats, so
a customer who is not logged in sees the checkout page. Spring's answer is a
HandlerInterceptor registered once for /basket and /checkout: not logged in
gets 401, logged in gets the page. Shared checks belong in one place.

## The verdict

Give each page its own controller, let Spring handle input conversion and
status errors, and put every check that many pages share in an interceptor or
filter, never in each page.

## How to recognise this in code you did not write

- `@RestController` classes, one per screen or resource.
- `@GetMapping("/...")` with `@RequestParam` parameters.
- `WebMvcConfigurer.addInterceptors(...)`.

## Where you have already met this

- Spring MVC `@Controller` and `@RestController` classes.
- Pages in PHP, JSP and ASP.NET Razor Pages, one file per page.
- Django and Rails views and controllers per page.
