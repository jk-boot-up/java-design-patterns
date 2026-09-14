# Prerequisites

This is the first project in the microservices category, and it is the gentlest of
the twelve. If you have done any of the Gang of Four projects in this repository
you have enough.

## Knowledge Prerequisites

### Required

- **Java basics.** Classes, interfaces, `try`/`catch`, generics used (not
  written), and `List`.
- **Records.** `ProductPage`, `Product` and `Money` are records. If you have not
  met them, a record is a class whose fields are final and whose constructor,
  accessors, `equals` and `hashCode` are written for you.
- **The idea that a program can be split into services.** Not how to deploy them.
  Just the idea that Pricing and Catalog might be separate programs, run by
  separate people, reachable over a network.

### Helpful, but explained as we go

- **The Facade pattern** (`structural/facade-pattern`). A gateway is very close
  to a facade, and the explainer spends a section on exactly where they differ. You
  will get more out of that section if you have seen a facade, but it is written
  so you do not have to have.
- **Method references.** `new CatalogService()::product` appears in
  `StoreServices`. It means "the `product` method of this object, as a function".
- **Latency intuition.** That a phone talking to a data centre is much slower than
  two machines in the same data centre talking to each other. The project puts
  real numbers on it, so you can take it on trust for now.

### Explicitly NOT required

- **Any infrastructure at all.** No Docker, no Kubernetes, no Spring Boot, no
  Kafka, no database, no cloud account, no HTTP client. This project starts
  nothing and opens no port. It runs offline on a laptop with a JDK.
- **Experience operating a distributed system.** This project teaches the shape of
  the pattern. It does not teach operations, and it says so plainly rather than
  letting you believe otherwise.
- **Networking knowledge.** Not TCP, not TLS, not DNS. A remote call here is a
  method call that costs simulated time and can be told to fail.

## A 60-Second "API Gateway" Primer

An API gateway is one service that sits in front of several others. A client calls
it once; it calls whatever it needs and returns a single answer shaped for the
client's screen.

The reason it is worth a whole service is that the client is usually far away and
the services are usually near each other. Making one slow call and four fast ones
is much better than making four slow ones. Along the way the gateway becomes the
natural place for anything every request needs — checking who is asking, most
obviously — and the natural place to know which of the services behind it actually
matter.

The one rule: a gateway routes, aggregates and protects. It does not decide
business questions. The moment it starts setting prices or judging whether an order
is allowed, it owns rules about data it does not own, and it becomes the hardest
thing in the system to change.

## A 60-Second "Simulated Network" Primer

There is no network in this project. Three small classes stand in for one.

`SimulatedClock` is the clock. It only moves when something moves it, so "this
call took two hundred milliseconds" is a number added to a counter rather than two
hundred milliseconds of your life. That is why the whole test suite finishes in
well under a second and why no test calls `Thread.sleep`.

`RemoteCall` is one endpoint. It knows how slow its link is, advances the clock by
that much, writes a line into the log, and returns an answer — or throws, if it has
been told to. `failNext(2)` means "fail the next two calls, then behave", which is
how a test can assert what the pattern did rather than what chance did.

`CallLog` is the timeline. It is the output of the demo, because both versions of
the app return the identical product page and the only way to tell them apart is to
look at what each one spent getting it.

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
cd micro-services-design-patterns/api-gateway-pattern
./gradlew test         # expect BUILD SUCCESSFUL, 25 tests
./gradlew run          # expect four timelines
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

**The demo's third act prints "no page"** — that is correct. Act three is the
version without a gateway losing a whole product page because an optional service
failed. It is meant to look like that.

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — why four calls from a phone
   is a problem, with the numbers
2. Run `./gradlew run` and read the four timelines
3. [`api-gateway-pattern-explained.md`](api-gateway-pattern-explained.md) — the
   pattern, starting from a hotel reception desk
4. [`class-diagram.md`](class-diagram.md) and
   [`uml-diagram.md`](uml-diagram.md) — the structure, then the sequences
5. [`animation.html`](animation.html) — the timeline one call at a time
6. The tests, which are the specification: `ProductPageGatewayTest` first
