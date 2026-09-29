# Secure Gateway, Explained

## The pattern in one sentence

A Secure Gateway is a secret-free gatekeeper that is the only thing the
internet can reach, passing on only requests of an allowed shape.

## The 5 acts

### 1. The service faces the internet

The order service answers the internet directly. A normal request for order 7
works. But a request with the internal-tools header `X-Internal-Admin: true`
exports all twelve thousand orders, and so does `/orders/../admin/export`,
which the service tidies into `/admin/export`. And the machine the internet
talks to holds the database password.

### 2. A gatekeeper in front

Now the order service is moved off the internet, and a gatekeeper stands in
front. The gatekeeper strips every header whose name starts with
`X-Internal-`. The same spoofed request now just returns order 7: the admin
header never reaches the service.

### 3. An allow-list

The gatekeeper lets through only two shapes of request: GET an order by its
number, and POST a new order. The path with dot dot does not match, and is
stopped with 404. DELETE on an order is stopped with 405, method not allowed.
A normal POST creates an order.

### 4. Size and shape limits

The gatekeeper also limits size: a five-megabyte order is refused with 413,
too large. And an order number must be digits only, so `/orders/7 OR 1=1`, an
attempt to trick the database, does not match and is refused. So far, three
requests have passed and four were stopped at the gate.

### 5. The bill

If the gatekeeper itself is broken into, it holds no credentials and no data.
But every request pays an extra hop, and every new endpoint stays blocked
until someone adds it to the gate's list. The trusted services must still
check their own inputs: the gate is one layer, not the only one.

## The verdict

Put a gatekeeper in front of any service holding credentials or sensitive
data. Keep it free of secrets, allow-list request shapes, strip internal
headers, limit sizes, and still validate inside the services.

## How to recognise this in code you did not write

- A DMZ or public subnet holding only proxies.
- Proxy rules listing allowed methods and paths.
- Headers such as `X-Internal-...` removed at the edge.

## Where you have already met this

- A web application firewall or reverse proxy in a DMZ, in front of internal services.
- NGINX or Envoy configured with an allow-list of paths and methods.
- Cloud API gateways with request validation and size limits.
