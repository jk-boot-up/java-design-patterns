# Dependencies

This project uses Spring Boot, Spring Cloud Config and JGit, which the plain-Java twin does not. This page says what they are, why they are here, and what they cost. It comes before the first line of Spring code on purpose.

**Skipping this project loses none of the pattern.** The plain-Java Externalised Configuration project in this course teaches all of it, with nothing installed.

## The analogy, before any of Spring's words

Think of a chain of bakeries. The price list is kept at head office, in a filing cabinet, and every change to it is signed and dated in a ledger. Head office has a receptionist. When a branch opens in the morning, it phones the receptionist, who reads out the current price list, and the branch writes the prices on its own board for the day. If head office changes a price at eleven, the branches do not know until somebody tells them to phone again. And one branch may have printed a poster at opening time, which still shows the old price after the board has been rubbed out and rewritten.

## What each piece is called

**Spring Boot** is a framework for building Java programs that start up as small web servers. Both programs in this project are Spring Boot applications.

The **config server** is the receptionist: a small web program, Spring Cloud Config Server, that reads a repository of settings files and answers the question "what are the settings for this application?" over HTTP. Its whole code in this project is one annotation, `@EnableConfigServer`.

The **git repository** is the filing cabinet with its ledger. Each change is a **commit**, which records the new file, who made it, when, and a short message. A commit has an **id**, a string of letters and digits worked out from all of that; the first seven characters, such as `2a6198d`, are enough to name it. The config server tells the shop which commit its settings came from, and calls that the **version**.

**Fetching at startup** is the branch phoning in as it opens. The shop's one line `spring.config.import: configserver:` means "before you start, ask this server for your settings".

A **refresh** is telling a branch to phone again. In Spring it is an HTTP request to the running shop, `POST /actuator/refresh`, which comes from **Spring Boot Actuator**, a library that gives a program a set of management pages. The refresh answers with the names of the settings that changed.

**`@RefreshScope`** marks an object as one to throw away and build again after a refresh: the board that is rubbed out and rewritten. An object that is not marked, and copied a setting when the shop started, is the poster: it keeps the old value.

**Fail fast** is a setting that says: if the config server cannot be reached at startup, refuse to start. **Optional** is the opposite: start anyway, on whatever settings are packed inside the program.

**JGit** is a git written in Java. The config server uses it to read the repository, and the demo uses it to create the repository and commit to it, so git does not need to be installed.

## Why this project uses them

Because the things this project teaches — a change that is served but not yet in force, a refresh with no restart, an object the refresh does not reach, and a shop that must decide what to do when its settings cannot be fetched — only exist when the settings live in another process and the shop fetches them over a network. That is what a config server is.

## What to install

Only a JDK, version 21. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Spring Boot | 4.1.1 |
| Spring Cloud release train | 2025.1.3 |
| Spring Cloud Config, server and client | 5.0.5 |
| JGit | 7.4.0, as Spring Cloud Config brings it |
| Spring dependency-management Gradle plugin | 1.1.7 |
| JUnit | 5.10.2 |

Spring Boot 4.1.1 and Spring Cloud 2025.1.3 are the newest generally available releases; the next ones, 4.2.0 and 2026.0.0, are still milestones. JGit stays at the version Spring Cloud Config is built against rather than being forced up to the newest, 7.8.0.

No container runtime is needed. No git needs to be installed.

## What it costs

The first build downloads about forty-five megabytes of libraries, 78 jars. After that a run takes about six seconds, most of it two Spring Boot programs starting, and the shop starting three times. The config server process is given at most 256 megabytes of memory. The demo picks free ports for every program, so it can run beside anything else on the machine.

## Where this pattern lives in a real system

In a git repository of settings files, one per application and one per profile; in a config server, usually several copies behind a load balancer; in each service's `spring.config.import` line and its choice between fail fast and optional; in the pipeline or the Spring Cloud Bus message that sends the refresh after a merge; and in the review of which objects are `@RefreshScope` and which copied a value at startup.
