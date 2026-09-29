# Health Endpoint Monitoring Pattern — Video Narration Script

## 1. Health Endpoint Monitoring

Hello, and welcome. This video explains the Health Endpoint Monitoring pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Each running copy of a service answers a small web address that says how it is. It answers two questions. Am I working at all? If not, restart me. And can I take work right now? If not, stop sending it. Think of the host at a busy restaurant, who decides which waiter gets the next table. A waiter who has fainted is sent home and replaced. A waiter whose kitchen has run out of gas is fine, but should not get tables for now. Sending them home would not fix the gas. In this video, the domain is an online shop. Its checkout service runs as three copies, called A, B and C. A load balancer shares the orders between them. By the end, you will hear why an open port is not a healthy service. The difference between liveness and readiness. Why a check that asks too much restarts everything. And what these checks cost.

## 2. The Scenario

Here is the scenario. The shop's checkout service runs as three instances. An instance is one running copy of the same program. Each instance has its own database connection. All three share the same payment provider. And the same product recommendations service. In front of them sits a load balancer. It shares the orders between A, B and C, in turn. How does it know which instances are fit for work?

## 3. Act One — An open port

First demo: an open port. Instance B is stuck. It is running, and its network port answers, but it cannot take an order. The load balancer only checks the port. So it keeps sending B its share of the work. Nine orders go out, shared between A, B and C. The three that land on B fail.

## 4. Act Two — Liveness

Second demo: a liveness endpoint. Each instance now answers a small web address: health, live. It asks one question. Is this process working at all? A and C answer two hundred, up. B answers five oh three, down, not responding. The load balancer takes B out of rotation. Nine orders go to A and C, and none fail. The platform also watches liveness. After three failed checks in a row, it restarts B. B comes back up, and rejoins the rotation.

## 5. Act Three — Readiness

Third demo: a readiness endpoint. This one asks a different question. Can this instance take an order right now? To answer, it checks what the instance depends on. Instance C has lost its database. And the product recommendations service is down for everyone. A and B answer two hundred, degraded. Recommendations are nice to have, not essential. So they keep taking orders, without suggestions. C answers five oh three, down, database down. The load balancer stops sending it orders. But C's liveness still says up. So nobody restarts it. A restart would not bring its database back.

## 6. Act Four — A liveness check that is too deep

Fourth demo: a liveness check that is too deep. The payment provider goes down for thirty seconds. All three instances share it. Suppose liveness also checked payments. Every instance would fail. After three checks, the platform restarts all three at once. Three of three. While they start up, there is no checkout at all. With liveness that checks only the process itself, nothing is restarted. Restarting checkout cannot fix the payment provider. So keep shared dependencies out of liveness.

## 7. Act Five — The bill

Fifth demo: the bill. Each readiness check calls three dependencies. Every ten seconds, on three instances, that is fifty-four calls a minute. Before a single customer orders anything. And the details can say too much. Database down is useful to the platform. It is also useful to an attacker. Keep the details on an internal address, and let the public one say only up, or down.

## 8. The Pattern

Let's name the pattern. Every instance answers two addresses. Health, live, asks: is the process working at all? If the answer is no, three times in a row, the platform restarts it. Health, ready, asks: can it take work right now? If a critical dependency is down, the answer is no, and the load balancer skips it. If only something optional is down, the answer is degraded. It keeps working, with less.

## 9. Who Does What

Here is who does what. The health endpoint has two checks, live and ready. The load balancer uses ready, to decide where to send orders. The restarter stands in for the platform. It uses live, to decide what to restart. And each dependency is marked critical, or not. That mark decides between down, and degraded.

## 10. Where You Have Seen It

You have probably met this pattern already. Kubernetes has liveness probes and readiness probes. They are exactly these two questions. Spring Boot Actuator gives every application a health address. Cloud load balancers have health check settings. And public status pages show operational, degraded, or down.

## 11. When To Use It

So, when should you use it? Give every service that runs as several instances both checks. Keep liveness shallow: only the process itself. Put critical dependencies in readiness. Report optional ones as degraded. Cache the answer for a few seconds, so checks do not flood your dependencies. And keep the detailed answer off the public internet.

## 12. Thanks for Watching

That's the Health Endpoint Monitoring pattern. If you remember one sentence, make it this one. Alive is not the same as ready. Restart what is dead, and stop sending work to what is not ready. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Cache the readiness answer for five seconds. Then count the dependency calls a minute. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
