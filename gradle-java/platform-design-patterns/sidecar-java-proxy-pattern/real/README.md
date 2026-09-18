# Tier 2 — two proxies, one port, and a service that is never told

Tier 1 makes the whole argument inside one JVM, where installing a proxy is
assigning a field and swapping one is assigning it again. That is honest about
the *shape* of the change and flattering about the *cost* of it. This directory
is where the four claims a single JVM cannot make get made:

1. **The proxy that answers changes language** — nginx configuration to Java —
   in a separate container, and the service is not rebuilt, restarted or told.
2. **The new proxy has to satisfy the same transport contract as the old one**,
   and the provider's own ledger says whether it did.
3. **A request arriving while nothing is bound to the port** is refused by the
   operating system, before anybody can see it or count it.
4. **The forty lines are not forty lines out here**, and the count below says
   how many they really are.

```bash
./demo.sh
```

Requires a JDK 21 and Docker. Tier 1 requires neither, which is why the two are
separate Gradle builds: the parent's `settings.gradle` does not include this
one, so `./gradlew test` one directory up never resolves Spring and still passes
offline.

> Every figure quoted below is pasted from a run of `demo.sh`. Nothing here is
> written from memory, and nothing here is rounded. Because this tier has a real
> network, a real TLS handshake and a real JVM in the path, the millisecond
> figures move by a few milliseconds from run to run; the *shape* is the claim.

## What is running

Four containers, and two of them are never up at the same time.

| Container | Image | What it is |
| --- | --- | --- |
| `sidecar-java-proxy-gateway` | built from `gateway/` | The payment provider. HTTPS only, TLS 1.3 only. Records the arrival time and outcome of every attempt. |
| `sidecar-java-proxy-checkout` | built from `payments/` | Checkout. No retry code, no TLS configuration, no provider address. Started once, and never restarted for the rest of the run. |
| `sidecar-java-proxy-nginx` | `nginx:1.31.5-alpine` | §41's proxy, mounting §41's configuration file unchanged. |
| `sidecar-java-proxy-java` | built from `javaproxy/` | The replacement. Plain JDK, no framework. |

Both proxies carry `network_mode: "service:checkout"`, which puts them inside
the service's network namespace, so all three containers share one network stack
and one set of ports. That is why the service can be configured with
`http://localhost:8081` and mean it — and it is also why **two proxies cannot be
up together**: one port, one listener. That constraint is not an awkwardness of
this demo; it is the swap window Act 7 is about.

`demo.sh` therefore starts containers by name rather than running `up` on the
whole file.

### Why the provider had to be rewritten for this project

§41's provider counted attempts and could be told to decline the first *n* of
them. That is useless here, because **both** proxies in this project make
exactly three attempts. A count-based provider cannot tell them apart.

So this provider is time-based instead. `POST /reset` takes
`{"unwellForMillis": 600, "allowance": 12}`, restarts its own clock, and declines
everything that arrives inside the first 600 milliseconds. Every attempt is
recorded with the millisecond it landed:

```json
{ "atMillis": 273, "reference": "ORD-4418", "service": "checkout", "outcome": "declined" }
```

A proxy claiming to have waited is a claim. Arrival times measured at the far
end are what happened, and the far end has no stake in the argument.

## The transcript

### Act 2 — the wobble, under a proxy that cannot wait

The provider declines everything for its first 600 milliseconds. nginx is on the
port.

```
    { "outcome": "declined", "reference": "ORD-4418", "service": "checkout",
      "note": "arrived at 59ms, unwell until 600ms" }

  what the provider itself recorded, at its own end:
    attempt at     24ms   declined
    attempt at     48ms   declined
    attempt at     59ms   declined
    3 attempts, first to last: 35ms

  and what checkout's nginx proxy logged, one line per attempt:
    checkout  172.21.0.2:9443, 172.21.0.2:9443, 172.21.0.2:9443  status=503, 503, 503  took=0.013, 0.015, 0.012  total=0.041
```

Three attempts, and the whole allowance for that payment was spent in
thirty-five milliseconds of a six-hundred-millisecond bad patch. Nobody wrote a
bug. The proxy did exactly what it was configured to do.

### Act 3 — the sentence there is nowhere to write

The demo prints the configuration the running container actually has, comments
stripped:

