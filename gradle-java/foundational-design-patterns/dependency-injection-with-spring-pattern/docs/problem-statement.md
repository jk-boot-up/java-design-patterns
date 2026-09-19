# Problem Statement

## Read the partner first

This project assumes [Dependency Injection](../dependency-injection-pattern), which builds the
wiring by hand and a container from scratch. Nothing here is lost by skipping Spring, and
[`dependencies.md`](dependencies.md) says so plainly.

## The scenario

The partner's: a checkout with a discount policy, a payment gateway and a notifier, and
the classes around it.

## What is new

`Wiring.build()` is gone. Every class carries `@Component`, and Spring builds the graph.

```
ONE. The same graph, with no wiring code.
  Wiring.build() is gone. Spring built the graph from the constructors.
  charged [9000], messages sent 3, exactly as by hand.
```

The constructors are the partner's, untouched. Spring reads their parameter types, as
`MiniContainer` did.

## What this project must deliver

Recognition: what each annotation replaced, Spring's real failures, and an honest account of
what it costs.
