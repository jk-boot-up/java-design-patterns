# Architectural Patterns — Implementation Plan

How the five projects in this category get built. [`spec.md`](spec.md) fixes what
they are; this fixes the order, the rules that keep the build from redoing
itself, and what "finished" means.

**Nothing here is built yet.** This document and [`spec.md`](spec.md) are the
whole category at the time of writing.

---

## Current state

| | |
| --- | --- |
| Projects specified | 5 (four architectures; Clean Architecture is two projects) |
| Projects built | **5 of 5 — the category is complete.** Layered Architecture (18 tests, 15:33), MVC (19 tests, 12:42), Hexagonal Architecture (17 tests, 10:11), Clean Architecture (16 tests, 10:19), Clean Architecture with Spring (11 tests, 9:09); all with full documents, diagrams, animation and a rendered video. |
| Category registered with the shared generators | yes — `make_narration.py`, `make_specs.py`, `make_thumbnails.py`, `make_youtube_docs.py`, and the root `README.md`, `gradle-java/README.md` and `docs/video-and-publishing-spec.md` all list the category |
| Existing projects in the repository | 37 built; 35 more specified across the platform, concurrency, enterprise, architectural and foundational categories |

---

## Order of work

### Phase 0 — Wire the category in, and write the feature once

Two jobs. The second is unusual and is the thing that makes this category
concrete rather than vague.

**Tooling.** Add `architectural-design-patterns` to `CATEGORIES` in
`gradle-java/docs/make_narration.py`, and add all five slugs to the per-project
tables in `make_specs.py`, `make_thumbnails.py` and `make_youtube_docs.py` —
those three carry their own tables and **silently skip anything missing**. Then
register the category in `gradle-java/README.md`, the root `README.md` and
`docs/video-and-publishing-spec.md`.

**The shared feature.** All five projects implement the same thing: a customer
places an order with three lines, stock is checked, payment is taken, a
confirmation is sent. Write it once, as a specification rather than as code:

1. **The behaviour**, as a list of observable outcomes.
2. **The acceptance tests** — the same assertions in all four projects, phrased
   so they can run against four different structures. If a test cannot be
   written that way, the feature is too coupled to a shape and needs
   rewording.
3. **The seed data**, so all four demos print recognisably the same run.

Doing this first is what lets a reader diff project 63 against project 66 and
see only the architecture. Doing it after the first project means retrofitting
four.

**The architecture test.** Settle how a dependency rule is asserted, and settle
it once. See the framework register below: this is the one place a library is
worth taking.

**Exit:** the tooling lists the category with zero projects; the feature, its
acceptance tests and the seed data exist in one place; and the architecture-test
approach is proven against a deliberate violation.

### Phase 1 — Build Layered end to end, as the category's reference

It goes first because it is the architecture most readers already have, so it is
the baseline the other three are measured against — and because its failure mode
is the one everyone has lived with: layers that exist as folders and are
violated by one convenient call.

Three things this phase settles for everyone after it:

- **How the architecture test reads and how it fails.** Its message must name
  the offending class and the rule it broke. This is the category's signature
  moment and it gets designed once.
- **How the forced change is counted and printed.** One format for files touched
  and lines changed.
- **How the directory listing is presented** in the README and on a slide.

**Exit:** one project passing every item in `spec.md` §9, with the architecture
test shown going red on camera.

### Phase 2 — Build the remaining four, one at a time

**One project at a time, finished completely before the next begins.**

| Order | Project | The moment to get right | Risk |
| --- | --- | --- | --- |
| 1 | `mvc-pattern` | £42.50 on screen, £42.49 in the email | Medium — the MVC/MVP/MVVM discussion can sprawl |
| 2 | `hexagonal-architecture-pattern` | The core driven by a CLI **and** backed by memory, unchanged | Medium |
| 3 | `clean-architecture-pattern` | The arrow flipping while the call goes the same way | **High — overlap with §65** |
| 4 | `clean-architecture-with-spring-pattern` | Hand-wiring failing at compile time, container wiring failing at startup | Medium — it must not become a Spring tutorial |

Three cautions, recorded now.

