# Prerequisites

## Required

- Java 21. Gradle comes with the wrapper in this directory.
- The idea of externalised configuration: a value that changes on somebody else's calendar lives outside the program and is read while it runs. The plain-Java Externalised Configuration project in this course teaches it with nothing installed, but this project explains everything it uses in its own files, so it can be read on its own.

## Explicitly not required

- **No container runtime.** The config server is a Java program, and the demo starts it as a second Java process and stops it at the end. There is no Docker, no broker and no database in this project.
- **No installed git.** The demo creates the repository and commits to it with JGit, a git written in Java.
- No prior Spring. Every word it introduces — config server, commit and version, fetching at startup, refresh, `@RefreshScope`, fail fast and optional — is said in plain language before the name for it is used, in [`dependencies.md`](dependencies.md).
- No knowledge of HTTP beyond "a program asks another program a question over the network and gets an answer with a status number".

## What you will need

The first run downloads the Spring libraries, about forty-five megabytes. After that `./gradlew run` and `./gradlew test` work offline. The demo uses free ports on your machine, chosen as it starts, so nothing needs to be free in advance.

## Versions this project pins

| Tool | Version |
| --- | --- |
| Spring Boot | 4.1.1 |
| Spring Cloud release train | 2025.1.3 |
| `org.springframework.cloud:spring-cloud-config-server` | 5.0.5 |
| `org.springframework.cloud:spring-cloud-starter-config` | 5.0.5 |
| JGit | 7.4.0, brought by Spring Cloud Config |
| `io.spring.dependency-management` plugin | 1.1.7 |
| JUnit | 5.10.2 |
| Java | 21 |
| Gradle | 9.2.1 |

Spring Boot and Spring Cloud are the newest generally available releases at the time the project was built. JGit is kept at the version Spring Cloud Config is built and tested against.
