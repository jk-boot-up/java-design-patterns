# Problem Statement

## The scenario

The checkout reads a price and a sku from the catalog's price service. The reports service reads only the sku. The catalog team wants to change the answer's shape.

## The naive version

Change the provider, run its own tests, and release. Consumers find out when they fail.

```
  the catalog renamed priceCents to price and released. checkout, 2 mugs: total -1, meaning the order failed.
  it was found in production, by a customer.
```

## What this project must deliver

A price provider with releases that rename a field, add a field, and change a field's meaning; contracts as data, listing field names and types; two consumers with different contracts; a verifier that runs the provider's real answer against every contract and names the consumer and the field; and a release that passes and is still wrong.
