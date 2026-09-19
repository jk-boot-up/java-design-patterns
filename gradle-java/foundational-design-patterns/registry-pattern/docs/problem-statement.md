# Problem Statement

## The scenario

A checkout needs three collaborators: a discount policy, a payment gateway and a
notifier. The payment gateway is needed six classes down.

## The naive version: pass it down

The gateway is handed through six constructors. Only the last uses it.

```
ONE. Pass it down — through six constructors.
  the gateway went through Storefront, CartService, OrderCoordinator, PricingStage,
  PaymentStage and Charger. only the last one uses it. the other five forward it.
```

This deserves real sympathy. It is friction, and pretending otherwise is dishonest.
It is also **honest**: every dependency is visible in a signature.

## What this project must deliver

A registry that removes the friction, and an account of what it costs, with
evidence. It must also say plainly where a registry is right.
