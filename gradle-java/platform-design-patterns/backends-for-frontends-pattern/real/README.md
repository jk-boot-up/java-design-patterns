# Backends for Frontends — the real version

Tier 1 makes the pattern's argument by counting calls inside one JVM. This is the
same argument with the calls actually made: three Spring Boot services on three
ports, two differently shaped JSON documents of visibly different sizes coming
back from two addresses, and every byte count measured by the client rather than
claimed by the server.

Nothing here changes what Tier 1 teaches. It is here to check it.

```bash
./demo.sh
```

Needs a JDK 21 and, the first time, a network connection so Gradle can fetch
Spring. **No Docker.** Tier 1 needs none of it, which is why the two are separate
Gradle builds — `./gradlew test` one directory up does not know this directory
exists.

## What is running

| Process | Port | What it is |
| --- | --- | --- |
| `shop` | 8082 | The five services — catalog, pricing, inventory, reviews, recommendations — plus the one shared endpoint in front of them. Everything that existed *before* anybody wrote a backend for a frontend. |
| `mobile-bff` | 8080 | The phone team's backend. `GET /phone/product-screen/{sku}` |
| `web-bff` | 8081 | The desktop team's backend. `GET /desktop/product-page/{sku}` |

The five services share one process, and that is a simplification worth naming.
What matters to this pattern is not that they are five deployments; it is that
they are five separate **calls**, each on its own path, each returning its own
whole document, and that a client wanting all five has to make all five. That
part is real here.

Two things about the two backends are real in a way Tier 1 could only assert.
They are separate processes with separate addresses, which is the closest a
repository can get to "owned by the team that owns the screen". And they are both
running at once, neither a fallback for the other, answering the same question
differently on purpose.

## The endpoints

| Endpoint | Purpose |
| --- | --- |
| `GET /api/products/{sku}` | The shared endpoint: the union of everything anybody needs |
| `GET /api/products/{sku}?fields=a,b,c` | The same, trimmed to named fields — including one level of nesting, so `pricing.nowPence` works |
| `GET /phone/product-screen/{sku}` | Six flat fields, in the form the phone screen draws them |
| `GET /desktop/product-page/{sku}` | Fifteen fields, including the description, five images and three reviews |
| `GET /phone/saving/{sku}`, `GET /desktop/saving/{sku}` | The discount label each backend would print — the last act |
| `POST /pricing/review` | The pricing team's rule review, as something the demo can trigger |
| `GET /calls`, `POST /calls/reset` | The shop's own tally of calls that arrived |

`/calls` is the one number in this walkthrough a backend cannot fake. Tier 1
counts calls in a `CallLog` the caller writes to, which is honest inside one
process and would be worth nothing here. These counts are kept by the callee, so
when the demo says the phone's backend made four internal calls and not five,
that four is the shop's own record of requests that actually arrived.

## The walkthrough

Everything below is captured output from `./demo.sh`, not written from memory.

### One shared endpoint, for everybody

```
  GET /api/products/SKU-4417
    1754 bytes, 12 top-level fields
    the phone draws six of them
    catalog=1  pricing=1  inventory=1  reviews=1  recommendations=1
    total internal calls: 5
```

One round trip from the device instead of five, which is the expensive part gone
and which the finished pattern keeps rather than undoes. But one endpoint
publishes one document, and that document has to satisfy every client, so it is
the union of all of them.

### And the obvious fix works

```
{
    "title": "Copper Filter Coffee Maker, 1 Litre",
    "pricing": {
        "nowPence": 4799
    },
    "thumbnail": "https://img.shop.example/4417/hero-320.jpg",
    "reviews": {
        "average": 4.6,
        "count": 218
    },
    "inventory": {
        "nextDelivery": "2026-09-18"
    }
}
  → 212 bytes on the wire

  1754 bytes down to 212, from a query parameter.
```

Thirty lines of projection code in `SharedApiController`, no new process to run,
nothing to deploy. **If this pattern were about payload size, this directory
would end here**, and so would a lot of write-ups.

### The request the shared endpoint cannot serve

The phone team want one line of text under the price — a delivery sentence,
joined from stock, the delivery rules and the clock. Ask for it by name, exactly
the way every other field was asked for:

```
  GET /api/products/SKU-4417?fields=delivery
{}
```

Empty, and not because of a typo. No service owns that field, so the shared
endpoint has no vocabulary for it. Adding it here would change a document five
other clients also receive, which makes it a contract change, a review, and a
place in a queue behind work that has nothing to do with the phone. Half an hour
of work; five weeks of waiting. **That is the saving, and it is not a number.**

### A backend for the phone

```
{
    "title": "Copper Filter Coffee Maker, 1 Litre",
    "price": "£47.99",
    "image": "https://img.shop.example/4417/hero-320.jpg",
    "rating": 4.6,
    "ratingCount": 218,
    "delivery": "Free delivery, arrives 2026-09-18"
}
  → 196 bytes on the wire

  what the shop was asked for, to serve that one request:
    catalog=1  pricing=1  inventory=1  reviews=1  recommendations=0
    total internal calls: 4
```

Four, not five — from the shop's own tally. Recommendations is reachable and was
not asked, because this screen has no related-products strip and the answer would
have had nowhere to go. A shared endpoint cannot make that decision on behalf of
one client.

