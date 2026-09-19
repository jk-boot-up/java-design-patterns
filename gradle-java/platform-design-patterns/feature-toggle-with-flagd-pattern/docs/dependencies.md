# Dependencies

This project uses flagd and OpenFeature, which the hand-built projects do not. This page says what it is, why it is here, and what it costs. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [Feature Toggle](../feature-toggle-pattern) teaches all of it with plain Java.

## What flagd and OpenFeature is

OpenFeature is a vendor-neutral standard for evaluating feature flags. flagd is its reference daemon: it reads flag definitions from a file or a URL, watches for changes, evaluates targeting rules, including fractional rollouts, and answers over gRPC and HTTP.

## Why this project uses it

The flag is really read from a file by a real daemon, so the switch, the rollout and the fall back are real, and behind a standard interface that other flag services also offer.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Docker | running; 24 or later |
| flagd image | `ghcr.io/open-feature/flagd:latest`, built 2026-09-10 |

The demo runs the container as `patterns-flagd`, and removes it at the end. It mounts a temporary folder holding the flags file.

## What it costs

The first run pulls the image, about 110 megabytes. The demo takes about ten seconds. Every flag check is an HTTP call to the container.

## Where this pattern lives

In a flags file or a flag service, in the OpenFeature SDK of each language, and in the targeting rules that pick who gets a flag.
