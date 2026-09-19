# Blue-Green and Canary, Explained

## The pattern in one sentence

Blue-green runs the old and new release side by side and switches traffic at once. A canary sends a small share of traffic to the new release first, and grows it only while it stays healthy.

## The six acts

### Replace It Where It Stands

Stop version one, install version two, start version two. Ten requests arrive while it is down. Of a hundred requests, ten failed.

```
  stop v1, install v2, start v2: 10 requests arrive while it is down. of 100 requests, failed: 10.
```

### Blue And Green

Version two is started beside version one, and tried with a test order. It is fine. Version one served fifty requests meanwhile. The switch is one setting. After it, version two serves the next fifty. Of a hundred requests, none failed.

```
  v2 was started beside v1 and tried with a test order: ok. v1 served 50 requests meanwhile.
  the switch was one setting. after it v2 served 50. of 100 requests, failed: 0.
```

### Going Back

Version two has a bug with big orders. Fifty requests on version two, five failed. One setting sends traffic back to version one, which was never stopped. The next fifty requests, none failed.

```
  v2 has a bug with big orders. 50 requests on v2, failed: 5.
  one setting sent traffic back to v1, which had never been stopped. the next 50 requests, failed: 0.
```

### A Canary

Five percent of traffic goes to the buggy version two. Of two hundred requests, version two got ten, and failed two. Had all two hundred gone to version two, twenty would have failed. A few customers found the bug, not everyone.

```
  5% of traffic to the buggy v2. of 200 requests, v2 got 10 and failed 2.
  had all 200 gone to v2, 20 would have failed. a few customers found the bug, not everyone.
```

### Promote In Steps, With A Gate

Steps of five, twenty five, fifty and a hundred percent, with a gate at five percent failures. The buggy version two is halted after one step, with twenty percent failing, and traffic goes back to version one. The good version two goes through all four steps, and ends at a hundred percent.

```
  buggy v2: halted true after 1 step, failure rate on v2 20%, traffic back to 100% v1.
  good v2: halted false, steps 4, now at 100% v2.
```

### The Bill

Two full copies run during the switch: capacity twenty instead of ten. And version two wrote five orders in a new format before we went back. Version one can read none of them. Both releases share one database, so a release that changes the data cannot be switched back safely.

```
  two full copies run during the switch: capacity 20 instead of 10.
  v2 wrote 5 orders in a new format before we went back. v1 can read: 0.
  both releases share one database, so a release that changes the data cannot be switched back safely.
```

## The verdict

Release beside the old version, never on top of it. Switch by a setting, so that going back is a setting. Use a canary for risky changes, with a gate on failures. Keep data changes compatible in both directions, and pay for the extra capacity for the time it takes.

## How to recognise this in code you did not write

- Two deployments or target groups behind a load balancer.
- Traffic weights of 5, 25 and 100 percent.
- Argo Rollouts, Flagger, AWS CodeDeploy, Kubernetes with an Istio route.
- A rollout that pauses on an error-rate check.

## Where you have already met this

Almost every large web service's release process, and Kubernetes rollouts with a service mesh.

## When this is too much

For an internal tool where a short outage is fine, a plain restart is enough. These methods pay off where downtime or a bad release is costly.
