# Externalised Configuration with Spring Cloud Config, Explained

## The pattern in one sentence

Externalised configuration means a value that changes on somebody else's calendar lives outside the program, and the program reads it while it runs, so changing the value needs no rebuild and no release.

## The analogy, before any of Spring's words

Think of a chain of bakeries. The price list is kept at head office, in a filing cabinet, and every change is signed and dated in a ledger. Head office has a receptionist. When a branch opens in the morning, it phones the receptionist, who reads out the current list, and the branch writes the prices on its board for the day.

Now four things this makes you think about. If head office changes a price at eleven, the branches carry on with the morning's prices until somebody tells them to phone again. When a branch does phone again, it rewrites its board, but the poster it printed at opening time still shows the old price. If somebody at head office writes a nonsense price, the receptionist reads it out faithfully, because checking prices is not the receptionist's job. And if head office's phone line is down, a branch that is already open carries on, while a branch that is just opening has to decide: stay shut, or open on the prices printed on its old menu. Those four things are this project.

## What Spring Cloud Config calls these things

The **config server** is the receptionist: a separate Java program, Spring Cloud Config Server, that reads a repository of settings files and answers over HTTP. Asked for the settings of the application called `checkout-service`, it answers with the file called `checkout-service.yml`.

The **git repository** is the filing cabinet with its ledger. Every change is a **commit**, with who made it, when and why. A commit's **id**, shortened to seven characters such as `2a6198d`, names it. The server reports which commit its answer came from as the **version**.

**Fetching at startup** is the branch phoning as it opens. The shop's settings say `spring.config.import: configserver:` and the address, and Spring asks the server before the shop starts.

A **refresh** is telling the branch to phone again: `POST /actuator/refresh`, a request to the running shop. **Actuator** is the Spring Boot library that provides it. It answers with the names of the settings that changed.

**`@RefreshScope`** marks an object to be thrown away and rebuilt after a refresh: the board. An ordinary object that copied a setting with `@Value` when the shop started is the poster.

**Fail fast** and **optional** are the two answers to a server that cannot be reached at startup: refuse to start, or start on the defaults packed inside the shop.

## The six acts

### The Setting Lives In Git

The demo creates a git repository in a temporary folder and commits `free-over: 50.00`, as Priya in engineering. It starts the config server as a second Java process, pointed at that repository. Asked for `checkout-service`, the server answers with version 2a6198d and a threshold of 50.0. Then the shop starts, fetches its settings from the server, and quotes a £48.00 basket: delivery £4.99, because £48.00 is under £50.00. The banner across the top of the home page says free delivery on orders over £50.00.

```
  git commit 2a6198d by Priya in engineering: free-over 50.00
    version 2a6198d, delivery.free-over 50.0
    quote:  goods £48.00 delivery £4.99 threshold £50.00
    banner: Free delivery on orders over £50.00
```

### Committed, Not In Force

Maya in marketing commits `free-over: 35.00` for the weekend. The config server reads the repository on every request, so it answers with the new commit, 64f6a92, and 35.0 straight away. The running shop has not asked again. It still quotes £4.99 on the £48.00 basket, against £50.00. The value in git and the value in force are now different, and nothing is broken.

```
  git commit 64f6a92 by Maya in marketing: free-over 35.00
    version 64f6a92, delivery.free-over 35.0
    quote:  goods £48.00 delivery £4.99 threshold £50.00
```

### The Refresh

The demo sends the running shop `POST /actuator/refresh`. The shop fetches its settings again and reports what changed: `config.client.version`, which is the commit its settings came from, and `delivery.free-over`. The next quote ships the £48.00 basket free, against £35.00. It is the same running copy of the shop, started in the first act: restarts 0.

```
  the shop fetches again and reports what changed: config.client.version, delivery.free-over
    quote:  goods £48.00 delivery FREE threshold £35.00
  the same running shop: yes, still the copy started in act 1. restarts: 0.
```

