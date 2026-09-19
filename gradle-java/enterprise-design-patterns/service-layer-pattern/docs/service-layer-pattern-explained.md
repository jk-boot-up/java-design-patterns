# Service Layer, Explained

## The pattern in one sentence

A service layer defines the application's operations, so every door calls one
`placeOrder`.

## How it works

`OrderService.placeOrder` begins a transaction, asks the domain to build the
order, reserves stock, takes payment, writes the order, commits, and then
sends the email. `WebController` and `SupportCli` are both thin. Each turns a
request into a call and a result into a reply.

```
FOUR. The pattern — one placeOrder, two doors.
  through the web:  refused: only 3 Mouse in stock, 5 wanted, charged 0
  through the CLI:  refused: only 3 Mouse in stock, 5 wanted, charged 0
  the same answer, because there is one placeOrder.
```

The service owns the order of the steps and the transaction boundary. The
domain owns the rules: `Order.from` rejects an empty cart, and
`Product.reserve` refuses to take stock below zero.

## The bill

**The anemic domain model.** Push too much into services and the domain
objects become bags of getters and setters with no behaviour. It is the most
common shape in enterprise Java and is widely considered an anti-pattern.

```
FIVE. The bill — the anemic domain model.
  AnemicOrder has 8 methods. all getters and setters: true
```

**The line is hard to draw.** The honest dividing line is: business rules in
the domain, orchestration in the service. But "free delivery over fifty
pounds" could be a rule about the order or about shipping, and reasonable
teams draw it differently.

```
SIX. The line is hard to draw.
  "free delivery over 50 pounds": is that a rule about the order, or about shipping?
  another team could put it in a ShippingService, and be just as right.
```

## Alternatives named

Transaction Script, one procedure per operation, is roughly what the naive
controller is. Table Module is another way to organise domain logic. This
project names both and teaches neither.

## Where you have already met this

A `@Service` class with `@Transactional` on `placeOrder` is this pattern. The
annotation draws the transaction boundary at the service.

## When this is too much

For one door and one operation, a service layer is an extra class. It earns its
place the moment a second door appears.
