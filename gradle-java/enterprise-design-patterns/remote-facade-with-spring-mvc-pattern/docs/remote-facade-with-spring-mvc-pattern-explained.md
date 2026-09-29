# Remote Facade with Spring MVC, Explained

## The pattern in one sentence

With Spring MVC, a remote facade is a thin controller that offers remote
callers coarse, screen-sized calls, over fine-grained objects inside.

## The 5 acts

### 1. A call for every fact

The phone app asks the fine-grained endpoints for each fact of the order
screen: customer Priya, the items, the total of £46.00, the address and the
slot. Five round trips, each paying the mobile network's 80 milliseconds:
over 0.4 seconds before the screen can be drawn.

### 2. The whole screen as JSON

The facade's `GET /order-summary` returns one JSON document, built by Jackson
from a Java record: the order number, customer, items, total, address and
slot. One round trip, under 0.2 seconds.

### 3. All or nothing

With small calls, the address changes, then the slot change is refused, and
the fine-grained API, with no error handling, answers 500. The order is left
half changed: new address, old slot. The facade's one `PUT /order-delivery`
checks the slot before changing anything: Sunday is refused with 422 and the
order is unchanged; Tuesday succeeds and both change together.

### 4. Fine-grained inside

Inside the server, nothing became coarse. The facade calls the Order's small
methods in-process, where calls are cheap, and the rule about valid slots
stays on the Order. The refusal came back as a standard problem report, with
the content type application/problem+json.

### 5. The bill

A small widget that shows only the delivery slot needs 8 bytes from the small
call, but 130 from the summary. And each new screen may want its own facade
method, so the facade grows with the app.

## The verdict

Offer screen-sized calls to remote callers, especially over slow networks.
Make changes all-or-nothing, report refusals as ProblemDetail, keep rules on
the domain objects, and add small calls where a screen really needs little.

## How to recognise this in code you did not write

- Endpoints named summary or details returning a whole screen.
- Record DTOs returned from `@RestController` methods.
- `@ExceptionHandler` methods returning `ProblemDetail`.

## Where you have already met this

- REST endpoints that return a whole screen, such as order summaries.
- Backends for frontends, which give each app its own coarse API.
- GraphQL, which lets the client ask for a whole screen in one request.