### The Surprise: Two Thresholds In One Shop

This is the headline of the project. The checkout's settings object is marked `@RefreshScope`, so the refresh rebuilt it. The banner reads the very same setting with `@Value`, copied into a field when the shop started, and nothing rebuilds it. So one running shop quotes against £35.00 and advertises £50.00 at the same time. No error, no warning. Only a restart of the shop brings the banner to £35.00.

```
    quote:  goods £48.00 delivery FREE threshold £35.00
    banner: Free delivery on orders over £50.00
  after a restart of the shop:
    banner: Free delivery on orders over £35.00
```

### The Bill: A Value Nobody Checked

On Saturday morning somebody commits `free-over: -1`. The config server serves it, because it does not check values. The refresh answers 200 and reports the key as changed. The shop's settings declare a range, £5.00 to £200.00, and Spring checks it when it rebuilds the settings object, on the next quote. The check fails, and there is nothing to fall back to, so the quote fails. And the next. Five quotes, five failures, each with HTTP status 500. Sam on call commits 35.00 again and refreshes, and the shop quotes normally. Git's own log is the history of all of it, newest first.

```
  git commit 6aaf4da by Maya in marketing: free-over -1
    version 6aaf4da, delivery.free-over -1
  the refresh answers 200 and reports: config.client.version, delivery.free-over
  the next 5 quotes: 5 failed, each with HTTP status 500.
  git commit f68331f by Sam on call: free-over 35.00, then a refresh: config.client.version, delivery.free-over
    f68331f  Sam on call  Put the weekend promotion back
    6aaf4da  Maya in marketing  Free delivery for everyone?
    64f6a92  Maya in marketing  Weekend promotion: free delivery over 35 pounds
    2a6198d  Priya in engineering  Free delivery over 50 pounds
```

### The Bill: The Server Stops

The demo stops the config server process. A refresh of the running shop now answers 500, and changes nothing: the shop keeps what it already fetched and still quotes the £48.00 basket free, against £35.00. A new copy of the shop, told to fail fast, refuses to start. A new copy told the server is optional starts on the default packed inside it, £50.00, and charges £4.99. The promotion is gone, and nothing reports an error.

```
  a refresh of the running shop now answers 500.
    quote:  goods £48.00 delivery FREE threshold £35.00
    refused to start: Could not locate PropertySource and the fail fast property is set, failing
    quote:  goods £48.00 delivery £4.99 threshold £50.00
```

## The verdict

Put the settings that change on somebody else's calendar in git, behind a config server, when several services share them and the history matters. Then say four things out loud, because Spring will not assume any of them. A commit is not in force until each running copy is refreshed, so decide who sends the refresh. A refresh reaches only `@RefreshScope` objects, so find every `@Value` that copies a changeable setting. A range check with nothing behind it turns a typo into an outage, so decide what the shop falls back to. And choose, for every service, between fail fast and optional, knowing that optional starts quietly on old values.

## How to recognise this in code you did not write

- `spring.config.import: configserver:` in a service's settings. With `optional:` in front of it, the service starts without the server.
- `spring.cloud.config.fail-fast: true`, or its absence.
- `@RefreshScope` on a class, and `@Value("${...}")` on a constructor or a field in a class without it. The second one never changes after startup.
- `POST /actuator/refresh` in a pipeline script, or Spring Cloud Bus, which sends the refresh to every copy at once.
- `@Validated` with ranges on a `@ConfigurationProperties` class, and whether anything catches the failure.

## Where you have already met this

Any Spring estate with more than a handful of services. Kubernetes ConfigMaps, Consul and AWS AppConfig ask the same two questions: when does a running program notice a change, and which parts of it hold on to the old value?

## When this is too much

If the shop runs as one or two copies and a value changes a few times a year, an environment variable and a restart are simpler and have no server to keep alive. If a value changes every minute, or per customer, it is data or a feature flag, not configuration.
