# Enterprise Application Patterns — Implementation Plan

How the eleven projects in this category get built. [`spec.md`](spec.md) fixes
what they are; this fixes the order, the rules that keep the build from redoing
itself, and what "finished" means.

**Nothing here is built yet.** This document and [`spec.md`](spec.md) are the
whole category at the time of writing.

---

## Current state

| | |
| --- | --- |
| Projects specified | 11 (seven patterns by hand; four of them again in the framework) |
| Projects built | 0 |
| Category registered with the shared generators | no |
| Existing projects in the repository | 37 built; 14 more specified across the platform and concurrency categories |

---

## Order of work

### Phase 0 — Wire the category in, and settle the shared toy database

Two jobs, and the second is the one that saves the most rework.

**Tooling.** Add `enterprise-design-patterns` to `CATEGORIES` in
`gradle-java/docs/make_narration.py`, and add all eleven slugs to the per-project
tables in `make_specs.py`, `make_thumbnails.py` and `make_youtube_docs.py` —
those three carry their own tables and **silently skip anything missing**. Then
register the category in `gradle-java/README.md`, the root `README.md` and
`docs/video-and-publishing-spec.md`.

**The toy database.** All seven hand-built projects need the same thing: an in-memory store
that behaves enough like a database to make the patterns real. Settle it once,
then copy it into each project — the repository has no shared library and should
not grow one.

It needs exactly five properties, and no more:

1. **Rows, not objects.** A table is a map from id to a map of column values. If
   it stores objects, Data Mapper has nothing to do and the category collapses.
2. **A visible operation counter.** Every insert, update and select is counted
   and printable. This is how N+1 is shown and how every quoted number is
   produced.
3. **An explicit `flush()`.** Nothing is written until asked, which is what
   makes Unit of Work demonstrable.
4. **Failure on demand.** A table that can be told to reject the next write, so
   "the third stock update fails" is deterministic.
5. **No threading.** Concurrency belongs to the concurrency category. This one
   is single-threaded throughout.

Also settle the four domain classes — `Customer`, `Product`, `Order`,
`OrderLine` — and the seeded data, once, so all seven projects tell one story
with the same customer ids.

**Exit:** the tooling lists the category with zero projects; the toy database
and the four domain classes exist, are tested, and live in the reference
project ready to be copied.

### Phase 1 — Build Data Mapper end to end, as the category's reference

It goes first because the whole category assumes it — every later pattern
presumes objects and rows are separate things. Build it complete and treat the
result as the template.

Three things this phase settles for everyone after it:

- **How Active Record is treated.** It is the naive version in §52 and it must
  be shown working well before its cost appears. The tone set here governs every
  other project's naive version, and `spec.md` §9 makes fairness a conformance
  item.
- **How the toy database's operations are printed.** One format for query
  counts, used by all eleven.
- **The "Where you have already met this" section.** Length, tone, and where it
  sits.

**Exit:** one project passing every item in `spec.md` §9, and a one-scene `real/`
demo that shows the generated SQL beside the hand-written mapper.

Because Data Mapper's `real/` demo is the first JPA one, it also settles the
framework conventions everything after it copies: how H2 and Hibernate are
pinned, how a framework demo is filmed, and what a `docs/dependencies.md` looks
like. Projects 59 to 62 inherit all of it.

### Phase 2 — Build the remaining six hand-built projects, one at a time, in learning order

**One project at a time, finished completely before the next begins.**

| Order | Project | The moment to get right | Framework material | Risk |
| --- | --- | --- | --- | --- |
| 1 | `identity-map-pattern` | The lost address change, then `==` being true | A whole project, §59 | Low |
| 2 | `unit-of-work-pattern` | The half-written order, and nothing to undo it with | A whole project, §60 | Low |
| 3 | `lazy-load-pattern` | N+1 printed as 21 queries for 20 orders | A whole project, §61 | Medium |
| 4 | `repository-pattern` | Swapping the store with no change to the caller | A whole project, §62 | Medium |
| 5 | `service-layer-pattern` | The second entry point, and the logic that drifted | One scene, `@Service` | **High — vagueness** |
| 6 | `dto-pattern` | The password hash in the JSON | One scene, Jackson at a REST boundary | Low |

