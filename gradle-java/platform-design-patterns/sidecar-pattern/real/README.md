# Tier 2 — the proxy as a real process

Tier 1 makes every argument about the Sidecar pattern inside one JVM, and says
plainly that inside one JVM the structure is Decorator. This directory is where
the three claims that a JVM cannot demonstrate get demonstrated:

1. **The policy changes without the service being rebuilt or restarted.**
2. **The proxy is not written in Java, and the service does not care.**
3. **Killing the proxy takes every call with it, on a completely healthy network.**

Those three are the reasons to pay for a separate process. Nothing else is. If
none of them applies to your concern, a shared library inside your own process
is cheaper, faster, and has one fewer thing that can fail — and Tier 1 says so
in its last scene.

```bash
./demo.sh
```

Requires a JDK 21 and Docker. Tier 1 requires neither, which is why the two are
separate Gradle builds: the parent's `settings.gradle` does not include this one,
so `./gradlew test` one directory up never resolves Spring and still passes
offline.

## What is running

Five containers, and the count is a third of the lesson.

| Container | Image | What it is |
| --- | --- | --- |
| `sidecar-demo-gateway` | built from `gateway/` | The payment provider. HTTPS only, TLS 1.3 only. Counts every attempt it receives. |
| `sidecar-demo-checkout` | built from `payments/` | Checkout. Has no retry code, no TLS configuration and no provider address. |
| `sidecar-demo-checkout-proxy` | `nginx:1.31.5-alpine` | The proxy beside checkout. |
| `sidecar-demo-refunds` | built from `payments/` | Refunds. The same image as checkout, with a different name. |
| `sidecar-demo-refunds-proxy` | `nginx:1.31.5-alpine` | The proxy beside refunds, mounting **the same config file**. |

Two of the five are the shop. That is the third row of Tier 1's bill — four
copies became one, and four processes became eight — made literal.

### The one line in `docker-compose.yml` that matters

```yaml
sidecar-checkout:
  image: nginx:1.31.5-alpine
  network_mode: "service:checkout"
```

`network_mode: "service:checkout"` puts the proxy inside the service's network
namespace. The two containers then share one network stack and one set of ports,
which is why the payments service can be configured with `http://localhost:8081`
and mean it. It is also the closest thing Compose has to a Kubernetes Pod, which
is where §43 picks the story up.

One consequence is worth knowing before it confuses you: the proxy has no
network of its own, so it cannot publish a port. Both `8080` (the service) and
`8081` (the proxy) are published by the **service's** entry in the compose file.

## The most important file in the repository

[`sidecar/payments-sidecar.conf.template`](sidecar/payments-sidecar.conf.template).
Everything Tier 1 argues in nineteen Java classes is written down there in about
twenty lines of somebody else's language, and all four of Tier 1's concerns
appear in it by name:

```nginx
proxy_next_upstream error timeout http_503 non_idempotent;   # how many times to try
proxy_next_upstream_tries 3;

proxy_connect_timeout 2s;                                    # when to give up
proxy_read_timeout 2s;

proxy_ssl_protocols TLSv1.3;                                 # what to present
proxy_ssl_server_name on;

proxy_set_header X-Service ${SERVICE_NAME};                  # who is calling
```

There is one copy of that file on disk, and both proxies mount it.

### Four things about nginx that cost this project a run each

**Retrying needs more than one server.** `proxy_next_upstream` moves to the
*next server in the group*. With a single `server` line there is no next one, and
nginx never retries however high you set `proxy_next_upstream_tries`. The upstream
block therefore lists the same address three times, which is how "up to three
attempts" is spelled when the upstream is one address.

**`max_fails=0` matters.** Without it, nginx counts the declines itself, decides
the provider is unhealthy, and starts failing payments before they leave the
machine — a circuit breaker nobody asked for, arriving as a side effect of a
retry policy.

**nginx will not retry a POST unless you say `non_idempotent`.** That default is
correct: a POST that timed out may well have been processed. Writing
`non_idempotent` is a statement that the provider treats a repeated reference as
one charge, which is a promise about the supplier's contract rather than a
setting — and it is the same promise the Idempotent Consumer pattern is about.

**`envsubst` will eat nginx's own variables.** The nginx image renders anything
in `/etc/nginx/templates` through `envsubst` before starting. Without
`NGINX_ENVSUBST_FILTER: SERVICE_NAME` in the compose file, `$upstream_status`,
`$request_time` and the rest are substituted with empty strings, and the access
log comes out blank with nothing complaining anywhere.

### What nginx cannot do here, stated rather than hidden

Tier 1's policy includes a **backoff** — wait 200ms, then wait again — and nginx
has no delay between retries. `proxy_next_upstream_timeout` caps the total time
across all attempts, which is the deadline, but the gap between attempt one and
attempt two is zero. A proxy that needs real backoff is a proxy that has to be
written, which is exactly what §42 does. The figures in this demo's transcript
are therefore *faster* than Tier 1's, and the difference is a missing feature
rather than a better implementation.

`proxy_ssl_verify` is off, because the provider's certificate is generated by
`demo.sh` a few seconds earlier and signed by nobody. In production that line
becomes `proxy_ssl_verify on` with a CA bundle beside it — and the point stands
either way, which is that it goes *here*, once, and not into each service.

## The transcript

Captured from a real run. Every figure below is the provider's own tally, not
the caller's, because a service cannot count the attempts a proxy made on its
behalf — not seeing them is the point of the pattern.

### Act 2 — what is left in the service

