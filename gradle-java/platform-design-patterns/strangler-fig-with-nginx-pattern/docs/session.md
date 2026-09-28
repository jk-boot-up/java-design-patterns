# Session Guide — Strangler Fig with NGINX Pattern

A 60-minute session built around one question: once the router is a real proxy with rules of its own, how do you know a route really moved, and what does moving it touch besides the route?

## Learning Objectives

1. Say, in plain words, what a reverse proxy, a location, a prefix, a regular expression, `^~`, `proxy_pass` and a reload are.
2. Show one route moving to the new service while the old shop keeps serving the rest, and a request in progress finishing on the old configuration.
3. Explain why an ordinary prefix location can lose to an older regular-expression location, and what `^~` changes.
4. Predict the path the new service receives from a `proxy_pass` with and without a trailing slash.
5. Name the bill: a moved route that can fail on its own, a cookie only one service understands, and three things to run.

## Timetable

| Time | Section |
| --- | --- |
| 0:00–0:08 | The office receptionist analogy, and the twin project recapped in two minutes |
| 0:08–0:16 | Act one: the big bang |
| 0:16–0:28 | Act two: one route, a reload, and a request in progress |
| 0:28–0:40 | Act three: which location wins |
| 0:40–0:46 | Act four: one slash |
| 0:46–0:52 | Acts five and six: the new service down, and the cookie |
| 0:52–1:00 | Exercises, and the verdict |

## Walkthrough

Start Docker Desktop, or another container runtime, first.

```bash
cd platform-design-patterns/strangler-fig-with-nginx-pattern
./gradlew -q run
```

Act one: why did the price page still work after the big bang, and why did the other three answer 404 rather than 502? Act two: what did "number 1 before and number 1 after" prove, and which process finished the open request? Act three: the reload succeeded and `nginx -t` passed; how would anybody have noticed the move did nothing? Act four: which part of the path did the slash remove? Act five: who wrote the 502? Act six: NGINX passed the cookie on; whose fault is the empty basket?

Then open `src/main/java/com/jk/explore/stranglerfignginx/NginxConfig.java` and read `render` aloud. Every configuration in the demo is that method with different choices. Point at `Move.block`: the three ways of moving a route differ by the characters `^~ ` and `/`.

## Discussion

Ask the room how they would find out, in production, that a move did nothing. The responses were all 200 and all correct prices. The only differences were a header naming the service and a `Cache-Control` header from the old rule. Would anybody be watching either?

Then ask who owns the gateway configuration in their organisation. The old system's team, who wrote the regular expression years ago, or the new service's team, who wrote the move? The bug in act three lives between the two.

## Exercises

1. Move `/api/stock/` as well as prices in the configuration with the old caching rule, without `^~`. Predict which service answers each, then run it.
2. Change the moved location to `location = /api/prices/SKU-1`, an exact match, and predict whether the old regular expression still wins for SKU-1 and for SKU-2.
3. Write `proxy_pass http://new_service/api/prices/;` with the trailing-slash location and predict the path the new service receives.
4. In act five, add a second server to the `new_service` upstream, pointing at the old shop, marked `backup`. What does the customer see when the new service is down, and what have you hidden?
5. Make the new service accept the old shop's `LEGACYSESSION` by asking the old shop for the basket. What has the new service now come to depend on?

Close with the verdict: one catch-all to the old system; every moved route with `^~`; the slash written on purpose; a reload waited for, not assumed; and every cookie a route depends on found before the route moves.
