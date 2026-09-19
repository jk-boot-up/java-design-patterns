# Sidecar on Kubernetes, Explained

## The pattern in one sentence

A Pod is two or more containers that share one network namespace and one fate, which is exactly what a
sidecar needs.

## An analogy, and then back to the shop

Two flatmates who share a phone line have agreed to it. Either can ring the other from the hall, but only
because they set it up, and if one moves out the line stays. Now think of a couple who share a flat.
Nobody set anything up: they have one address, one front door, and one lease. If the flat is given up,
both leave together. That is the difference between two containers in a Compose file and two containers in
a Pod. The first is an agreement. The second is what a Pod is.

## Four things a Pod guarantees

**1. A shared network, by definition.**

```
ONE. Shared by configuration, or shared by definition.
  a Pod: checkout reaches localhost:8081: true. there is no line to forget.
  both containers are on 10.244.0.10, one network, because that is what a Pod is.
```

**2. A shared lifecycle.** The Pod is scheduled, evicted and deleted as one unit.

```
TWO. One lifecycle.
  Compose: checkout stopped. the proxy is still running: true.
  Pod: deleted. checkout running: false, proxy running: false. they go together.
  the replacement is a new Pod on a new address (10.244.0.10 became 10.244.0.11), with both containers new.
```

**3. A correction worth making: restarts are per container.** It is tempting to say a crash in one
container takes its neighbour with it. It does not. The kubelet restarts each crashed container on its own.

```
THREE. Restarts, however, are per container.
  the proxy's process dies. the Pod is 1/2. a payment now: connection refused on localhost:8081
  the kubelet restarts the proxy alone. Pod 2/2, proxy restarts 1, checkout restarts 0.
```

What is shared is the Pod: scheduling, eviction and deletion, not process death. While the proxy is down the
service's calls fail, exactly as in [`sidecar-pattern`](../sidecar-pattern)'s "kill the proxy" act, and then
they recover without anyone touching the service.

**4. Injection.** The sidecar arrives beside a service whose own manifest does not mention it.

```
FOUR. Injection.
  the manifest the refunds team wrote lists 1 container: [refunds]
  the Pod that was created lists 2: [refunds, sidecar-proxy]
```

That is the mechanism every service mesh is built on: an admission step adds a proxy to every Pod as it is
created, and no team wrote it. This project does the same by hand; a real mutating webhook is named and not
built.

## `READY 2/2`, and the start-up race

`kubectl get pods` prints `2/2` for one logical service made of two containers. With the proxy down it
prints `1/2`, and the Pod stops receiving traffic. Containers started together also leave a race: the service
can start, and call the proxy, before the proxy is listening. A **native sidecar**, an init container with
`restartPolicy: Always`, is started first and must be running before the service starts.

```
FIVE. READY 2/2, and the start-up race.
  containers started together, in manifest order: [checkout, sidecar-proxy].
  a native sidecar starts first: [sidecar-proxy, checkout]. the ordering problem is gone.
```

## The bill, and the honest question

Everything Compose cost, plus a cluster: a scheduler, a control plane, a YAML dialect and a networking model,
added to a shop that worked with two containers and a file. For a fleet that is a bargain. For four services
it is the reason "do you need Kubernetes yet?" is a real question, and for four services the honest answer is
almost certainly not. This project answers it rather than selling the cluster.

## What this simulation does not show

Tier 1 is a model. It has no scheduler deciding which node, no etcd, no network partitions, and no restart
back-off: a real kubelet waits longer between each restart of a container that keeps crashing. Tier 2 runs the
same two containers on a real cluster and closes most of that gap. It does not close all of it: one laptop
running `kind` is not a fleet, and its control plane is one container that does not fail.

## Where you have already met this

Every Pod in every cluster, and the proxy a service mesh injects beside your service.

## When this is too much

For four services, or one team, Compose is cheaper, faster to start, and has fewer ways to fail.