```nginx
upstream provider {
    server gateway:9443 max_fails=0;
    server gateway:9443 max_fails=0;
    server gateway:9443 max_fails=0;
}
...
    proxy_next_upstream error timeout http_503 non_idempotent;
    proxy_next_upstream_tries 3;
```

The provider's address appears three times because **three entries is how "up to
three attempts" is spelled when there is one address to talk to**. `proxy_next_upstream`
moves to the *next server in the group*, and it moves immediately. There is no
directive in nginx's http proxy module that expresses a wait between attempts —
`proxy_next_upstream_timeout` caps the total time across all of them, which is a
deadline, not a gap.

The provider's letter asked for "at most three attempts, and wait properly
between them." nginx can honour the first half of that sentence exactly and the
second half not at all.

### Act 4 — the swap

`docker compose stop sidecar-nginx`, then `docker compose up -d sidecar-java`.

```
  now bound to localhost:8081:  java-proxy

  checkout, which was not part of any of that:
    { "service": "checkout", "talksTo": "http://localhost:8081",
      "knowsTheProviderAddress": false,
      "retryCode": "none -- see PaymentsController.pay" }

    checkout started at 2026-09-17T19:15:07.536380333Z
    checkout now says   2026-09-17T19:15:07.536380333Z
```

Same container, same start timestamp before and after, same one-line
configuration. No jar was rebuilt and no service was restarted. There is no
notification step in `demo.sh` because there is nothing to notify: the only
thing the two proxy containers have in common is a port number, and the only
thing checkout ever knew was that port number.

### Act 5 — the same wobble, the same three attempts

Identical provider, identical 600ms wobble, identical payment, different proxy.

```
    { "outcome": "paid", "reference": "ORD-4418", "service": "checkout",
      "note": "arrived at 711ms", "receipt": "pay_ORD-4418", "amountPence": 4799 }

  what the provider itself recorded:
    attempt at     24ms   declined
    attempt at    273ms   declined
    attempt at    711ms   charged
    3 attempts, first to last: 687ms

  the provider's full ledger, including the transport it saw:
    { "allowance": 12, "unwellForMillis": 600, "total": 3, "refused": 0,
      "byService": { "checkout": 3 }, "firstToLastMillis": 687,
      "transport": "TLSv1.3 (the caller presented a certificate)" }
```

Set the two ledgers side by side. **35 milliseconds against 687**, and the same
number of attempts in both. The provider received no extra traffic out of this
change and its allowance is untouched; only the spacing moved, and by the third
attempt the provider was well again.

The `transport` line is the second claim discharged: the forty-line Java proxy
is presenting TLS 1.3 to the provider, exactly as nginx was, and checkout still
has no keystore, no trust store and no protocol list anywhere in its
configuration.

> **Why `demo.sh` sends a throwaway payment before the acts.** An earlier run of
> this demo showed Act 5 making only *two* attempts. The cause was not the retry
> loop: the Java proxy's first TLS handshake and first class-loading pushed its
> first attempt out to 189ms, so the second one already cleared the wobble and
> the third was never needed. The fix is `warm_up()` — one `WARM-UP` payment
> against a healthy provider, run after startup and again after the swap, so
> neither act below is the first request its proxy has ever made. Both proxies
> get the same treatment. It is worth knowing in its own right: **the first
> request through a fresh JVM proxy is slower than every request after it**, and
> that is a real difference between a JVM beside your service and a few
> megabytes of C.

### Act 6 — a refusal is still final

An allowance of two attempts, and a provider unwell for 600ms.

```
    { "outcome": "refused", "reference": "ORD-4419", "service": "checkout",
      "note": "the account's 2-attempt allowance is spent" }

  what the provider itself recorded:
    attempt at     17ms   declined
    attempt at    251ms   declined
    attempt at    687ms   refused
    3 attempts, first to last: 670ms
```

The third attempt came back `429`, and the proxy stopped there rather than
waiting and asking again. Being able to *write* the waiting is not a licence to
become greedier; the Java proxy enforces the same rule nginx did, in one line:

```java
if (response.statusCode() == 429) {
    break;                       // a refusal is final, never retried
}
```

### Act 7 — the gap in the middle of a swap

`docker compose stop sidecar-java`. Nothing else is touched.

```
  bound to localhost:8081:  nothing

  a customer pays for a kettle:
    { "outcome": "no sidecar", "service": "checkout",
      "reached": "nothing -- http://localhost:8081 did not answer",
      "note": "ClosedChannelException" }

  the provider's own ledger:
    { "allowance": 12, "total": 0, "refused": 0, "byService": {},
      "arrivals": [], "firstToLastMillis": 0 }
```

