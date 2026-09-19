# Problem Statement

## The scenario

The same checkout, the same three collaborators (a discount policy, a payment
gateway and a notifier), one more time.

## The three earlier answers

[Registry](../registry-pattern) passed nothing and looked everything up in a global.
[Service Locator](../service-locator-pattern) asked a middleman. Both left the same
problem: a class that asks hides what it needs from everyone outside it.

## The pattern

The class declares what it needs in its constructor, and is given it.

```
ONE. The signature is the dependency list.
  CheckoutService(DiscountPolicy, PaymentGateway, Notifier)
  that is everything it needs: complete, and checked by the compiler.
```

## What this project must deliver

The wiring by hand, first, with its line count. A clear recommendation between the
three forms. A container written here, so it is demystified. And the costs.
