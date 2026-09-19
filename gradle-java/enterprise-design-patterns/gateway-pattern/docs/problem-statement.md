# Problem Statement

## The scenario

The store takes payments through an outside provider. Checkout, subscription renewal and gift-card top-ups all need to charge a card. The provider's client uses maps of strings and two-digit result codes.

## The naive version

Each of the three features builds the provider's request and reads the provider's codes itself.

```
  checkout: paid, receipt AC-4999. renewal: renewed. gift card: topped up.
  three places build the provider's request fields and read its result codes. network calls made: 3.
  one of them forgot the currency field. nobody has noticed yet.
```

## What this project must deliver

A `PaymentGateway` in the shop's own words; an Acme gateway that alone knows the provider's fields and codes and retries a timeout once; a BetaPay gateway behind the same door; a fake that never touches the network; the naive callers, one of which forgot the currency; the limit of a common interface; and a plain verdict.
