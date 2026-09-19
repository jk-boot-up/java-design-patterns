# Feature Toggle with flagd, Explained

## The pattern in one sentence

With flagd, a flag is an entry in a file that a daemon watches, and the application asks the daemon whether a flag is on for a customer.

## What is new here

The pattern is [Feature Toggle](../feature-toggle-pattern). This page is only what flagd and OpenFeature adds.

### Deploying Is Releasing

Gift wrap goes live by deploying it: one deploy. It has a bug, so taking it away is another: two deploys. Each deploy ships every other change waiting in the branch too.

```
  gift wrap goes live by deploying it: 1 deploy. it has a bug, so taking it away is another: 2 deploys.
  each deploy ships every other change waiting in the branch too.
```

### Deploy Dark, Switch Later

Gift wrap is in the deployed code, and flagd has it off. An order of five thousand costs five thousand. The flags file is edited, and flagd notices by itself: no deploy, no restart. The same order costs fifty three hundred.

```
  gift wrap is in the deployed code, and flagd has it off. an order of 5000 costs: 5000.
  the flags file was edited, and flagd noticed by itself. no deploy, no restart. the same order costs: 5300.
```

### Switch On For Some

A ten percent rollout, decided by flagd's own hash of the customer. Of a hundred customers, about a tenth got it. Then only two named testers: of a hundred customers, two got it.

```
  a 10 percent rollout, decided by flagd's own hash of the customer. of 100 customers, got it: about a tenth.
  only two named testers. of 100 customers, got it: 2.
```

### The Kill Switch

Gift wrap has a bug. With twenty percent on, about a fifth of a hundred orders failed. One edit to the file turned it off. Of a hundred orders, none failed. No deploy.

```
  gift wrap has a bug. with 20 percent on, some of 100 orders failed: yes, about a fifth.
  one edit to the file turned it off. of 100 orders, failed: 0. no deploy.
```

### When flagd Cannot Be Reached

Flagd is up, and an order of five thousand costs fifty three hundred. Flagd is stopped, and it costs five thousand. The order still works, and every feature falls back to off.

```
  flagd is up. an order of 5000: 5300.
  flagd is stopped. an order of 5000: 5000. the order still works, and every feature falls back to off.
```

### The Bill

A shop with five flags would have thirty two possible combinations. The tests usually run one. Flagd is another process to run and keep up, and every flag check is a network call: this demo made hundreds. And a flag that is settled and still in the file is an if that nobody needs. Flagd does not remove it for you.

```
  this file has one real flag. a shop with 5 flags like it would have 32 possible combinations. the tests usually run one.
  flagd is another process to run and keep up, and every flag check is a network call: this demo made hundreds.
  and a flag that is settled and still in the file is an if that nobody needs. flagd does not remove it for you.
```

## The verdict

Keep flags in a file or service that a daemon serves, and change them there, not in code. Rollouts by hash are repeatable, so the same customers stay in. Decide what happens when the daemon is down: off is the safe answer. And remove settled flags.

## How to recognise this in code you did not write

- A `flags.json` with `variants`, `defaultVariant` and `targeting`.
- An OpenFeature client, `client.getBooleanValue(...)`.
- A `fractional` rule for a percentage rollout.
- A sidecar or daemon named flagd.

## Where you have already met this

Companies that use OpenFeature with LaunchDarkly, Flagsmith, Unleash or their own service.

## When this is too much

For a handful of switches that change with each release, a setting in the deployment is enough. A daemon adds a process and a network call to every check.
