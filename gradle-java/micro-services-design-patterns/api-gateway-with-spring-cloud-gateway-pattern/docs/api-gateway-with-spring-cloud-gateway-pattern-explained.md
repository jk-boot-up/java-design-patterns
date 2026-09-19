# API Gateway with Spring Cloud Gateway, Explained

## The pattern in one sentence

In Spring Cloud Gateway, a gateway is a routing table of paths and services, with filters applied on the way through.

## What is new here

The pattern is [API Gateway](../api-gateway-pattern). This page is only what Spring Cloud Gateway adds.

### One Address, Four Services

One gateway address serves four paths, and each goes to a different service.

```
  GET /api/catalogue/products/MUG-BLUE -> 200 catalogue answers for /products/MUG-BLUE
  GET /api/pricing/products/MUG-BLUE -> 200 pricing answers for /products/MUG-BLUE
  GET /api/inventory/products/MUG-BLUE -> 200 inventory answers for /products/MUG-BLUE
  GET /api/recommendations/products/MUG-BLUE -> 200 recommendations answers for /products/MUG-BLUE
  the client knows one address, and the gateway's routing table knows the rest.
```

### The Prefix Is Stripped

The gateway removes the public prefix before it forwards, and adds a header saying the request came through the gateway.

```
  the client asked for /api/pricing/products/MUG-BLUE. the pricing service was asked for: /products/MUG-BLUE.
  the pricing service saw the source header: gateway.
```

### One Token Check, For Every Route

A global filter rejects a request without a token, for every route. Nothing reaches a service.

```
  no token: 401
  no token, other route: 401
  requests that reached a service: 0.
  with a token: 200 catalogue answers for /products/MUG-BLUE
```

### One Service Down

When recommendations goes down, only its own route fails. But the status is 500, not 503, so it looks like a bug in the shop.

```
  recommendations: 500
  catalogue, still: 200
  the failure stayed on its own route. but a refused connection is reported as 500, not 503:
  to the client it looks like a bug in the shop. map it in the gateway if the difference matters.
```

### A Gateway Forwards

A page that needs three services still takes three calls. The gateway forwards each one. It does not merge them.

```
  a product page needs three services here, so the client made 3 calls, and 3 reached services.
  merging them into one response is a job for composition code, in or behind the gateway.
```

### A Slow Service

When pricing never answers, the gateway answers for it with a 504, after the timeout set in configuration.

```
  pricing never answers. the gateway answers for it: 504.
  the wait is a setting, spring.cloud.gateway.server.webflux.httpclient.response-timeout.
```

## The verdict

Use it for routing, authentication, headers and limits at the edge. Set a timeout on every route. Decide what a dead service looks like to clients. Compose responses somewhere else, or in a filter you write.

## How to recognise this in code you did not write

- `RouteLocatorBuilder` with `.route(...)`.
- `spring.cloud.gateway.server.webflux.routes` in configuration.
- A `GlobalFilter` bean.

## Where you have already met this

The public edge of most Spring-based platforms.

## When this is too much

For one service, a gateway is a hop that adds nothing.