**Clean must not be Hexagonal again.** They are genuinely close, and four
similar videos would be the worst outcome available to this category. §66's
distinct content is: the concentric rule stated as a single sentence, the
dependency-inversion moment shown in code, the two-at-once forced change, and
the most honest "this is often too much" section in the course. If a draft of
§66 does not contain all four, it is Hexagonal with different diagrams and
should not ship.

**MVC must not become a framework tour.** The classic pattern, then a plain
statement of what a web framework actually does, then stop. MVP and MVVM get one
scene between them.

**Hexagonal must show both sides.** The driving side — the same core run from a
CLI — is the half most treatments skip, and skipping it here would make the
project ordinary.

**§67 comes last, and only after §66 is finished and published.** It is §66's
graph assembled by Spring, in its own project, and it is only legible to someone
who has already watched the hand-wiring. Three rules keep it honest: it copies
§66's entities, use cases and adapters rather than reinventing them; it re-teaches
neither Clean Architecture nor Spring, spending its time on the one contrast it
owns — compile-time wiring failure against startup wiring failure; and it writes
`docs/dependencies.md` **before** the first annotation, so Spring is explained
rather than assumed. If the schedule runs short, §67 is the project to defer:
§66 teaches the architecture completely on its own.

**Exit:** five projects complete, each verified before the next begins.

### Phase 3 — Verify the category

1. The artefact sweep from
   [`../../micro-services-design-patterns/docs/ai-session.md`](../../micro-services-design-patterns/docs/ai-session.md)
   §2, pointed here.
2. `./gradlew test` in every project, all green, including the architecture
   tests.
3. **The five-way diff.** Run the same acceptance tests against all five
   projects and confirm the observable behaviour is identical. If the
   architectures produce different output, the comparison the category rests on
   is not valid. §66 and §67 must agree exactly, since only their assembly
   differs.
4. Every forced-change count re-checked against real output.
5. Every spec regenerated **after** its video exists.
6. **Every video listened to with the screen off**, checking that no
   explanation depends on a diagram. This category fails that check most
   easily.
7. Every poster and thumbnail looked at.
8. `git status` shows no mp4, m4a, srt, wav, log, `docs/audio/` or
   `video/build/`.
9. The ten extra conformance items in `spec.md` §9 checked per project.

---

## Sequencing rules

**Finish one project before starting the next.**

**Build §72 Dependency Injection before §66 if the schedule allows.** Clean
Architecture's wiring is where DI stops being abstract, and having the project
to link to is worth more than the ordering costs. If the foundational category
has not been built, §66 explains its own wiring and links forward.

**Perform the change; do not describe it.** Every claim about cost is a counted
diff from a real run.

**Regenerate the spec last, after the video exists.**

**Any fix to the shared pipeline is rolled out to all projects.**

**Nothing is committed or pushed unless asked.** Build artefacts go to
`.gitignore`; source, documents, `animation.html`, posters, thumbnails and
rendered diagrams stay in. Commit messages carry no co-author trailer.

---

## Framework register

Any open-source framework may be used where it is genuinely needed, and every
use is accounted for here before it reaches a build file.

| Project | Tier | Dependency | Why it, rather than plain Java |
| --- | --- | --- | --- |
| all five | 1 | JUnit 5 (`5.10.x`) | The repository standard. |
| all five | 1 | **ArchUnit (`1.3.x`)** | The exception worth making, and the reason is the category's whole thesis. A dependency rule written as an ArchUnit test *is* the architecture, executably: `noClasses().that().resideInAPackage("..domain..").should().dependOnClassesThat().resideInAPackage("..infrastructure..")` reads as English, fails with the offending class named, and turns a whiteboard promise into a build failure. Hand-rolling package inspection would produce a worse message and teach reflection instead of architecture. |

| `clean-architecture-with-spring` (§67) | 1 | **Spring Boot (`3.3.x`)** | The whole subject of the project. It assembles §66's graph with a container so the reader recognises `@Component` as the twenty lines §66 wrote by hand, and so the startup-time wiring failure can be shown beside §66's compile-time one. Carries a full `docs/dependencies.md`. |

**Containers and databases are not planned in this category.** These are
structures within one application, and a container adds a deployment story that is
not the subject. That is a judgement about subject matter rather than a
restriction: if a project finds that a framework makes its architecture clearer,
take it and add a row.

