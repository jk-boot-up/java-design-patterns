# Dependencies

This project uses NGINX, run in a container by Testcontainers, which the plain
Java version of Secure Gateway does not. Skipping it loses none of the
pattern: the plain version teaches all of it with nothing installed.

## What NGINX is

NGINX is a web server and reverse proxy. A location block matches request paths; = means exactly, ~ means a regular expression; the most specific match wins, and location / catches everything else. proxy_pass forwards a request to another server. proxy_set_header sets a header on the forwarded request; an empty value removes it. limit_except GET allows only GET, and HEAD, inside a location, refusing others with 403. client_max_body_size refuses larger request bodies with 413. NGINX normalises a path, resolving dot-dot, before matching locations.

## What Testcontainers is

Testcontainers starts the NGINX container from inside the program, copies the configuration file into it, and lets it reach the order service running on this machine.

## Why this project uses them

The plain version shows the idea in Java. This version shows that in
practice the gatekeeper is usually standard infrastructure, and its policy a
short configuration file.

## What to install

Only a JDK, version 21, and a running Docker. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Java | 21 |
| Docker | running; 24 or later |
| NGINX image | nginx:1.31.6-alpine |
| Testcontainers | 2.0.5 |

## What it costs

- A container runtime, and a first run that downloads the NGINX image.
- A configuration file to review whenever an endpoint is added.