The price arrived as the string `"£47.99"`; pricing returned the integer `4799`.
The delivery field arrived as a whole English sentence.

### A backend for the desktop

Fifteen fields, 1409 bytes, five internal calls — and the field worth comparing
is `delivery`, which is the bare date `"2026-09-18"` rather than a sentence,
because the desktop page has a delivery panel with its own layout and wants the
parts. Two backends over the same data, disagreeing about what a product is, is
not an inconsistency waiting to be tidied up.

### The same product, several ways

```
  design                                bytes   fields  internal
  one shared endpoint                    1754       12         5
  shared endpoint, ?fields=               212        6         5
  a backend for the phone                 196        6         4
  a backend for the desktop              1409       15         5
```

The `?fields=` row is the one to sit with, and it is the row most write-ups of
this pattern leave out. It lands in the same territory as the phone's own
backend, from one query parameter. The backend's advantage over it is not in this
table at all.

### The bill — one rule, two answers

```
  Before the pricing review, both backends claim a saving:
    phone:   'Save £12.00'
    desktop: 'Save £12.00 (20%)'
```

Then the pricing team finish their review: a higher price may only be advertised
as a saving if it was genuinely in force long enough, and this one went up eleven
days ago. The shop is told, once, in one place. Both backends read pricing on
every request, so **both are told**.

```
  POST /pricing/review
{
    "note": "the higher price no longer qualifies to be advertised against",
    "listPriceHeldLongEnough": false
}

  Same product, same price, same second, asked again:
    phone:   'Save £12.00'
    desktop: ''

  Both services are healthy:
    phone:   {"groups":["liveness","readiness"],"status":"UP"}
    desktop: {"groups":["liveness","readiness"],"status":"UP"}
```

One of those two screens is now advertising a saving the shop is not allowed to
claim. Nothing threw. Nothing was logged. Both processes report UP. `SavingRules`
in `mobile-bff` does not even take the `listPriceHeldLongEnough` flag as an
argument, so there is no branch to get wrong — and no test writable inside either
process could notice, because from inside each backend, each backend is right.

**A backend for a frontend may hold the shape. Anything the shop would still
believe with every client switched off belongs behind it.**

Note what the two backends duplicate, and which duplication is which. `Money` is
copied into both and that is fine: formatting money for a screen is presentation,
the one thing these backends are supposed to own. `SavingRules` is copied into
both and that is the bug. The difference is not how much code there is.

## What Tier 1 got right, and the one place the numbers differ

| | Tier 1 | Tier 2 |
| --- | --- | --- |
| shared endpoint | 1755 | 1754 |
| `?fields=` | 212 | 212 |
| phone's backend | 196 | 196 |
| desktop's backend | 1391 | 1409 |
| internal calls, phone | 4 | 4 |
| internal calls, desktop | 5 | 5 |

Close enough to be worth explaining rather than glossed over. Tier 1's `Doc`
measures its own rendering; Tier 2's numbers are Jackson's serialisation measured
by `curl` on the receiving end. The two differ by a byte here and eighteen there
in whitespace and escaping conventions, and by nothing that matters.

The two claims Tier 1 could have been wrong about, and was not: the phone's
document really is an order of magnitude smaller than the shared endpoint's over
a real connection, and the phone's backend really does make one fewer internal
call than the desktop's — measured this time by the process on the other end.

## What this tier still does not show

Being clear about this is the obligation every project in this category carries.

- **Three processes is not a deployment.** There is no container, no service
  discovery, no load balancer and no TLS. The addresses are localhost ports in a
  configuration file.
- **The calls are still sequential.** Both backends fan out to the shop one call
  at a time, exactly as Tier 1 does. A real backend would issue them together and
  wait once, which means both tiers **understate** the pattern's benefit.
- **No failure handling.** If the shop is down, both backends return a 500. A
  real backend for a frontend has timeouts, partial responses and a decision
  about which fields a screen can be drawn without.
- **No versioning, no schemas, no compression.** Real clients ship for years and
  cannot all be upgraded at once, which is a large part of what makes these
  backends worth owning and none of which is here.
- **The ownership claim is still a claim.** Three processes in one Gradle build,
  written by one person, cannot demonstrate that the phone team ships on their
  own cadence. That is the part of this pattern a repository cannot prove.

## Files

| Path | What it is |
| --- | --- |
| `settings.gradle` | Three modules, and the note on why this is a separate build |
| `build.gradle` | Shared Spring Boot settings; every version comes from the category catalogue |
| `shop/` | The five services, the shared endpoint with `?fields=`, the call counter |
| `mobile-bff/` | The phone's backend, and the stale copy of the saving rule |
| `web-bff/` | The desktop's backend, and the current one |
| `demo.sh` | The seven-step walkthrough that produced every transcript above |

Spring Boot **4.1.1**, pinned in
[`../../gradle/libs.versions.toml`](../../gradle/libs.versions.toml) with the
reasoning in the implementation plan's framework register. Two Boot 4 traps are
worth knowing if you are coming from Boot 3, and both are written up in the build
files rather than here: `spring-boot-starter-web` no longer brings an
auto-configured `RestClient.Builder`, so the two backends ask for
`spring-boot-starter-restclient` by name, and the shop — which calls nobody —
correctly does not.