The provider is healthy, the network is healthy, checkout is healthy, and the
payment failed instantly. **Zero attempts reached the provider**, because the
request never left the machine — so nothing in the provider's dashboards will
ever show that this happened, and nothing in yours will either unless you are
watching the service, not the supplier.

This is why a swap is a rollout and not an edit: start the new proxy before
stopping the old one, move one service at a time, and keep the old one
installable. Putting nginx back is the whole rollback, and the demo does it in
one command:

```
  bound to localhost:8081:  nginx
    { "outcome": "paid", "reference": "ORD-4421", "service": "checkout",
      "note": "arrived at 36ms", "receipt": "pay_ORD-4421", "amountPence": 3150 }
```

## What the swap actually cost

This is the part Tier 1 flatters, and the demo prints the correction:

```
    nginx configuration, comments stripped:   27 lines
    Java proxy, comments stripped:            112 lines
```

Tier 1 compares 22 lines of configuration with 40 of Java, because in one JVM
the Java proxy *is* a retry loop and nothing else — the surrounding program
already exists. Out here it does not. The 112 lines above are what a proxy has
to do before it can retry at all: bind a port, read a request, present a
certificate, hand an answer back, and decide what to trust.

The retry loop itself is still small. `forward()` is twenty-five of those lines,
and the sleep is one of them:

```java
if (attempt < MAX_ATTEMPTS) {
    Thread.sleep(backoff);
    backoff *= 2;                // 200ms, then 400ms
}
```

The other eighty-seven lines are what nginx was already doing for free — and
even at 112 lines this proxy is still missing an access log in the shop's
format, connection pooling, inbound TLS, header hygiene, and anybody publishing
security fixes for it while you sleep.

There is a second line on the bill that has nothing to do with source. Compare
[`javaproxy/Dockerfile`](javaproxy/Dockerfile) with
[`payments/Dockerfile`](payments/Dockerfile): the same four lines, and now a JVM
sits beside every service where a few megabytes of nginx used to. Add the warm-up
note from Act 5 to that, and the true cost of the swap is a JVM's memory, a JVM's
first-request latency, and a proxy you are now on the hook for.

The benefit is unchanged and it is worth restating plainly: **the same three
attempts, properly spaced, and a payment that goes through.** Whether that is
worth the bill is a decision about your supplier and your traffic, and this
project's job is to make sure you are looking at both columns when you make it.

## Where this is deliberately smaller than production

- **One service, not four.** §41 needs several to make the duplicated policy
  hurt. Here the policy already lives in one place, and the question is only
  which program enforces it.
- **The Java proxy trusts every certificate.** The provider's certificate is
  generated by `demo.sh` a few seconds earlier and signed by nobody, so the
  proxy installs a trust-all `SSLContext`. In production that becomes a trust
  store — and the point stands either way, which is that it goes *here*, once,
  and not into each service.
- **Single-threaded.** `HttpServer` is given a single-threaded executor so the
  arrival times in the transcript are not interleaved between concurrent
  payments. A real proxy needs a pool, and a pool is more of those 112 lines.
- **The provider is a Spring Boot application in a container**, not a payment
  provider. It exists to record arrival times and to be told when to be unwell.
- **No mesh, no control plane, no injection.** Swapping one proxy by hand is
  this project. Swapping every proxy in a fleet without touching a compose file
  is what a control plane is for, and §43 is where the pod takes over the
  placement.

## Files

| Path | What it is |
| --- | --- |
| [`javaproxy/`](javaproxy) | **The replacement.** One class, no dependencies. Read `forward()`. |
| [`sidecar/payments-sidecar.conf.template`](sidecar/payments-sidecar.conf.template) | §41's proxy configuration, mounted here unchanged. |
| [`docker-compose.yml`](docker-compose.yml) | Four containers, one shared network namespace, and two things that want the same port. |
| [`payments/`](payments) | The service, with the concerns removed. It is not modified by any act. |
| [`gateway/`](gateway) | The provider: TLS 1.3, a timestamped ledger, and a wobble measured in milliseconds. |
| [`demo.sh`](demo.sh) | The seven acts, unattended. Generates the certificate and prints the transcript above. |
