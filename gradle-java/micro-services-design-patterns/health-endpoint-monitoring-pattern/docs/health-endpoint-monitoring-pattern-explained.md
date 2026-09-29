# Health Endpoint Monitoring, Explained

## The pattern in one sentence

Health Endpoint Monitoring gives each instance two addresses: liveness, which
says whether the process works and gets it restarted if not, and readiness,
which says whether it can take work now and takes it out of rotation if not.

## The 5 acts

### 1. An open port

Instance B is stuck: the process is running and its network port accepts
connections, but it cannot take an order. The load balancer only checks the
port, so B stays in rotation with A and C. Nine orders are shared in turn, and
the three that go to B fail.

### 2. Liveness

Each instance now answers `/health/live`. A and C answer `200 UP`; B answers
`503 DOWN, not responding`. The load balancer takes B out of rotation and all
nine orders succeed on A and C. The platform's `Restarter` checks liveness every
ten seconds. After three failures in a row it restarts B, which comes back
`200 UP` and rejoins the rotation.

### 3. Readiness

Now C loses its database, and the shared recommendations service goes down.
`/health/ready` checks the dependencies. A and B answer `200 DEGRADED
(recommendations down)`: recommendations are not critical, so they keep
taking orders, just without suggestions. C answers `503 DOWN (database down)`.
But C's liveness is still `200 UP`, so it is not restarted, which would not
bring its database back. Nine orders go to A and B and none fail.

### 4. A liveness check that is too deep

The payment provider, which all three instances share, is down for thirty
seconds. If liveness also checks payments (`deepLive`), every instance fails it,
and after three checks the platform restarts all three at once: no checkout at
all while they start up, and the provider is still down. With a shallow liveness
check, no instance is restarted. Restarting checkout cannot fix someone else's
outage.

### 5. The bill

Each readiness check calls three dependencies. Every ten seconds on three
instances, that is 54 dependency calls a minute before any customer orders
anything. And a detailed answer such as "database down" is exactly what an
attacker wants to know, so the detail belongs on an internal address and the
public one should say only up or down.

## The verdict

Give every service both. Keep liveness shallow: only the process itself.
Put critical dependencies in readiness, report non-critical ones as degraded,
cache the result for a few seconds, and keep the detailed answer off the public
internet.

## How to recognise this in code you did not write

- `/health`, `/healthz`, `/ready`, `/live`, `/actuator/health` endpoints.
- `livenessProbe` and `readinessProbe` in Kubernetes files.
- Status values `UP`, `DOWN`, `DEGRADED`, `OUT_OF_SERVICE`.
- Load balancer settings for health check path, interval and threshold.

## Where you have already met this

- Kubernetes liveness, readiness and startup probes.
- Spring Boot Actuator's `/actuator/health`, with its `liveness` and `readiness` groups.
- Load balancer target health checks in AWS, Azure and Google Cloud.
- Status pages that show a service as operational, degraded or down.