Three cautions, recorded now because each is discovered late otherwise.

**Lazy Load is the category's best video and should be given the most care.**
`LazyInitializationException` is among the most-searched Java errors there is,
and this project explains it from its mechanism instead of offering the usual
workaround. Budget accordingly.

**Service Layer is the one that can go vague.** "Put business logic in a service"
is advice, not a pattern, and a project that says only that is not worth making.
Its concrete anchor is the second entry point: build the CLI, copy the logic,
show the drift, then extract. And it must name the Anemic Domain Model and give
an honest dividing line rather than pretending the boundary is obvious.

**Repository must not become CQRS.** The read/write split belongs to §34 and is
linked, not re-taught.

**Exit:** seven hand-built projects complete, each verified before the next
begins.

### Phase 2a — Build the four framework projects, one at a time

These are §59 to §62, and they come **after all seven hand-built projects are
finished and published**, in the order their partners were built.

| Order | Project | Pairs with | The moment to get right | Risk |
| --- | --- | --- | --- | --- |
| 1 | `identity-map-with-jpa-pattern` | §53 | `first == second`, then two contexts making it false | Low |
| 2 | `unit-of-work-with-spring-pattern` | §54 | The checked exception that commits, and the flush nobody wrote | Medium |
| 3 | `lazy-load-with-hibernate-pattern` | §55 | A real `LazyInitializationException`, then the three fixes and their costs | **Medium–High** — the best video in the category |
| 4 | `repository-with-spring-data-pattern` | §56 | Deleting the implementation and the application still running | Medium |

Five rules govern all four, and they are what keep a framework project from
turning into a framework tutorial:

1. **Copy the partner's domain unchanged.** Same classes, same seeded customers,
   same scenario, same numbers. Only the mechanism differs, and the comparison is
   worthless if anything else moved.
2. **Do not re-teach the pattern.** The partner owns it. Open by naming the
   partner in the first sentence, then spend the whole project on the one thing
   this version adds.
3. **Write `docs/dependencies.md` before the first annotation**, so Hibernate and
   Spring are explained rather than assumed, and so the explanation is the plan
   rather than an afterthought.
4. **Lead with the failure, not the feature.** Each of these projects has one
   concrete thing that goes wrong — a detached entity, a swallowed rollback, a
   closed session, a leaked managed entity — and that is the reason the project
   exists. A draft that only demonstrates convenience has missed its subject.
5. **Keep the framework out of the partner.** Nothing in §52 to §58's build files
   changes when these are built.

If the schedule runs short, defer from the bottom of the table upward. §61 is the
one to protect: it explains the most-searched exception in Java from its
mechanism, and nothing else in the course is positioned to do that.

**Exit:** eleven projects complete, each verified before the next begins.

### Phase 3 — Verify the category

1. The artefact sweep from
   [`../../micro-services-design-patterns/docs/ai-session.md`](../../micro-services-design-patterns/docs/ai-session.md)
   §2, pointed here.
2. `./gradlew test` in every project, **with no database installed and no
   network**, all green.
3. Every query count quoted in a README, a slide or a narration line re-checked
   against real run output.
4. Every spec regenerated **after** its video exists.
5. Every video printed `audio timeline continuous`, and every one listened to.
6. Every poster and thumbnail looked at.
7. `git status` shows no mp4, m4a, srt, wav, log, `docs/audio/` or
   `video/build/`.
8. The nine extra conformance items in `spec.md` §9 checked per project.
9. **The four pairings diffed.** Each framework project's domain classes and
   seeded data must match its partner's exactly. If they have drifted, the
   comparison the pairing rests on is not valid.
