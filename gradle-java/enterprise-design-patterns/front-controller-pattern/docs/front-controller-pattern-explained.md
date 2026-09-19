# Front Controller, Explained

## The pattern in one sentence

A front controller is a single entry point that every request passes through, where the shared work of logging, signing in, routing and error handling is done once.

## The six acts

### Every Handler Looks After Itself

The orders handler has no sign-in check, so a visitor who is not signed in receives ada's orders. The account handler checks, but logs only what it accepts, so neither request is logged.

```
  /orders with no sign-in: 200 ada's orders: ORD-1, ORD-2
  /account with no sign-in: 401 please sign in
  requests logged: 0 of 2. the orders handler has no login check and no log line, and the account handler logs only what it accepts.
```

### One Entry Point

Through the front controller, orders without a sign-in is refused and orders with one is served. Products, listed as public, needs neither. The check is written once.

```
  /orders with no sign-in: 401 please sign in
  /orders signed in:       200 ada's orders: ORD-1, ORD-2
  /products, public:       200 the catalogue: mug, tea, machine
  the login check is written once. no handler can forget it, because no handler has it.
```

### Routes In One Table

An unknown page gets a 404 and a wrong method a 405, both from the routing table, in one place.

```
  /nowhere:        404 no such page
  POST /products:  405 method not allowed
  every unknown page and wrong method is answered the same way, in one place.
```

### Everything Is Logged

The log has all three requests, including the refused one and the missing page, because logging is a filter that runs first.

```
  GET /orders -> 401
  GET /orders -> 200
  GET /nowhere -> 404
  the refused request and the missing page are in the log. the naive handlers logged neither.
```

### Failures Are Handled Once

A handler throws an error whose message contains a password. The customer sees a plain five hundred. The detail goes to the log only.

```
  a handler throws. the customer sees: 500 something went wrong.
  the log has the detail: error on /broken: database password is hunter2.
  the message with the password stayed in the log, and never reached the customer.
```

### The Bill: One Door

One filter with a bug in it makes every page return a five hundred at once. The front controller is the one place everything depends on.

```
  one filter with a bug in it. /products: 500 something went wrong, /orders: 500 something went wrong, /account: 500 something went wrong.
  every page is down at once. the front controller is the one place everything depends on.
```

## The verdict

Use a front controller for any application with several pages or endpoints and shared concerns: sign in, logging, error handling, routing. Keep filters small, ordered, and well tested, because everything depends on them. Keep handlers free of the shared work. Most web frameworks give you one already, so learn the one you have.

## How to recognise this in code you did not write

- A single servlet or dispatcher mapped to every path.
- A filter chain, or middleware, in front of the handlers.
- A routing table or annotations that map paths to methods.
- `DispatcherServlet` in Spring, `app.use(...)` in Express, `Rack` middleware in Ruby.

## Where you have already met this

Spring's `DispatcherServlet`, servlet filters, Express and Koa middleware, and every API gateway.

## When this is too much

For a program with one endpoint, a front controller is a door in front of a door. Its risk is being a single point of failure, so keep it simple and tested.
