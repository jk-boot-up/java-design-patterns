# Dependencies

This project uses Kubernetes, kind and the Fabric8 Kubernetes client, which the plain-Java project does not. This page says what they are, why they are here, and what they cost. It comes before the first line of Kubernetes code on purpose.

**Skipping this project loses none of the pattern.** The plain-Java Leader Election project in this course teaches all of it in plain Java, with nothing installed.

## What Kubernetes is, for this project

Kubernetes runs programs across a group of machines, called a **cluster**; each machine is a **node**. At its centre is the **API server**: a program that stores records describing everything in the cluster, and lets anyone with permission read and write them. Think of a notice board in a staff room, where every note has a number in the corner that goes up each time the note is rewritten.

One kind of record on that board is a **Lease**: a note that says who holds a job, how long the hold lasts, when the holder last renewed it, and how many times the holder has changed. The holder is the **holder identity**. Renewing is rewriting the note with a fresh time. The number in the corner is the **resource version**. If you rewrite a note and say which number you read, and someone has rewritten it since, the board refuses you; Kubernetes calls that refusal **409 Conflict**. That refusal is the only rule the board enforces about a Lease. It never takes a note down because it is old.

## What kind is

kind runs a whole Kubernetes cluster inside one container, as if the container were a machine. It is here so that `./gradlew run` can create a real cluster in about thirty seconds, use it, and delete it. The cluster is named `patterns-leader-election`, and its address is written to a private temporary file rather than to your own Kubernetes settings.

## What Fabric8 is

Fabric8 is a Java client for the Kubernetes API server, and it has a leader elector built in. Given a Lease's name, a copy's name, and three timings, it keeps asking the API server for the lease, renews it while it holds it, and calls back three times: when this copy starts leading, when it stops, and when it sees a new leader. This project uses its `LeaderElector` and `LeaseLock`, with a lease of 5 seconds, a renewal deadline of 4 seconds, and a retry every 1 second.

The official Kubernetes Java client, newest release 27.0.0, has a leader elector too, and it implements the same algorithm. Fabric8 was chosen because it is the client Quarkus, Apache Camel and the Java Operator SDK are built on, because its elector is the one the Java Operator SDK uses, and because the whole election is four settings and three callbacks. Its default HTTP stack, Vert.x, is swapped for the one built into the JDK, which is smaller and needs nothing else.

## Why this project uses them

Because the three things this project teaches cannot happen inside one program. A lease that nothing on the server takes away, judged by each copy's own clock. A leader frozen with every thread stopped, as a real process is by a long garbage-collection pause. And a real server refusing a write made from an old version. All three need copies that are genuinely separate processes, and a record that lives outside all of them.

## What to install

A JDK, version 21, a container runtime, and kind. Gradle downloads the rest, and the versions are pinned:

| Tool | Version |
| --- | --- |
| Docker, or a Docker-compatible runtime | running; 24 or later |
| kind | 0.33.0 |
| Kubernetes node image | `kindest/node:v1.37.0` |
| `io.fabric8:kubernetes-client` | 8.0.0 |
| `io.fabric8:kubernetes-httpclient-jdk` | 8.0.0 |
| `org.slf4j:slf4j-simple` | 2.0.20 |

Every one of these is the newest generally available release; none is held back.

## What it costs

The first run pulls the kind node image, about 1 GB. After that a run takes a little over a minute: about thirty seconds to create the cluster, and the rest waiting for leases to run out, because that is the lesson. The node uses several hundred megabytes of memory while it is up, and each of the three copies is a small Java process of its own. The freeze in the fourth and fifth acts uses the operating system's stop and continue signals, so the demo runs on macOS and Linux, not on Windows outside WSL.

## Where this pattern lives in a real system

In the Lease objects in a cluster's `kube-system` namespace, one for the scheduler and one for the controller manager; in every operator that runs more than one copy; and in the few lines of configuration that set the lease length, the renewal deadline and the retry period. The fencing check does not live in Kubernetes at all. It lives in whatever the leader writes to.
