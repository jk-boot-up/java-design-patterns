# Prerequisites

This is the second project in the microservices category. It needs nothing that
the API Gateway project did not, and it can be read first if you prefer — nothing
here depends on having seen a gateway.

## Knowledge Prerequisites

### Required

- **Java basics.** Classes, `try`/`catch`, `for` over a `List`, generics used (not
  written).
- **Records.** `ServiceInstance` and `Money` are records, and `Lease` is a private
  record inside the registry. A record is a class whose fields are final and whose
  constructor, accessors, `equals` and `hashCode` are written for you.
- **`Map` and `List`.** The registry is a `LinkedHashMap` with a rule attached.
  Understanding that the map keeps insertion order is enough.
- **The idea that a program can run as several copies.** Not how to start them.
  Just the idea that Pricing might be the same program running three times, and
  that any of the three can answer.

### Helpful, but explained as we go

- **What a timestamp comparison is for.** The single line
  `clock.millis() - lease.lastHeartbeatAt() > LEASE_MILLIS` is the heart of this
  project. If that shape is familiar you will spot it immediately; if not, it is
  walked through line by line.
- **Exception handling as control flow.** The discovering client catches a failure
  and *carries on* rather than reporting it. That is unusual enough to be worth
  noticing, and it is the reason the pattern works at all.
- **Having once been on call when a deployment took something down.** Not
  required. It does make the first act of the demo land harder.

### Explicitly NOT required

- **Any infrastructure at all.** No Docker, no Kubernetes, no Consul, no Eureka,
  no Spring Cloud, no service mesh, no cloud account. This project starts nothing
  and opens no port. It runs offline on a laptop with a JDK.
- **DNS knowledge.** DNS is mentioned once, as a comparison. You do not need to
  know how it resolves anything.
- **Threads.** There is no background thread expiring leases. Expiry happens when
  somebody asks, which is both simpler to read and — as it turns out — how several
  real registries behave.
- **Experience operating a distributed system.** This project teaches the shape of
  the pattern. It does not teach operations, and it says so plainly rather than
  letting you believe otherwise.

## A 60-Second "Service Discovery" Primer

A service that matters usually runs as more than one copy, and the set of copies
changes — every deployment, every autoscaling event, every crash. A caller needs an
address, and the addresses keep moving.

Service discovery replaces the written-down address with a question. There is a
shared list of who is running; instances put themselves on it when they start and
take themselves off when they stop; and callers ask the list instead of holding a
constant.

The part people skip is that the list is sometimes wrong. A process that crashes
cannot send a message saying it has crashed, so for a few seconds the list will
happily hand out a dead address. That is why registrations expire — and why a
discovering client must be prepared to try the next name rather than trusting the
first.

## A 60-Second "Lease" Primer

A lease is permission with an expiry date. In this project a registration is good
for `LEASE_MILLIS`, which is three seconds, counted from the last heartbeat.

An instance renews its lease by sending a heartbeat. Renewing is cheap — one
message — and forgetting is fatal, in the sense that the instance disappears from
the list. That asymmetry is the whole design: the registry does not have to detect
death, it only has to notice silence, and silence is what a dead process is
extremely good at producing.

Read `ServiceRegistry.instances(...)` with that in mind. It walks the leases, drops
the ones whose last heartbeat is older than the lease, logs each drop as `EXPIRED`,
and returns the rest. Expiry is lazy: it happens at lookup time rather than on a
timer, so nothing in this project needs a clock that ticks by itself.

## A 60-Second "Simulated Network" Primer

There is no network in this project. Four small classes stand in for one.

`SimulatedClock` is the clock. It only moves when something moves it, so "four
seconds later" is a number added to a counter rather than four seconds of your
life. That is why the whole test suite finishes in well under a second, and why no
test calls `Thread.sleep` — including the tests about a three-second lease.

`RemoteCall` is one endpoint. It knows how slow its link is, advances the clock by
that much, writes a line into the log, and returns an answer — or throws, if the
instance behind it is no longer running.

`CallLog` is the timeline. It is the output of the demo, because the price comes
back as `£449.99` either way and the only way to see what discovery did for you is
to read what happened on the way.

`Money` holds pence as a `long`, so no price in this repository is ever a `double`.

## Software Prerequisites

- **JDK 21 or newer.** Nothing else.
- **Gradle:** not needed globally. The project ships a wrapper.

### Installing JDK 21

macOS, with Homebrew:

```bash
brew install openjdk@21
sudo ln -sfn $(brew --prefix)/opt/openjdk@21/libexec/openjdk.jdk \
    /Library/Java/JavaVirtualMachines/openjdk-21.jdk
```

Linux (Debian or Ubuntu):

```bash
sudo apt install openjdk-21-jdk
```

Windows: install the Microsoft Build of OpenJDK 21 or Temurin 21 from the
installer, and let it set `JAVA_HOME`.

### Verify Your Setup

```bash
java -version          # expect 21 or newer
cd micro-services-design-patterns/service-discovery-pattern
./gradlew test         # expect BUILD SUCCESSFUL, 19 tests
./gradlew run          # expect four acts
```

If `./gradlew` will not execute on macOS or Linux, make it executable:

```bash
chmod +x gradlew
```

The first `./gradlew` command downloads Gradle itself and needs a network
connection. Everything after that works offline, including the demo — because the
demo has no network to use.

## Troubleshooting

**"Unsupported class file major version"** — Gradle is using an older JDK than the
toolchain asks for. Check `java -version`, and set `JAVA_HOME` to a 21 install.

**The pound sign prints as a question mark or a box** — your terminal is not using
UTF-8. On Linux, `export LANG=en_GB.UTF-8`. The prices in the output are in pounds
and the demo is a London shop.

**Act one prints "pricing-1 did not answer"** — that is correct and it is the point
of act one. The hardcoded client has just been taken down by an ordinary
deployment, while two healthy instances sit idle.

**Act three logs `STALE` and then succeeds** — also correct. The registry handed
out a dead address, the client noticed, and it tried the next one. If that line
ever stops appearing, the demo has stopped teaching the harder half of the pattern.

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — why a constant address is a
   time bomb, with the deployment that sets it off
2. Run `./gradlew run` and read the four acts, in order
3. [`service-discovery-pattern-explained.md`](service-discovery-pattern-explained.md)
   — the pattern, starting from a taxi rank
4. [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md) —
   the structure, then the four sequences
5. [`animation.html`](animation.html) — the registry changing its mind, one step at
   a time
6. The tests, which are the specification: `ServiceRegistryTest` first, then
   `HardcodedPricingClientTest` to see the failure pinned down
