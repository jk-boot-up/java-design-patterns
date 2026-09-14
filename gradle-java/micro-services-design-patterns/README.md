# Microservices Patterns

Twelve patterns for systems that are more than one program, taught the same way
as the twenty-five Gang of Four patterns in this repository: one self-contained
Gradle Java 21 project each, in the same online-store domain, with runnable
code, tests, written notes, diagrams, an animated walkthrough and a narrated
video.

**Status: specified, not yet built.** The two documents below fix what the
projects are before any of them is written.

- [`docs/spec.md`](docs/spec.md) — the scenario each pattern is taught through,
  why it fits, the naive alternative it must show failing, and the honest cost
  it must admit to.
- [`docs/implementation-plan.md`](docs/implementation-plan.md) — the order the
  twelve get built in, and the rules that keep the build from having to redo
  itself.

## The twelve

| # | Pattern | Scenario |
| --- | --- | --- |
| 1 | API Gateway | One front door for the storefront |
| 2 | Service Registry and Discovery | Finding a live Pricing instance |
| 3 | Client-Side Load Balancing | Spreading catalog reads across instances |
| 4 | Retry with Backoff | A flaky payment gateway |
| 5 | Circuit Breaker | When Recommendations stops answering |
| 6 | Bulkhead | A slow supplier feed starving checkout |
| 7 | Database per Service | Orders and Catalog stop sharing tables |
| 8 | API Composition | Assembling the order details page |
| 9 | CQRS | Order history without the joins |
| 10 | Saga | Placing an order across four services |
| 11 | Transactional Outbox | Never losing the order event |
| 12 | Idempotent Consumer | The duplicate `OrderPlaced` |

They are in learning order, and it runs in three movements: how a call reaches a
service at all (1–3), what to do when that call fails (4–6), and the genuinely
hard part — state split across services that cannot share a transaction (7–12).

## One JVM, no infrastructure

Every project runs with `./gradlew run` on a machine with nothing installed but
a JDK, offline. No Docker, no Spring, no Kafka, no database, no HTTP port. A
service is a plain class behind an interface, and a remote call is a method call
through a small harness that can be told to be slow, to fail, or to fail
intermittently.

That is a deliberate trade, and the projects say so rather than hiding it. What
you learn is the pattern's shape — what objects exist, what each decides, what
the failure path looks like in code — which is the same whether the call
underneath is a method call or an HTTP request. What you do not learn is
operating a distributed system. A reader who finishes all twelve knows what a
circuit breaker is and could write one; they have not run one in production.

## Prerequisites

These are harder than the Gang of Four projects and assume them. Before starting
here, be comfortable with
[Strategy](../behavioural/strategy-pattern),
[Observer](../behavioural/observer-pattern),
[Command](../behavioural/command-pattern),
[Decorator](../structural/decorator-pattern),
[Proxy](../structural/proxy-pattern) and
[Facade](../structural/facade-pattern) — each of the twelve leans on at least
one of them, and several exist mainly to show a familiar pattern doing its work
one process boundary further out.
