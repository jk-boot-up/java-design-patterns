# Prerequisites

What you need before starting this project, what you can pick up as you go, and
what you explicitly do not need to know. The short version: if you can read a Java
interface and a `for` loop, you are ready.

## Knowledge Prerequisites

### Required

- **Java basics** — classes, interfaces, `final` fields, constructors.
- **`List` and `Map`** — `get`, `put`, iteration. Nothing exotic.
- **Reading a JUnit test** — `assertEquals`, `assertTrue`. You do not need to be
  able to write one, though you will be invited to.
- **What a service is, loosely.** "A program on another machine that answers
  questions over the network" is enough. You do not need to have deployed one.

### Helpful, but explained as we go

- **The Strategy pattern** ([`../../behavioural/strategy-pattern`](../../behavioural/strategy-pattern)).
  This project *is* Strategy, applied to machines instead of business rules. If you
  have done that session, the shape of `LoadBalancer` will look familiar
  immediately. If you have not, you will learn it here, and the earlier project
  will then feel like revision.
- **The Service Discovery pattern** ([`../service-discovery-pattern`](../service-discovery-pattern)).
  That project answers "what instances exist?" This one answers "which of them do I
  ask?" — so it picks up exactly where the other one puts you down. You can still do
  this one first; the list of three instances is simply handed to you here.
- **A running mean.** `LeastLatencyBalancer` keeps one, in three lines. If the term
  is new, there is a primer below.

### Explicitly NOT required

- **Any experience running a cluster.** There is no Docker here, no Kubernetes, no
  service mesh, no cloud account and no network. The three "instances" are three
  objects in one JVM.
- **Spring, Spring Cloud or Ribbon.** The pattern is an interface with one method.
  Nothing in this project imports anything outside the JDK.
- **Threads or concurrency.** Everything runs on one thread, in a fixed order, so
  every number in the output is reproducible.
- **Statistics.** The one piece of arithmetic is a running average, written out in
  full below.

## A 60-Second "Load Balancing" Primer

When a service is busy, you run more than one copy of it. The copies are
interchangeable: ask any of them and you get the same answer.

That immediately creates a question that did not exist when there was one copy:
**which copy do you ask?** Answering it is load balancing, and there are exactly two
places the answer can live.

It can live **in the caller**, which is this pattern. Every client picks for itself,
on every request, from a list of who is available.

Or it can live **in front of the cluster** — one component that every request passes
through, which picks on the caller's behalf. That is *server-side* load balancing.

Neither is a beginner's mistake. Client-side balancing can use information the
caller alone has; server-side balancing can see all the traffic, which no single
caller can. This project builds the first one honestly, including the two places
where it falls down, and then tells you when to reach for the second.

## A 60-Second "Running Mean" Primer

`LeastLatencyBalancer` needs to remember how slow each instance has been, across
many requests, without keeping every measurement. The standard trick is a running
mean — you keep the average and the count, and nudge the average towards each new
number:

```java
int seen = samples.merge(id, 1, Integer::sum);
long previous = averageMillis.getOrDefault(id, tookMillis);
averageMillis.put(id, previous + (tookMillis - previous) / seen);
```

Read the last line in words: move the old average a fraction of the way towards the
new measurement, and make that fraction smaller the more samples you have seen. The
tenth measurement moves it a tenth of the way; the hundredth moves it a hundredth.

The point of it is the *hundredth* case. One unlucky slow request should not rewrite
what the client believes about a machine that has been fast a hundred times.

## A 60-Second "Simulated Network" Primer

There is no network in this project, and there is no waiting.

`SimulatedClock` is a `long` with a method to move it forward. It never advances on
its own. `RemoteCall` wraps a piece of work with a latency: when you invoke it, it
pushes the clock forward by that many milliseconds and writes a line into `CallLog`.

So when the output says twelve requests took 320 milliseconds, that is not a
measurement subject to what else your laptop was doing. It is arithmetic, it is the
same on every machine, and the whole test suite finishes in about a second.

`CallLog` keeps the timeline — who called whom, when, and which instance was chosen —
so you can read afterwards exactly how the traffic was shared out.

## Software Prerequisites

- **JDK 21 or newer.** Nothing else.
- **Gradle:** not needed globally. The project ships a wrapper.

### Installing JDK 21

macOS, with Homebrew:

```bash
brew install openjdk@21
sudo ln -sfn $(brew --prefix)/opt/openjdk@21/libexec/openjdk.jdk \
    /Library/Java/JavaVirtualMachines/openjdk-21.jdk
```

Linux (Debian or Ubuntu):

```bash
sudo apt install openjdk-21-jdk
```

Windows: install the Microsoft Build of OpenJDK 21 or Temurin 21 from the
installer, and let it set `JAVA_HOME`.

### Verify Your Setup

```bash
java -version          # expect 21 or newer
cd micro-services-design-patterns/load-balancing-pattern
./gradlew test         # expect BUILD SUCCESSFUL, 21 tests
./gradlew run          # expect four acts
```

If `./gradlew` will not execute on macOS or Linux, make it executable:

```bash
chmod +x gradlew
```

The first `./gradlew` command downloads Gradle itself and needs a network
connection. Everything after that works offline, including the demo — because the
demo has no network to use.

## Troubleshooting

**"Unsupported class file major version"** — Gradle is using an older JDK than the
toolchain asks for. Check `java -version`, and set `JAVA_HOME` to a 21 install.

**Act one is the fastest act, and nothing fails** — that is correct, and it is the
whole point of act one. Taking the first instance every time gives the right answer
in 120ms while two paid-for machines sit idle. If you were expecting an error, that
expectation is the lesson.

**Every test in `FirstInstanceBalancerTest` passes** — also correct, also
deliberate. A concentration bug does not announce itself with a failing test.

**The numbers differ from the ones in the docs** — they should not. Every latency
comes from `SimulatedClock` and `RandomBalancer` is seeded. If your output differs
from `README.md`, something has genuinely changed in the source.

## Recommended Reading Order

1. [`problem-statement.md`](problem-statement.md) — three instances, one of them
   busy, and the three-line choice nobody notices making
2. Run `./gradlew run` and read the four acts, in order. Read the *timings* as well
   as the shares.
3. [`load-balancing-pattern-explained.md`](load-balancing-pattern-explained.md) —
   the pattern, starting from a row of supermarket tills
4. [`class-diagram.md`](class-diagram.md) and [`uml-diagram.md`](uml-diagram.md) —
   the structure, then the five sequences
5. [`animation.html`](animation.html) — the same twelve requests being shared out,
   one step at a time
6. The tests, which are the specification: `LoadBalancerTest` first, then
   `FirstInstanceBalancerTest` to see a passing test file that describes a problem
