# Microservices Patterns — Implementation Plan

How the twelve projects specified in [`spec.md`](spec.md) get built.

This is the *how*. The *what* is in `spec.md`, and the video and publishing
standard both inherit from is
[`../../docs/video-and-publishing-spec.md`](../../docs/video-and-publishing-spec.md).

---

## Current state

Nothing exists but these two documents.
`gradle-java/micro-services-design-patterns/` contains this `docs/` directory
and no projects.

The twenty-five Gang of Four projects are complete and are the working
reference: the file set, the build scripts, the slide renderer and the
generators all exist and work. Nothing in this category needs to be invented
except its own content — and one thing that *is* new, which is the simulation
harness (§Phase 1).

The lesson carried over from the behavioural build is the sequencing one:
**everything that changes what a video contains lands before the video is
rendered**, because re-rendering is the only step that costs ten minutes and
cannot be partially redone.

---

## Order of work

### Phase 0 — Wire the category into the shared tooling

Before any project is written, because all twelve depend on it and because
doing it later means editing twelve projects instead of five files.

1. **`docs/video-and-publishing-spec.md`** — §1 Scope becomes thirty-seven
   projects with a fourth row, and points at
   `micro-services-design-patterns/docs/spec.md` for the category detail.
2. **`docs/make_specs.py`** — twelve entries appended to `ORDER` and `NAME`,
   and the category-to-directory mapping taught the new folder name, which is
   the one place the longer directory name (`micro-services-design-patterns`
   rather than a single word) will need care.
3. **`docs/make_youtube_docs.py`** — twelve title and tag entries, from
   `spec.md` §7.
4. **`docs/make_thumbnails.py`** — twelve entries.
5. **`gradle-java/README.md` and the repository `README.md`** — a fourth
   category section and its learning order.

The per-project `SPECS` block in `make_specs.py` carries the real class names,
so it cannot be written before the project exists; it lands with each project.
All three generators already skip a slug whose directory is absent, so the
series can be listed in full from the start.

Phase 0 is done when all three generators run clean over the existing
twenty-five and report the twelve new slugs as not built yet.

### Phase 1 — Build API Gateway end to end, as the category's reference

API Gateway is first in the learning order and is the simplest of the twelve,
so it is the right project to shake out the template on. It is built
**complete** — code, tests, all ten documents, both diagrams, the animation,
the video — and reviewed before anything else starts.

Two things get settled here and then copied eleven times, and getting them
right is most of what Phase 1 is for:

**The simulation harness.** Three classes, no more (`spec.md` §2.4):

- a `Clock` seam and a fake implementation the tests advance by hand;
- a `RemoteService<T>` wrapper that adds simulated latency and can be scripted
  to fail — "fail twice, then succeed", "always time out", "take 3 seconds";
- a `CallLog` that records service, simulated timestamp, outcome and what the
  pattern decided, and prints the timeline the demo and the console slide need.

These must be small enough to read in one sitting and boring enough that no
project needs to modify them. If a later project has to change the harness, the
change is made in that project *and* backported, exactly as the audio-pipeline
fix was rolled across every project rather than left where it was found.

**The timeline slide.** The layout that shows a failing call sequence with
elapsed time — designed once, in `make_slides.py`, and reused. Every project in
this category needs one (`spec.md` §7.1).

### Phase 2 — Build the remaining eleven, in learning order

Service Discovery, Load Balancing, Retry, Circuit Breaker, Bulkhead, Database
per Service, API Composition, CQRS, Saga, Transactional Outbox, Idempotent
Consumer.

In order, and one at a time, because the scenarios build on each other far more
tightly than the Gang of Four ones do: Circuit Breaker's argument only lands
once Retry has been taught, API Composition exists to solve the problem
Database per Service creates, and Idempotent Consumer is the second half of
Transactional Outbox. Building out of order means writing those references
against projects that do not exist yet.

Per project, in this sequence — the code first, because every other artefact
quotes it, and the video last, because it is the only step that is expensive to
redo:

1. Design the services involved against `spec.md` §3, using the shared service
   map rather than inventing new services. Confirm the naive alternative is one
   a competent developer would actually write.
