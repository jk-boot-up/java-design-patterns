# Problem Statement

## The scenario

Placing an order: validate the cart, check stock, take payment, write the
order, send an email.

## The naive version: the logic in the controller

With one door, the web controller, it works.

```
ONE. The logic in the controller — with one door, it works.
  a good order:   placed
  charged: 20000 pence, emails sent: 1
```

Then support asks for a command line. The logic is copied. Later the web door
is fixed to reserve stock before taking payment. The copy is not.

```
TWO. A second door — the logic is copied, and it drifts.
  through the web:  refused: only 3 Mouse in stock, 5 wanted, charged 0
  through the CLI:  refused: only 3 Mouse in stock, 5 wanted, charged 6000
```

A customer is charged, or not, depending on which door they came through.

## The other naive version: it all in the domain object

`Order.place()` looks tidy until the order needs a payment gateway, an email
service, a database and the products. Its constructor takes six things. It is
no longer a domain object.

## What this project must deliver

One `placeOrder`, called by both doors, that owns the orchestration and the
transaction, with the rules left in the domain.
