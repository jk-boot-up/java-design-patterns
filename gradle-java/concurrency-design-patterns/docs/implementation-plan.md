# Concurrency Patterns — Implementation Plan

How the six projects in this category get built. [`spec.md`](spec.md) fixes what
they are; this fixes the order, the rules that keep the build from redoing
itself, and what "finished" means.

**Nothing here is built yet.** This document and [`spec.md`](spec.md) are the
whole category at the time of writing.

---

## Current state

| | |
| --- | --- |
| Projects specified | 6 |
| Projects built | 0 |
| Category registered with the shared generators | no |
| Existing projects in the repository | 37 built, 8 more specified in `platform-design-patterns` |

---

## Order of work

### Phase 0 — Wire the category in, and build the test harness

Two jobs, and the second is what makes this category possible at all.

**Tooling.** Add `concurrency-design-patterns` to `CATEGORIES` in
`gradle-java/docs/make_narration.py`, and add all six slugs to the per-project
tables in `make_specs.py`, `make_thumbnails.py` and `make_youtube_docs.py` —
those three carry their own tables and **silently skip anything missing**. Then
register the category in `gradle-java/README.md`, the root `README.md`, and
`docs/video-and-publishing-spec.md`.

**The determinism harness.** Before any project, extract from
`bulkhead-pattern` (§31) what it already does, and settle the three pieces
`spec.md` §2 names:

1. A **barrier helper** that parks *n* threads at a named point and releases
   them together, so a race is forced rather than awaited.
2. An **interleaving runner** that replays a pair of operations across a fixed
   list of planned interleavings and asserts the outcome of each. This is what
   turns "the lost update happens sometimes" into a test that fails every run.
3. A **step-controlled executor** that runs queued tasks one at a time on
   command, so a test can assert on state between tasks.

These are copied into each project rather than shared through a library — the
repository has no cross-project dependencies and should not grow one for this.
Copying means the reader of any single project sees the whole mechanism.

**Exit:** the tooling lists the category with zero projects, and the three
harness pieces exist, are tested against a known race, and have a home in the
reference project.

### Phase 1 — Build Producer–Consumer end to end, as the category's reference

It goes first because it is the simplest honest concurrency failure and because
every later project consumes its queue. Build it complete — source, tests, the
full document set, both diagrams, animation, video, publishing document — and
treat the result as the template.

Three things this phase settles for everyone after it:

- **The shape of a forced failure.** How a race is set up, named and asserted,
  and how the test reads to a beginner. Get it right once.
- **How timings are printed.** Queue depth, throughput, thread counts — one
  format, used by all six.
- **The "What the scheduler really does" section.** Its length, its tone, and
  where it sits relative to the costs.

**Exit:** one project passing every item in `spec.md` §9, with the harness
proven on a real race.

### Phase 2 — Build the remaining five, one at a time, in learning order

**One project at a time, finished completely before the next begins.**

| Order | Project | The failure to force | Risk |
| --- | --- | --- | --- |
| 1 | `thread-pool-pattern` | Pool starvation deadlock, and the thread-per-order collapse | **Medium** — the `OutOfMemoryError` demo must be safe to run |
| 2 | `future-promise-pattern` | The stack trace missing the line that caused it | Low |
| 3 | `read-write-lock-pattern` | A reader seeing half a price update; writer starvation | Medium |
| 4 | `monitor-object-pattern` | The lost update; `volatile` not being enough; `if` instead of `while` | Low |
| 5 | `active-object-pattern` | The mailbox backing up; the throughput ceiling | **Medium** — it is a capstone and must not re-teach four projects |

Two specific cautions, recorded now because both are discovered late otherwise.

**The thread-per-order collapse must not destabilise the machine building it.**
Demonstrating `OutOfMemoryError: unable to create native thread` by actually
exhausting a laptop is not acceptable in a course a beginner runs. Cap the demo,
show the curve — creation cost and context-switch cost climbing with thread
count — and print the extrapolation rather than reaching the cliff. State in
narration that the cliff is real and where it sits.

**Active Object must stay a capstone, not a recap.** Its job is the assembly:
queue plus thread plus future plus state ownership. It links to the four
projects that taught those and re-teaches none of them. If its script is
running long, that is what is wrong with it.

**Exit:** six projects complete, each verified before the next begins.

### Phase 3 — Verify the category

1. The artefact sweep from
   [`../../micro-services-design-patterns/docs/ai-session.md`](../../micro-services-design-patterns/docs/ai-session.md)
   §2, pointed here.
2. `./gradlew test` in every project, **run twenty times in a row**, with every
   run green. This is the category's defining check and it replaces the single
   run the other categories do.
3. No `Thread.sleep` anywhere under `*/src/test`, and none in the demos except
   where the delay is the subject.
