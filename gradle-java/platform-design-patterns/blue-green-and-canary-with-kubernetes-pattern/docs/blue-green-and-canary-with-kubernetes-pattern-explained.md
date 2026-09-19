# Blue-Green and Canary with Kubernetes, Explained

## The pattern in one sentence

On Kubernetes, blue-green is a change of a Service's selector between two Deployments, and a canary is a change of their replica counts behind one Service.

## What is new here

The pattern is [Blue-Green and Canary](../blue-green-and-canary-pattern). This page is only what Kubernetes adds.

### Replace It Where It Stands

The first release is stopped to make room for the second. Twenty requests arrive while nothing is running, and all twenty fail.

```
  v1 stopped to make room for v2. 20 requests while nothing is running: failed 20 of 20.
```

### Blue And Green

Version two runs beside version one, and only a test port reaches it. The test request is answered by version two. Twenty requests before the switch are all answered by version one. The switch is one patch to the service. Twenty after are all answered by version two, and none failed.

```
  v2 is running beside v1, and only a test port reaches it. test request to v2: v2.
  20 requests before the switch: {v1=20}. the switch is one patch to the service. 20 after: {v2=20}, failed 0.
```

### Going Back

Version two has a bug with big orders. Twenty big orders on version two: all twenty fail. One patch sends the service back to version one, whose pods never stopped. Twenty big orders: none fail.

```
  v2 has a bug with big orders. 20 big orders on v2, failed: 20.
  one patch sent the service back to v1, whose pods had never stopped. 20 big orders, failed: 0.
```

### A Canary

Nine pods of version one and one of version two, behind one service. Three hundred big orders: a few dozen failed, a small share, as a canary should be. The spread is chosen by the cluster's own rules, so the exact count changes from run to run. Had all three hundred gone to version two, all would have failed.

```
  9 pods of v1 and 1 of v2, behind one service. 300 big orders: failed 36, which is a small share, as a canary should be.
  the spread is chosen by the cluster's own rules, so the exact count changes from run to run.
  had all 300 gone to v2, all 300 would have failed. a few customers found the bug, not everyone.
```

### Promote In Steps, With A Gate

Steps of one, five and ten pods of version two, with a gate at five failures in a hundred. The buggy release is halted, and every pod is version one again. A first step with few requests can miss a bug, and the next step, with more traffic, catches it.

```
  the gate caught it at the first step.
  steps of 1, 5 and 10 pods of v2, and a gate at 5 failures in 100. buggy v2: halted true, and every pod is v1 again.
```

### The Bill

During a blue-green switch both releases are fully running: four pods, where one release needs two. Both share one database, so a release that changes the data cannot be switched back safely. And a cluster is a lot to run for a checkout.

```
  during a blue-green switch both releases are fully running: 4 pods, where one release needs 2.
  both releases share one database, so a release that changes the data cannot be switched back safely.
  and a cluster is a lot to run for a checkout: a control plane, a node, an image, a service and two deployments.
```

## The verdict

Release beside the old version. On Kubernetes, switch with a selector and go back with the same. Use replica counts for a canary, with a gate on failures and enough traffic per step. Automate it with a rollout tool, and keep data changes compatible in both directions.

## How to recognise this in code you did not write

- A Service whose `selector` includes a `version` label.
- Two Deployments of one app, with different `version` labels.
- Argo Rollouts or Flagger objects.
- `kubectl rollout` and `kubectl scale` in a release script.

## Where you have already met this

Kubernetes platforms and their release tools.

## When this is too much

For an internal tool where a short outage is fine, a plain restart is enough, and a cluster is a lot to run for one service.