2. Scaffold the Gradle project from the previous one, copying the harness.
3. Write the production code and the naive counter-example classes.
4. Write the tests, including the property assertions `spec.md` §6.5 requires
   and the one that pins the naive alternative's wrong behaviour. Confirm the
   suite is deterministic and under two seconds.
5. `./gradlew build`, then `./gradlew run`, and quote the real output — the
   timeline, including its failure — in the top-level `README.md`.
6. Write `docs/` — problem statement, explainer (including the §2.1 limitation
   and the §5 cross-reference), both diagrams, the animation, prerequisites,
   session plan. Render both Mermaid diagrams to PNG.
7. Write `video/scenes.py` and `make_slides.py`. Render the poster and
   **look at it**.
8. `./build_video.sh`. Confirm it prints `audio timeline continuous`.
9. `python3 ../../docs/make_youtube_docs.py <slug>` and
   `python3 ../../docs/make_specs.py <slug>`.
10. Walk the project's conformance checklist — the repository-wide fourteen plus
    the six in `spec.md` §9.

### Phase 3 — Verify the category

Once all twelve exist: build and run all twelve, confirm the whole test suite is
sleep-free (`grep -r "Thread.sleep" src/test` returns nothing across the
category), confirm every poster shows its own pattern name, confirm every
`youtube.md` chapter list matches its current `.srt`, and measure loudness on
every delivered MP4.

Then regenerate all thirty-seven specs so the cross-category numbers are
consistent, and update both READMEs.

---

## Sequencing rules

**Nothing is rendered twice.** Everything that changes what a video *contains* —
narration text, slide content, the code being shown — lands before
`build_video.sh` is run for that project. This is why the video is step 8 of 10
rather than step 3.

**The harness is settled in Phase 1 and then frozen.** A harness that drifts
across twelve projects makes the twelve READMEs subtly wrong about what they
share. If it must change, it changes everywhere.

**Listen to the first build of each project.** The continuity self-check
verifies that no audio is missing; it cannot hear that the audio is bad.

**Look at every poster.** `poster.png` is generated, its correctness is not
checked by anything, and it is the single most visible artefact the project
produces.

**Do not batch the videos.** Rendering twelve at the end defers the discovery of
a systematic narration or slide problem until every project has one.

---

## Risks

| Risk | Mitigation |
| --- | --- |
| The simulation reads as fake, and the reader dismisses the lesson | The harness is honest about what it is and the explainer says so in every project (`spec.md` §2.1). The demo shows real failures with real consequences — a double charge, a lost event — not a print statement claiming a service is down. |
| Twelve projects blur into "a wrapper class that catches exceptions" | Retry, Circuit Breaker and Bulkhead are the three most at risk. Each carries a mandatory comparison with the other two, and each has to show a case where the *other* pattern is the wrong answer. |
| Beginners are lost — this is harder material than the Gang of Four | The order in `spec.md` §1 defers all failure handling until the shape of a call is understood, and all data problems until then. Prerequisites for these projects name the Gang of Four projects a reader should have done first. |
| Tests become slow and flaky, and then get deleted | `spec.md` §6.4 is a conformance item, not advice: no sleeps, seeded randomness, under two seconds, checked in Phase 3 by grep. |
| The category drifts into infrastructure teaching | `spec.md` §8 fixes what is out of scope and why. A thirteenth project needs a spec change, not a decision made mid-build. |
| Bulkhead's real threads make its tests non-deterministic | It is the only project allowed real concurrency; its tests use a fixed pool and latches. If a deterministic version cannot be written, the project is redesigned rather than the rule relaxed. |

---

## Definition of done

The category is complete when:

- [x] Twelve projects exist, each passing the repository-wide conformance
      checklist and the six category items in `spec.md` §9.
- [x] Every project builds, tests pass in under two seconds, and its README
      quotes real run output including the failure.
- [x] No `Thread.sleep` appears anywhere under `*/src/test`.
- [x] Twelve videos are rendered, each having printed
      `audio timeline continuous`, each listened to at least once.
- [x] Twelve posters and thumbnails have been looked at.
- [x] All thirty-seven projects' `spec.md` / `spec.html` regenerate clean —
      every one reporting a real scene count, runtime and test count, with
      integrated loudness within 0.02 LU of the −16 LUFS target.
- [x] The root `README.md`, `gradle-java/README.md` and the repository-wide
      spec all describe thirty-seven projects across four categories.