4. Every spec regenerated **after** its video exists — a spec reporting
   `0 scenes` is stale, and this has already shipped once in this repository.
5. Every video printed `audio timeline continuous`, and every one listened to
   with the screen ignored, checking the narration stands alone.
6. Every poster and thumbnail looked at.
7. `git status` shows no mp4, m4a, srt, wav, log, `docs/audio/` or
   `video/build/`.
8. The six extra conformance items in `spec.md` §9 checked per project.

---

## Sequencing rules

**Finish one project before starting the next.** The standing rule across this
repository.

**Run the demo before quoting it.** Every number in a document, a slide or a
narration line comes from real `./gradlew run` output. In this category that
matters more than usual, because timings differ between machines: quote the
figures from one nominated machine and say in the README that the reader's will
differ in magnitude but not in shape.

**Regenerate the spec last, after the video exists.** `make_specs.py` measures
the mp4 and silently degrades if it is absent.

**Any fix to the shared pipeline is rolled out to all projects.**

**Nothing is committed or pushed unless asked.** Build artefacts go to
`.gitignore`; source, documents, `animation.html`, posters, thumbnails and
rendered diagrams stay in. Commit messages carry no co-author trailer.

---

## Framework register

Any open-source framework may be used where it is genuinely needed, and every
use is accounted for here before it reaches a build file — the same rule the
platform category follows.

| Project | Dependency | Verdict |
| --- | --- | --- |
| all six | JUnit 5 (`5.10.x`) | The repository standard. |
| all six | **nothing else** | `java.util.concurrent` is the subject. Adding a concurrency library would mean teaching the library instead of the pattern. |

Two candidates are worth recording, because both are tempting and both may yet
be right. Neither is prohibited — this is the current judgement, to be revisited
if a draft argues otherwise:

| Candidate | Current judgement |
| --- | --- |
| jcstress | The right tool for proving memory-model claims, and genuinely excellent. It needs a harness a beginner cannot read and runs for minutes, which breaks the two-second budget. Best use if taken: **one project, as a closing scene** — "here is the tool that proves this properly" — rather than as the category's test mechanism. |
| Awaitility | Makes waiting readable, which sounds ideal, but this category's whole thesis is that tests should not wait. A latch says *"both threads are now here"*; Awaitility says *"check again in a moment"*. The latch is the lesson. |

This category is expected to stay pure Java with no Tier 2, not because
frameworks are unwelcome but because `java.util.concurrent` is the subject and
there is no process boundary to cross. If a project finds a library that makes a
concurrency idea clearer rather than more magical, take it and add a row.

---

## Risks

| Risk | Mitigation |
| --- | --- |
| **A test flakes on a loaded CI machine** | The defining risk. Phase 3 runs every suite twenty times. A test that depends on timing rather than on a latch is rewritten, not retried. |
| **The demos are slow** | Latches release immediately; sleeps do not. A suite that takes minutes has sleeps in it. The under-two-seconds budget still applies. |
| The `OutOfMemoryError` demo harms the machine | Capped and extrapolated, never actually exhausted. Recorded in Phase 2. |
| Timings quoted from one machine mislead on another | Quote from one nominated machine, say so in the README, and let the reader compare shapes rather than absolutes. |
| **Narration becomes unfollowable without the picture** | An interleaving is naturally visual, and this is the hardest category to narrate. `spec.md` §7 makes naming the threads and speaking the order a rule. Listen to every video with the screen off. |
| Active Object recaps four earlier projects | It links rather than re-teaches; a long script is the symptom. |
| Virtual threads date the Thread Pool project | §47 addresses them directly rather than ignoring them. The pattern is bounding a resource, and that survives. |
| The harness gets copied with a bug in it | It is tested against a known race in Phase 0, before it is copied five times. |

---

## Definition of done

The category is complete when:

- [ ] Six projects exist, each passing the repository-wide conformance checklist
      and the six extra items in `spec.md` §9.
- [ ] **Every suite has been run twenty consecutive times with no flake.**
- [ ] Every naive failure reproduces on every run, forced by a latch, a barrier
      or a planned interleaving — never by a sleep.
- [ ] Every project builds, tests pass in under two seconds, and its README
      quotes real run output including the failure, the fix and the cost.
- [ ] Every video is rendered, printed `audio timeline continuous`, runs between
      eleven and thirteen minutes, and has been **listened to with the screen
      ignored**.
- [ ] Every poster and thumbnail has been looked at.
- [ ] Every explainer has its "What the scheduler really does" section, and
      every video says it aloud.
- [ ] All specs across the repository regenerate clean.
- [ ] The root `README.md`, `gradle-java/README.md` and the repository-wide spec
      all describe the category.
