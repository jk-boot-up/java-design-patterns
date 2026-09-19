# MVC with Spring MVC, Explained

## The pattern in one sentence

In Spring MVC, a controller method returns a view name and a model, and the framework does the rendering.

## What is new here

The pattern is [MVC](../mvc-pattern). This page is only what Spring MVC adds.

### The Controller Names A View

A browser request gets an HTML page. The controller named a view, and the model supplied the total.

```
  GET /orders/ORD-000001, as a browser -> 200, text/html.
  the page says: Total: £292.50, Discount: £32.50.
```

### The Same Model, A Second View

A program asking for JSON gets the same model as data. A second controller method was added, and the model did not change.

```
  GET /orders/ORD-000001, as a program -> 200 {"orderId":"ORD-000001","customer":"ada","lines":[{"sku":"ESP-001","quantity":1,"pricePence":30000},{"sku":"BNS-220","quantity":2,"pricePence":1250}],"subtotalPence":32500,"discountPence":3250,"totalPence":29250}
  the controller method changed, and the model did not.
```

### Computed Once

One page view computes the summary once. The model can also be run with no server at all.

```
  summaries computed for one page view: 1.
  the model alone, no server: £292.50.
```

### A Sum In The View

A template that adds up the lines itself shows 32500, and never applies the discount that the model knows about.

```
  the shortcut view says: Total: 32500. the model says 29250 pence.
  the view added up the lines and never heard of the discount.
```

### The Same View, Another Order

The template that adds up two named lines fails on an order with one line. The real view shows any number of lines.

```
  POST /orders -> 302 redirect to /orders/ORD-000002.
  the shortcut view on that one-line order: 500.
  the real view on it: 200, Total: £12.50.
```

### Post, Redirect, Get

A form post answers with a redirect to the new order's page. Refreshing repeats the read, not the write.

```
  the form post answered with a redirect, not a page.
  refreshing the browser repeats the GET, and cannot place the order twice.
```

## The verdict

Compute in the model, once. Keep templates to display. Keep the controller thin. Use a redirect after a form post. Test the model without a server.

## How to recognise this in code you did not write

- `@Controller` methods that return a string and take a `Model`.
- Templates under `resources/templates`.
- `redirect:` in a return value.

## Where you have already met this

Every server-rendered Spring web page.

## When this is too much

For an API with no pages, a controller that returns data is enough, and there is no view to separate.