**Spring appears in exactly one project, §67, and nowhere else.** Projects 63 to
66 have no framework in any build file, so a reader who wants the architectures
without the framework gets them. That separation is the whole reason §67 is its
own project rather than a scene inside §66.

### Considered, and not currently planned

**Any open-source framework is available.** This table records current judgement
rather than prohibition, so a later session does not re-derive it.

| Candidate | Current judgement |
| --- | --- |
| **Spring, inside §66 itself** | Kept out of §66 and given its own project instead, §67. The hand-wiring *is* the dependency-inversion lesson, and an annotation that does it invisibly removes the moment §66 exists for — but the container version is genuinely worth building, so it is built, separately, and §66 links to it. This row was previously a flat exclusion. |
| A web framework, for MVC | The pattern is the separation, not the routing. A plain `render()` and a plain text output show it with nothing in the way. Worth one scene naming what a real framework adds. |
| A UI toolkit, for MVP/MVVM | More setup than the single scene those variants get is worth. Revisit only if that scene proves unconvincing without one. |
| A database, anywhere | The forced changes swap stores, and an in-memory map on both sides keeps the swap visible rather than the setup. |

---

## Risks

| Risk | Mitigation |
| --- | --- |
| **The category becomes four diagram videos** | The category's defining risk, and the reason `spec.md` §2 leads with it. Three answers, all mandatory: one feature built four times, a counted forced change, and an architecture test that fails. Nothing ships that cannot be run. |
| **Clean restates Hexagonal** | Phase 2 names four pieces of content §66 must have, and says a draft without all four should not ship. |
| **Narration leans on a picture** | The hardest audio-only category in the course. `spec.md` §7 requires architecture to be spoken as rules and directions, bans "as you can see", and Phase 3 listens to every video with the screen off. |
| The videos argue for ever more structure | Every project has a mandatory "when this is too much" section, and §66's is the most emphatic. |
| The shared feature gets retrofitted | Written first, in Phase 0, with acceptance tests that are structure-agnostic. |
| The projects grow too large to read | One feature, four or five classes per layer. An architecture shown across forty classes cannot be held in the head. |
| MVC sprawls into MVP, MVVM and framework history | One scene for the variants, one plain statement of what web MVC does, then stop. |
| ArchUnit rots or changes API | Pinned. It is a test-only dependency, so a break stops a build loudly rather than misleading a reader quietly. |
| **§67 becomes a Spring tutorial** | It owns one contrast — compile-time against startup-time wiring failure — and nothing else. §66 owns the architecture. A draft that explains dependency injection from scratch has drifted into §72's territory. |
| **§67 and §66 drift apart** | §67 copies §66's entities, use cases and adapters unchanged, and the Phase 3 five-way diff requires the two to produce identical output. |
| **Spring leaks into §63 to §66** | Four of the five projects have no framework in any build file, and that is checked in Phase 3. It is the reason §67 is a separate project. |

---

## Definition of done

The category is complete when:

- [ ] Five projects exist, each passing the repository-wide conformance
      checklist and the ten extra items in `spec.md` §9.
- [ ] **All five implement the same order-placing feature**, and the shared
      acceptance tests pass against all five.
- [ ] **§67 is a project in its own right** — its own README, documents, poster,
      thumbnail and video — naming §66 in its first paragraph, while §66 links
      forward to it.
- [ ] **Spring appears in no build file except §67's**, and §67 carries a
      `docs/dependencies.md` written for someone who has never used it.
- [ ] **Every project has an architecture test that fails when the rule is
      broken**, and the video shows it failing.
- [ ] Every forced change has been performed and its cost counted from real
      output.
- [ ] Every project builds and tests pass in under two seconds.
- [ ] Every README opens with its directory listing.
- [ ] Every video is rendered, printed `audio timeline continuous`, runs between
      eleven and thirteen minutes, and **has been listened to with the screen
      ignored**.
- [ ] Every poster and thumbnail has been looked at.
- [ ] Every explainer has its "when this is too much" section, and every video
      says it aloud.
- [ ] All specs across the repository regenerate clean.
- [ ] The root `README.md`, `gradle-java/README.md` and the repository-wide spec
      all describe the category.
