# Problem Statement

## Read the first project first

This builds on [`sidecar-pattern`](../sidecar-pattern), which explains what a sidecar is, why the retry
code left the service, and what a second process costs. Nothing here re-teaches it. It takes the same
two containers, the checkout service and the proxy beside it, and asks one question: what changes when
Kubernetes runs them?

Nothing is lost by skipping Kubernetes. [`docs/dependencies.md`](docs/dependencies.md) says what it is,
what it costs, and how to skip it.

## The scenario

The shop's checkout service makes one payment call, to `localhost:8081`. Something else must be
listening there, and it must be running beside checkout, on the same network, for as long as checkout is.

## What Docker Compose gave you, and what it did not

In Compose, one line makes that true:

```
ONE. Shared by configuration, or shared by definition.
  Compose, with network_mode: service:checkout: checkout reaches localhost:8081: true
  Compose, with that one line forgotten:        checkout reaches localhost:8081: false
```

The sharing is configuration, and configuration can be forgotten. And each container has its own
lifecycle: stop one, and the other keeps running.

## What this project must deliver

Four things a Compose file can only approximate: a shared network by definition, a shared lifecycle,
injection, and `READY 2/2`. And an honest answer to whether you need any of it yet.
