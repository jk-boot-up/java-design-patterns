# Gateway Offloading with Spring Cloud Gateway, Explained

## The pattern in one sentence

With Spring Cloud Gateway, offloading puts the shared chores in a global
filter and server settings, so every service behind gets them for free.

## The 5 acts

### 1. Every service checks for itself

Three real services each check the sign-in token themselves. An expired token
is refused by catalog and by cart with 401, token expired. The orders
service answers 200, orders for ana, because its copy of the check never looks
at the expiry.

### 2. One check at the gateway

Now every request goes through a Spring Cloud Gateway. Its global filter
checks the token before any route: the expired token is refused with 401 for
catalog, cart and orders alike. A valid token reaches the orders service,
with the customer passed on in the X-Customer header. The services hold no
sign-in code at all.

### 3. Rate limiting

The same filter keeps a token bucket for each customer: five requests, refilled
at five a minute. Eight requests in a row: five pass and three are refused
with 429, too many requests. No service had to write a limiter.

### 4. Compression

Reactor Netty, the gateway's server, is told by three properties to compress
JSON responses. The catalog page, 10,093 bytes plain, comes back with
Content-Encoding gzip at under a fifth of the size. The catalog service knows
nothing about compression.

### 5. The bill

Through the gateway, a caller with ana's token who adds X-Customer: ben still
gets ana's orders, because the gateway removes the header and sets its own.
But straight to the orders service, the same header is believed: 200, orders
for ben. The services must be reachable only through the gateway, and every
request now passes one more hop.

## The verdict

Offload generic chores to the gateway when many services need them. Strip
headers the services will trust, share rate-limit state across gateway
instances, block every side door, and run the gateway as the critical piece
it is.

## How to recognise this in code you did not write

- `GlobalFilter` beans with an order.
- `RouteLocatorBuilder` routes, or `spring.cloud.gateway` route properties.
- Services that read the caller from a header set by the gateway.

## Where you have already met this

- Spring Cloud Gateway global filters and route filters.
- Kong, NGINX, Envoy and cloud API gateways with auth and rate-limit plugins.
- `server.compression.enabled` on Spring Boot servers.
