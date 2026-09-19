# Problem Statement

## Read the partner first

This project assumes [API Gateway](../api-gateway-pattern), which put one gateway in front of catalogue, pricing, inventory and recommendations, so the mobile app made one call to one address and lost nothing when a feature service went down. Nothing here is lost by skipping Spring Cloud Gateway, and [`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: four internal services, and a mobile app that should know only one address.

## What is new

**Spring Cloud Gateway** is a real gateway you configure, not one you write. You give it a routing table, and it forwards real HTTP requests, applying filters on the way.

```
  GET /api/catalogue/products/MUG-BLUE -> 200 catalogue answers for /products/MUG-BLUE
  GET /api/pricing/products/MUG-BLUE -> 200 pricing answers for /products/MUG-BLUE
  GET /api/inventory/products/MUG-BLUE -> 200 inventory answers for /products/MUG-BLUE
  GET /api/recommendations/products/MUG-BLUE -> 200 recommendations answers for /products/MUG-BLUE
  the client knows one address, and the gateway's routing table knows the rest.
```

## The failure this project exists to show

It forwards, but it does not compose: a page that needs three services still takes three calls. A refused connection comes back as 500. And every filter you add runs for every route.