10. **`grep` the build files of projects 52 to 58** and confirm no framework
    appears in any of them.

---

## Sequencing rules

**Finish one project before starting the next.**

**Build the hand-built project first and completely, including the video**, then
its framework partner as a separate project. A Hibernate problem must never block
a project that does not need Hibernate to teach its pattern, and keeping the two
in separate projects is what guarantees that.

**Run the demo before quoting it.** Every number — especially every query count
— comes from real `./gradlew run` output.

**Regenerate the spec last, after the video exists.**

**Any fix to the shared pipeline is rolled out to all projects.**

**Nothing is committed or pushed unless asked.** Build artefacts go to
`.gitignore`; source, documents, `animation.html`, posters, thumbnails and
rendered diagrams stay in. Commit messages carry no co-author trailer.

---

## Framework register

Any open-source framework may be used, and every use is accounted for here
before it reaches a build file. This category has the strongest case in the
course, because recognising the pattern inside the framework is half of what it
teaches.

The register is a map, not a gate. The one structural constraint is where a
framework may live: **the seven hand-built projects stay framework-free, and the
framework version is built as a project of its own.** Both halves matter. A
library inside the hand-built project would hide the mechanism that is the
lesson — but leaving the framework out altogether would be worse, because
recognising the pattern inside Hibernate and Spring is half of what this category
teaches. So both versions get built, separately, and each uses the real framework
a reader will meet at work rather than a simplified stand-in. This replaces an
earlier rule that kept the framework out of Tier 1 without building it anywhere
as a project of its own.

Versions are indicative and get fixed at Phase 0 in one shared catalogue; the
reasons are not negotiable.

| Project | Where | Dependency | Why it, rather than plain Java |
| --- | --- | --- | --- |
| all eleven | main | JUnit 5 (`5.10.x`) | The repository standard. |
| §52 to §58 | main | **nothing else** | The hand-built mechanism is the lesson. A library here would hide it, and a reader who wants the mechanism alone gets it. |
| §59 `identity-map-with-jpa` | main | Hibernate (`6.5.x`), H2 (`2.2.x`) | The persistence context *is* the pattern; nothing else demonstrates it, and the detached-entity failure needs a real one. |
| §60 `unit-of-work-with-spring` | main | Spring Boot (`3.3.x`), H2 | `@Transactional` is the pattern as most readers meet it, and its surprises — the checked exception that commits, the unexpected flush — are Spring's own. |
| §61 `lazy-load-with-hibernate` | main | Hibernate, H2 | A genuine `LazyInitializationException` cannot be faked convincingly, and faking it would defeat the project. |
| §62 `repository-with-spring-data` | main | Spring Data JPA (`3.3.x`), H2 | An interface with no implementation, after building one by hand. |
| §52 `data-mapper` | `real/` demo | Hibernate, H2 | Real generated SQL beside a hand-written mapper, for one scene. |
| §57 `service-layer` | `real/` demo | Spring Boot | `@Service` and where the transaction boundary is drawn, for one scene. |
| §58 `dto` | `real/` demo | Spring Boot, Jackson (via the Boot BOM) | The entity-versus-DTO problem is a serialisation problem, for one scene. |

The `real/` demos sit in a subdirectory excluded from the root
`settings.gradle`, so `./gradlew test` never reaches them. The four framework
projects are ordinary projects and their tests do run — they are the project.

H2 runs in memory and needs no installation, which is why it is the database
everywhere here rather than Postgres in a container. A reader with a JDK and a
warm Gradle cache can run every project in this category, including the four
framework ones — which is what makes it reasonable to ship them as projects
rather than as optional extras.

### Considered, and not currently planned

**Any open-source framework is available.** This table records the current
judgement on candidates that came up, so a later session does not re-derive the
same reasoning. None of it is a prohibition — if a draft shows one of these
earning its place, take it and update the row.

