# Dependencies

This project uses Envoy, which the hand-built projects do not. This page says what it is, why it is here, and what it costs. It comes before the first line of framework code on purpose.

**Skipping this project loses none of the pattern.** [Service Mesh](../service-mesh-pattern) teaches all of it with plain Java.

## What Envoy is

Envoy is a high-performance proxy, made at Lyft, and the data plane of Istio and several other meshes. Its behaviour is set by a configuration: listeners, routes, clusters and filters. It serves its own counters on an admin port.

## Why this project uses it

Envoy is the real thing under most meshes. Its retries, its refusals and its counters are real, and so is the configuration that sets them.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Docker | running; 24 or later |
| Envoy image | `envoyproxy/envoy:v1.37-latest` |

The demo runs the container as `patterns-envoy`, and removes it at the end. The payment service is a Java HTTP server on this machine, reached from the container as `host.docker.internal`.

## What it costs

The first run pulls the image, about 180 megabytes. The demo takes about half a minute, because Envoy is restarted with a new configuration in three of the acts.

## Where this pattern lives

In Envoy's `retry_policy`, in its RBAC filter, and in its `/stats` admin page. A full mesh generates this configuration for you, from higher-level settings.
