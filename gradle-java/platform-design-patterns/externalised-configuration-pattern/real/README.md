# Tier 2 — the same pattern, with Spring Cloud Config

Tier 1, one directory up, is plain Java with no framework and no network. It is
the lesson. This directory is the same pattern as a real deployment writes it:
two Spring Boot services, a value that lives in neither of them, and a change
that reaches production in one HTTP request.

**Read Tier 1 first.** Nothing here re-explains what externalised configuration
is or why the constant had to move. This directory answers a narrower question:
what does the pattern look like when a framework already implements most of it,
and — more usefully — *which part does the framework not implement?*

Everything below is captured output from `./demo.sh`. Nothing in this file is
written from memory.

## Run it

```
./demo.sh
```

A JDK 21, and a network connection the first time so Gradle can fetch Spring.
The script starts both services, walks the whole sequence, and stops them
again. It takes about a minute.

Tier 1 needs neither the network nor this directory. That asymmetry is why the
two are separate Gradle builds: `real/settings.gradle` is a build of its own and
the parent does not include it, so `../gradlew test` never tries to resolve
Spring and passes offline.

## The two services

| Service | Port | What it is |
| --- | --- | --- |
| `config-server` | 8888 | Tier 1's `ConfigSource`, as a process. One annotation, `@EnableConfigServer`; everything else is YAML |
| `checkout-service` | 8080 | Tier 1's `ConfiguredCheckout`, with an HTTP door on it |

The value itself is in `config-repo/checkout-service.yml`, which belongs to
neither service. The file name is the lookup key: Spring Cloud Config matches it
to the client's `spring.application.name`.

This demo uses the **native** (directory) backend rather than a git one. Git is
what a real deployment uses and it is what gives you the audit trail Tier 1 had
to build by hand as `ChangeLog`. Swapping to it is two lines of YAML and nothing
downstream changes. A directory is used here because a reader can open it in an
editor and see the pattern in one step, instead of creating a repository first.

## What the config server serves

```json
{
    "name": "checkout-service",
    "profiles": ["default"],
    "propertySources": [
        {
            "name": "file:config-repo/checkout-service.yml",
            "source": {
                "delivery.freeOver": 50.0,
                "delivery.standard": 4.99
            }
        }
    ]
}
```

## A quote, at the threshold of £50.00

A basket of forty-eight pounds does not reach fifty, so delivery is charged.

```json
{
    "goodsTotal": "£48.00",
    "freeDeliveryOver": "£50.00",
    "deliveryCost": "£4.99",
    "total": "£52.99",
    "thresholdState": "in force",
    "thresholdOrigin": "configserver:file:config-repo/checkout-service.yml"
}
```

`thresholdOrigin` is not decoration. The first question anybody asks about a
surprising number in production is where it came from, and a service that has
moved the value out of the code without moving the explanation with it cannot
answer. It names the property source that actually supplied the key, so an
environment variable quietly overriding the config server shows up here rather
than in an incident.

## The change

Edit one line of `config-repo/checkout-service.yml` to `freeOver: 35.00`, then:

```
curl -X POST http://localhost:8080/actuator/refresh
["delivery.freeOver"]
```

The response is the list of keys that changed. The same basket, asked again:

```json
{
    "goodsTotal": "£48.00",
    "freeDeliveryOver": "£35.00",
    "deliveryCost": "£0.00",
    "total": "£48.00",
    "thresholdState": "in force"
}
```

Same process, same build, same uptime, and delivery is now free. No compile, no
artefact, no deployment, no restart. In Tier 1 the release pipeline that would
otherwise have carried this change took two hours and fifteen minutes and put
it live two days late.

`@RefreshScope` on `DeliverySettings` is what makes it work. Without it the bean
is built once at startup and holds its value for the life of the process, which
is a constant that took a longer route to get there. With it, the bean is thrown
away and rebuilt on the next request after a refresh.

## The guard, and the thing Spring does not give you

This is the part worth the visit even if you already know Spring Cloud Config.

Set the threshold to `-1` and refresh. The value is outside the declared range —
`@DecimalMin("5.00")` and `@DecimalMax("200.00")` on `DeliverySettings` — so the
bind fails and the value never reaches the checkout.

```json
{
    "goodsTotal": "£48.00",
    "freeDeliveryOver": "£35.00",
    "deliveryCost": "£0.00",
    "thresholdState": "the configured value was rejected; trading on the last value that passed validation"
}
```

The shop is still trading, on the last value that passed. **That is not stock
behaviour, and the first version of this demo assumed it was.**

What a plain `@RefreshScope @Validated` bean actually does is this. The refresh
discards the bean. The next request asks for it, Spring rebuilds it, binds the
new value, runs validation, and validation fails — so *the request* fails. Then
the next one fails the same way, and every one after it. The bad value never
reaches a customer, which is the important half. But neither does anything else:
`/quote` returns 500 until somebody fixes the file. One mistyped number took the
shop down with no code deployed, which is exactly the risk the pattern is
supposed to be managing.

So a range check on its own is not the guard. The guard is the range check
**plus somewhere to fall back to**, and that second half is `LastGoodSettings` —
about thirty lines, a plain singleton so that it survives the refresh that
destroys the refresh-scoped bean. Any team that externalises a value and stops
at `@Validated` is missing it.

This is the Tier 1 lesson arriving at the same place by a different road. Tier 1
built `GuardedSettings` by hand and it was obvious that rejecting a change means
keeping the old one. With a framework doing the work it is not obvious at all,
because the framework does the visible half and leaves the other half to you.

## What the framework replaced, and what it did not

Tier 1's argument was that a constant gets four guards free — the compiler, a
reviewer, version control, and a revert — and that moving the value outside
throws all four away. Here is the same table, in Spring's terms.

| The guard a constant gave you | What buys it back here |
| --- | --- |
| The compiler rejects `"fifty"` where a number belongs | Binding to `BigDecimal`, which fails the refresh on a non-numeric value |
| A reviewer notices `-1` | `@DecimalMin` / `@DecimalMax`, plus `LastGoodSettings` so rejection is survivable |
| Version control records who changed it and when | The git backend, in a real deployment. **Not this demo** — the native backend has no history, and that is its one honest cost |
| A revert is as fast as the change | A revert is the same one-line edit and the same refresh |

Three of four come from the framework. The fourth is a deployment decision, and
the native backend used here does not make it. That row is the reason the config
repository is a git repository in production rather than a directory.

## What is not here

- **Authentication.** `/actuator/refresh` is a write operation that changes
  prices, and it is wide open on port 8080. In a real deployment both actuator
  endpoints sit behind authentication.
- **Automatic refresh.** The refresh is triggered by hand. Spring Cloud Bus can
  broadcast it to every instance, which is what you want with more than one
  replica, and it is a whole subject of its own.
- **Encryption.** Config Server can serve encrypted values. A delivery threshold
  is not a secret, so this demo does not need it.

Each of these is left out because it would cost a reader time without teaching
the pattern, not because a real deployment can do without them.

## Versions

Everything is pinned in
[`../../gradle/libs.versions.toml`](../../gradle/libs.versions.toml) and
explained in [`../../docs/pinned-versions.md`](../../docs/pinned-versions.md).
Spring Boot 4.1.1, Spring Cloud 2025.1.3. No ranges, no `latest`.