| Candidate | Current judgement |
| --- | --- |
| MapStruct, in the DTO project | It generates the mapping code, which is exactly the cost §58 exists to make visible. The sequence that works: show the tedium by hand, then show MapStruct removing it. Taking it *after* the cost has landed is a good outcome, not a compromise. |
| Lombok | Saves typing, costs a reader who then has to know what was generated. Java records cover most of it already. |
| A real Postgres in a container | H2 in memory teaches the same patterns with none of the setup, and keeps every Tier 2 runnable from a JDK and a warm cache. The container permission exists; this is a case where not using it serves the reader better. Worth revisiting only if a pattern turns on database-specific behaviour. |
| jOOQ, MyBatis | Alternative answers to §52 rather than the pattern itself. Worth naming in a scene; a project each would be a different course. |
| A mocking framework | Hand-written fakes over the toy database are readable by a beginner. No objection where a Tier 2 test genuinely needs one. |

---

## Risks

| Risk | Mitigation |
| --- | --- |
| **Service Layer becomes vague advice** | The highest-risk project in the category, flagged in Phase 2. Its anchor is the concrete second entry point and the drift it causes, plus a named position on the Anemic Domain Model. |
| **The toy database grows into a real one** | Five properties, listed in Phase 0, and no more. If it needs a query planner, the project has gone wrong. |
| The naive versions become straw men | A conformance item. Active Record is good for small applications; SQL in a service is fine in a script. Say so. |
| Tier 2 rots — Hibernate or Spring Boot majors land | Pinned in one shared catalogue; never on the path of `./gradlew test`. |
| Repository restates CQRS (§34) | Linked, not re-taught. |
| DTO restates Backends for Frontends (§40) | Same decision at a different layer; the projects link and each says which layer it is at. |
| The category reads as a Spring tutorial | Seven of the eleven projects have no framework at all, and each of the four that do is pinned to one contrast and one failure. Rule 2 of Phase 2a — do not re-teach the pattern, do not teach the framework — is the check. |
| **A framework project repeats its partner** | Each opens by naming its partner and leads with a failure the partner cannot show. If a draft's most interesting moment is one the partner already had, it should not ship. |
| **A pairing drifts apart** | The framework project copies its partner's domain and seeded data unchanged, and Phase 3 diffs the four pairs. |
| **A framework leaks into a hand-built project** | Phase 3 greps the build files of §52 to §58. It is the reason §59 to §62 are separate projects. |
| Eleven full projects is a large amount of work | Roughly a week each including the render, though §59 to §62 are cheaper because they inherit their partner's domain, scenario and numbers. The one-at-a-time rule means the category is useful at any point, and the four framework projects are ordered so that deferring from the bottom of the Phase 2a table costs least. |

---

## Definition of done

The category is complete when:

- [ ] Eleven projects exist, each passing the repository-wide conformance
      checklist and the nine extra items in `spec.md` §9.
- [ ] **Every one of §52 to §58 passes with no database installed and no
      network**, and no framework appears in any of their build files.
- [ ] **Each of §59 to §62 is a project in its own right** — its own README,
      documents, poster, thumbnail and video — naming its partner in its first
      paragraph, using that partner's domain unchanged, and carrying a
      `docs/dependencies.md` written for someone who has never used Hibernate or
      Spring.
- [ ] Every `real/` demo and every framework project runs from a single command
      on a machine that has never built it.
- [ ] Every project builds, tests pass in under two seconds, and its README
      quotes real run output including the query counts.
- [ ] Every dependency and every version appears in the framework register and
      matches what the build files declare.
- [ ] Every video is rendered, printed `audio timeline continuous`, runs between
      eleven and thirteen minutes, and has been listened to.
- [ ] Every poster and thumbnail has been looked at.
- [ ] Every explainer has its "Where you have already met this" section, and
      every video says it aloud.
- [ ] All specs across the repository regenerate clean.
- [ ] The root `README.md`, `gradle-java/README.md` and the repository-wide spec
      all describe the category.
