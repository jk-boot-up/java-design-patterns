# Dependencies

This project uses Kubernetes, which the hand-built projects do not. This page says what it is, why it is here, and what it costs. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [Blue-Green and Canary](../blue-green-and-canary-pattern) teaches all of it with plain Java.

## What Kubernetes is

Kubernetes runs containers in pods, keeps the number you ask for, and puts a Service in front of them that chooses pods by label. kind runs a real Kubernetes cluster as a Docker container, so a laptop can have one.

## Why this project uses it

On Kubernetes the switch, the replica counts and the gap while a release is replaced are real, so the pattern can be seen doing its real work.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Docker | running; 24 or later |
| kind | 0.33 or later, `brew install kind` |
| kubectl | 1.30 or later |
| nginx image | `nginx:alpine`, pulled once, and loaded into the cluster |

The demo creates a cluster named `patterns-bg`, and deletes it at the end. Set `KEEP_CLUSTER=1` to keep it.

## What it costs

The first run pulls the node image, about a gigabyte. The demo takes about a minute and a half. A cluster uses a few hundred megabytes of memory while it runs.

## Where this pattern lives

In a Service's `selector`, in a Deployment's `replicas`, and in tools such as Argo Rollouts, Flagger and the service meshes that automate them.
