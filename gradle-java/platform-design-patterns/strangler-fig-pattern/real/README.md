# Tier 2 — the router as a real nginx, in front of two real services

Tier 1 makes the argument in one JVM. This directory runs the router as **nginx**, the thing a real migration
would use, in front of **two real HTTP services**. Both services are Tier 1's own classes: `legacy` runs the
legacy checkout's pricing and `fresh` runs the rewrite's, so whatever the router does is done to code Tier 1
already tested.

**Tier 2 is optional.** Skipping it loses none of the pattern.

```bash
./demo.sh          # compiles Tier 1, starts three containers, runs four acts, stops them
```

Requires a JDK 21, Docker, and a network the first time (Docker pulls a JRE and nginx). It starts three containers and
`demo.sh` removes them when it finishes or fails. To stop them by hand: `docker compose down`.

The parent's `settings.gradle` does not include this directory, so `./gradlew test` one level up never starts Docker.

## What is running

| Container | Image | What it is |
| --- | --- | --- |
| `strangler-demo-legacy` | built from `Dockerfile` | Tier 1's legacy pricing, behind `/api/orders/price`. |
| `strangler-demo-fresh` | the same image | Tier 1's rewritten pricing. The same endpoint, a different answer at exactly fifty pounds. |
| `strangler-demo-router` | `nginx:1.31.5-alpine` | The strangler. One file, `routes.conf`, decides where pricing goes. |

### The one file that moves a capability

`nginx/routes-legacy.conf`, `routes-shadow.conf` and `routes-fresh.conf` are the three states of `routes.conf`. The demo copies
one into place and runs `nginx -s reload`, which swaps the configuration in without dropping a connection.

```nginx
# shadow: legacy answers, and the new service receives a duplicate whose answer is discarded
location /api/orders/price {
    proxy_pass http://legacy;
    mirror /internal-shadow;
    mirror_request_body off;
}
```

`/api/orders/stock` is not in that file at all. It is legacy's in every state, which is why moving pricing
cannot move stock.

## The transcript

Captured from a real run. Never edit it by hand.

```
Compiling Tier 1 and starting three containers
========================================================================

Act 1 — every route starts on legacy
========================================================================
  a price for an order of exactly fifty pounds, and one of forty:
    total=6495 delivery=495 servedBy=legacy   (X-Served-By: legacy)
    total=5295 delivery=495 servedBy=legacy   (X-Served-By: legacy)
  stock, which will never move in this demo:
    served by legacy
========================================================================

Act 2 — shadow: legacy serves, and the new service receives a copy
========================================================================
  the new service before: requests=0 servedBy=fresh
    total=6495 delivery=495 servedBy=legacy   (X-Served-By: legacy)
  the new service after:  requests=1 servedBy=fresh
  what each service computed for order 3, from its own log:
    legacy: price id=3 -> total=6495 delivery=495 servedBy=legacy
    fresh:  price id=3 -> total=6000 delivery=0 servedBy=fresh

  The customer got legacy's answer. The new service was called as well, and the two
  disagree: at exactly fifty pounds legacy charges delivery and the rewrite does not.
  That is the difference Tier 1's shadow reads found, found here on real requests.
========================================================================

Act 3 — move pricing: a config edit and a reload, with no restart
========================================================================
    total=6000 delivery=0 servedBy=fresh   (X-Served-By: fresh)
  the same order, now served by the new service.
  did anything restart?
    router:  no, started 2026-09-19T10:03:08.903930503Z
    legacy:  no, started 2026-09-19T10:03:08.657223295Z
    fresh:   no, started 2026-09-19T10:03:08.656076045Z
========================================================================

Act 4 — roll pricing back, and nothing else moves
========================================================================
    total=6495 delivery=495 servedBy=legacy   (X-Served-By: legacy)
  stock was on legacy the whole time:
    served by legacy

  One file, one reload. Pricing came back, stock never moved, and no service was
  restarted. That is what a switch per capability is worth.
```

## What this shows that Tier 1 cannot

- **Moving a route needs no restart.** Act 3's start times show that the router and both services kept running through a
  route move. In Tier 1 a route is a field.
- **A shadow request is a real duplicate over a real network.** The new service's own counter went from 0 to 1.
- **The two answers disagree on real requests**, in the same way Tier 1's shadow reads found.

## What this still does not show

- **Comparison is by eye.** nginx's `mirror` sends the copy and discards the answer, so the two results are compared here by
  reading both services' logs. A real migration needs a component that compares them and reports differences, which is
  more than nginx does.
- **Two containers on a laptop are not two deployments** owned by two teams with two release calendars.
- **No data moves.** Pricing is stateless. Stock is where two sources of truth appear, and this demo never moves it.
- **The organisational part**, where migrations actually stall, is not something a container can show.
