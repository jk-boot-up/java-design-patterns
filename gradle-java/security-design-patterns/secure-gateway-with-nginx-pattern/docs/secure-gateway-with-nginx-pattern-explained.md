# Secure Gateway with NGINX, Explained

## The pattern in one sentence

With NGINX, a secure gateway is a secret-free reverse proxy whose
configuration allow-lists locations and methods, limits size and strips
internal headers.

## The 5 acts

### 1. The service faces the internet

The order service is called directly. A normal request for order 7 works. A
request with the internal-tools header X-Internal-Admin set to true exports
all twelve thousand orders, and so does the path /orders/../admin/export,
which the service tidies into /admin/export. And this machine holds the
database password.

### 2. An NGINX gatekeeper

Now NGINX stands in front. A request for order 7 works as before. The same
request with the admin header just returns order 7, because the
configuration sets X-Internal-Admin to an empty value, which removes it before
the request goes on.

### 3. An allow-list of locations

NGINX normalises a path before choosing a location, so /orders/../admin/export
becomes /admin/export, which no allowed location matches: 404. DELETE on an
order is refused by limit_except with 403. A normal POST creates an order:
201.

### 4. Size and shape

A five-megabyte order is refused by client_max_body_size with 413. A request
for order "7 OR 1=1", an attempt to trick the database, matches no location,
because the order number must be one to nine digits: 404.

### 5. The bill

A look inside the NGINX container finds no password in its environment: a
gatekeeper broken into gives nothing away. The costs: every request pays an
extra hop, a new endpoint stays blocked until a location is added for it, and
the order service must still check its own inputs.

## The verdict

Put a gatekeeper such as NGINX in front of any service holding credentials or
sensitive data. Keep its configuration an allow-list, keep secrets off it,
and still validate inside the services.

## How to recognise this in code you did not write

- `location` blocks ending in `location / { return 404; }`.
- `proxy_set_header X-Internal-... "";`.
- `limit_except` and `client_max_body_size` directives.

## Where you have already met this

- NGINX or HAProxy as a reverse proxy in a DMZ.
- Web application firewalls such as ModSecurity rules on NGINX.
- Cloud load balancers with path-based rules.
