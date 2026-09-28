# Dependencies

This project uses NGINX and Testcontainers, which the plain-Java twin does not. This page says what they are, why they are here, and what they cost. It comes before the first line of NGINX configuration on purpose.

**Skipping this project loses none of the pattern.** The plain-Java Strangler Fig project in this course teaches all of it, with nothing installed.

## What NGINX is

NGINX is a web server that is very often used as a **reverse proxy**: a program that stands in front of other programs, takes every request the customer sends, and passes each one on to whichever program behind it should answer. The customer only ever sees NGINX's address.

Think of the reception desk in a large office building. Visitors never wander the corridors; they tell the receptionist who they want, and the receptionist sends them to the right floor. When a department moves floors, the receptionist gets a new list, and the visitors never notice. But the receptionist reads the list by rules of their own — perhaps an old sticky note on the desk beats the new list — and that is where the surprises live.

In NGINX's words, each entry on the list is a **location** block. A location matches the start of a web address, called a **prefix**, such as `/api/prices/`, or a **regular expression**, a pattern written with symbols such as `^/api/(prices|stock)/`, marked with a `~`. NGINX finds the longest matching prefix, then tries the regular expressions in order, and the first one that matches wins. A prefix marked **`^~`** tells NGINX to stop looking once it matches. **`proxy_pass`** says where to send the request; a named group of addresses it can send to is an **upstream**, here `old_shop` and `new_service`. **`nginx -s reload`** tells NGINX to read its configuration again. NGINX's **main process** reads the configuration; its **worker processes** handle the requests. **502 Bad Gateway** is the answer NGINX gives when the program behind it does not answer.

## What Testcontainers is

Testcontainers is a Java library that starts a container from inside your program and stops it again when you are done. It is here so that the demo owns NGINX's lifetime: `./gradlew run` brings NGINX up, uses it, and takes it away at the end. It maps NGINX's port to a free random port on your machine, so this demo can run beside anything else. And because the two shop services run on your machine, not in a container, Testcontainers opens a way from the container back to them: NGINX reaches them by the name `host.testcontainers.internal`. The 2.x line has no dedicated NGINX module, so the plain container type is used.

## Why this project uses them

Because the things this project teaches — which location wins, what one slash does to a path, what a reload does to a request in progress, what a real proxy answers when the service behind it is down — are NGINX's own behaviour. A router written in Java has none of them. The router has to be the real one.

## What to install

Only a JDK, version 21, and a container runtime. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Docker, or a Docker-compatible runtime | running; 24 or later |
| NGINX image | `nginx:1.31.6-alpine` |
| `org.testcontainers:testcontainers` | 2.0.5 |
| `org.slf4j:slf4j-simple` | 2.0.17 |

Every one of these is the newest generally available release; none is held back. NGINX publishes a mainline line and a stable line; 1.31.6 is the newest mainline, which NGINX recommends for most users, and the stable line was at 1.30.5. The Alpine variant of the image is used because it is the smallest.

## What it costs

The first run pulls the NGINX image, about 62 MB once unpacked. After that a run takes about eight seconds, most of it the container starting. Testcontainers also runs two small helper containers for the length of the run: one that carries NGINX's connections back to the two services on your machine, about 15 MB, and one that removes anything left behind if the demo is killed part way through. Both exit on their own a few seconds after the demo does.

## Where this pattern lives in a real system

In the gateway's configuration, where every route that has moved has a location block of its own and everything else falls through to the old system; in the review of that configuration, where somebody has to ask which rule wins; in the deployment pipeline, which tests the configuration with `nginx -t` and reloads rather than restarts; and in the session handling, which has to work for both systems for as long as both are live.