```
  checkout describes itself:
    {
        "service": "checkout",
        "talksTo": "http://localhost:8081",
        "knowsTheProviderAddress": false,
        "retryCode": "none -- see PaymentsController.pay",
        "startedAt": "2026-09-17T08:28:39.178Z",
        "upFor": "3s"
    }

  Every mention of retrying in the payments service, in full:
    PaymentsController.java:83:  out.put("retryCode", "none -- see PaymentsController.pay");
    PaymentsApplication.java:11:  * the retry policy, because the copies are what Tier 1 is about. Here the
    PaymentsApplication.java:16:  * retry, no backoff, no deadline, no certificate, no counter, and no address for
    PaymentsApplication.java:17:  * the payment provider. Search the source for "retry" and you will find this
```

Two comments and a field name.

### Act 4 — a healthy payment, and who spoke TLS

```
    {
        "outcome": "paid",
        "reference": "ORD-4417",
        "service": "checkout",
        "note": "attempt 1",
        "receipt": "pay_ORD-4417",
        "amountPence": 4799
    }

  the provider's own record:
    {
        "allowance": 12,
        "total": 1,
        "refused": 0,
        "byService": { "checkout": 1 },
        "transport": "TLSv1.3 (the caller presented a certificate)"
    }
```

The provider accepts TLS 1.3 and nothing else. The service that took this payment
sent plain HTTP to localhost and has no keystore, no trust store and no protocol
list anywhere in its configuration. **The transport is a concern it never learns
about**, which in Tier 1 was one of the sixteen copies.

### Act 5 — a retry the service never made

The provider is told to decline the first two attempts at any payment.

```
  the provider's own record:
    {
        "allowance": 12,
        "total": 6,
        "refused": 0,
        "byService": { "checkout": 3, "refunds": 3 },
        "transport": "TLSv1.3 (the caller presented a certificate)"
    }

  what checkout's proxy logged, one line per attempt:
    checkout  172.20.0.2:9443  status=200  took=0.021  total=0.023
    checkout  172.20.0.2:9443, 172.20.0.2:9443, 172.20.0.2:9443  status=503, 503, 200  took=0.001, 0.009, 0.009  total=0.020
```

That second log line is the pattern in one line of text. Three upstream
addresses, three statuses, one request. The service made one call and got one
answer.

### Act 6 — the claim a JVM cannot make

One line of one file changes: `proxy_next_upstream_tries 3` becomes `1`. The two
proxies restart. **Neither service is rebuilt, redeployed or restarted.**

```
    { "outcome": "declined", "reference": "ORD-4419", "service": "checkout",
      "note": "attempt 1 -- try again" }

  and the service containers, which were never touched:
    checkout started at 2026-09-17T08:28:39.145484751Z, now 2026-09-17T08:28:39.145484751Z
    refunds  started at 2026-09-17T08:28:39.115510793Z, now 2026-09-17T08:28:39.115510793Z
```

Same start timestamps before and after. In Tier 1's March, this identical change
was four pull requests, four reviews and four releases, and one of the four was
forgotten by a team that had no reason to know they were involved. Here it is one
edit, and there is no fourth place for it to miss.

### Act 7 — the second thing that can be down

`docker compose stop sidecar-checkout`. Nothing else is touched.

```
  checkout tries to take a payment:
    { "outcome": "no sidecar", "service": "checkout",
      "reached": "nothing -- http://localhost:8081 did not answer",
      "note": "ClosedChannelException" }

  refunds, whose own proxy is fine:
    { "outcome": "paid", "reference": "REF-3821", "service": "refunds",
      "note": "attempt 1", "receipt": "pay_REF-3821", "amountPence": 2250 }

  the provider's own record:
    { "allowance": 12, "total": 1, "refused": 0,
      "byService": { "refunds": 1 } }
```

The gateway is healthy. The network is healthy. Checkout is healthy. Checkout
cannot take a single payment, and **none of its attempts reached the provider**,
because the request never left the machine — and the service has no retry code to
fall back on, because we deleted it on purpose.

Starting the proxy again is the whole repair. That is both the consolation and
the warning: the failure is cheap to fix and total while it lasts.

## Where this is deliberately smaller than production

- **Two services, not four.** Tier 1 needs four to make the copies hurt; here the
  copies are already gone, and a third and fourth identical container would add
  starting time without adding a claim.
- **One image, started twice.** Checkout and refunds are the same jar with a
  different `SHOP_SERVICE_NAME`, because once the concerns have moved out there is
  genuinely nothing left to distinguish them in this demo.
- **No backoff**, as above. The one real feature gap, and it is nginx's.
- **The provider is a Spring Boot application in a container**, not a payment
  provider. It exists to count attempts and to be told when to decline.
- **No mesh, no control plane, no injection.** A mesh is this pattern applied to
  every service at once with something on top that configures them all; Tier 1's
  last act gives the arithmetic for deciding whether you want one.

## Files

| Path | What it is |
| --- | --- |
| [`sidecar/payments-sidecar.conf.template`](sidecar/payments-sidecar.conf.template) | **The policy.** One file, both proxies. |
| [`docker-compose.yml`](docker-compose.yml) | Five containers, and the shared network namespace. |
| [`payments/`](payments) | The service with the concerns removed. Read `PaymentsController.pay`. |
| [`gateway/`](gateway) | The provider: TLS 1.3, an attempt tally, and a wobble you can switch on. |
| [`demo.sh`](demo.sh) | The seven acts, unattended. Generates the certificate and captures the transcript. |
