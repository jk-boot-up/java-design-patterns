# Gateway Offloading, Explained

## The pattern in one sentence

Gateway Offloading moves the chores every service needs into the gateway in
front of them, so they are done once and the same way.

## The 5 acts

### 1. Every service checks for itself

Catalog, cart and orders each check the sign-in token with their own copy of
the code. A customer's token expired a minute ago. Catalog and cart refuse it
with 401. Orders answers 200, because the orders team's copy never checks
expiry. Three copies of the same check, and one of them is wrong.

### 2. One check, at the gateway

Now the gateway checks the token once, before routing. The same expired
token is refused with 401 for catalog, cart and orders alike. A valid token
reaches the orders service, which is told who the customer is in a header.
The services hold no sign-in code at all.

### 3. Rate limiting

The gateway also limits each customer to five requests a second. A customer
sends eight in one second: five pass and three are refused with status 429,
too many requests. The orders service only ever sees five, and none of the
services had to write a rate limiter.

### 4. Compression

The catalog page is ten thousand bytes of JSON. For clients that accept it,
the gateway compresses the response with gzip, to under a fifth of its size.
One compressor at the gateway, instead of one in every service.

### 5. The bill

The services now trust whatever the gateway tells them. So a call that goes
straight to the orders service, skipping the gateway and claiming to be
another customer, is accepted. The services must only be reachable through
the gateway. And with everything going through one place, a gateway fault
or a slow gateway hits every page at once.

## The verdict

Offload generic, shared chores, such as sign-in checks, rate limits,
compression, TLS and logging, when many services need them. Keep business
rules in the services, block every side door, and run the gateway as the
critical component it now is.

## How to recognise this in code you did not write

- Gateway plugins for JWT validation, rate limiting or gzip.
- Services reading the caller from a header such as `X-User-Id`.
- TLS ending at a load balancer, with plain HTTP behind it.

## Where you have already met this

- API gateways: Kong, NGINX, Envoy, AWS API Gateway, Spring Cloud Gateway.
- TLS termination at a load balancer.
- Rate-limiting and JWT-validation plugins on a gateway.
