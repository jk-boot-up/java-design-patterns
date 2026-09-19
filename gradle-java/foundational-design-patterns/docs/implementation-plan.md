# Foundational Patterns — Implementation Plan

How the five projects in this category get built. [`spec.md`](spec.md) fixes what
they are; this fixes the order, the rules that keep the build from redoing
itself, and what "finished" means.

**All five projects are built.** One deliberate difference from this plan: Dependency
Injection writes a small container in plain Java rather than running Spring Boot.

---

## Current state

| | |
| --- | --- |
| Projects specified | 5 |
| Projects built | 9 (five by hand, four with a framework or infrastructure) |
| Category registered with the shared generators | yes |
| Existing projects in the repository | 68 built (37, plus 5 architectural, 6 concurrency, 11 enterprise and these 9) |

---

## Order of work

### Phase 0 — Wire the category in, and settle the shared collaborators

**Tooling.** Add `foundational-design-patterns` to `CATEGORIES` in
`gradle-java/docs/make_narration.py`, and add all five slugs to the per-project
tables in `make_specs.py`, `make_thumbnails.py` and `make_youtube_docs.py` —
those three carry their own tables and **silently skip anything missing**. Then
register the category in `gradle-java/README.md`, the root `README.md` and
`docs/video-and-publishing-spec.md`.

**The three collaborators.** Projects 70, 71 and 72 are three answers to one
question, so they must ask the same question in the same words. Settle once: a
`DiscountPolicy`, a `PaymentGateway` and a `Notifier`, with the same interfaces
and the same checkout using them. Then the three projects differ only in how the
checkout gets hold of them, and a reader can compare them directly.

Settle the deep constructor chain too — the six levels §70's naive version
collapses — because all three projects refer to it.

**Exit:** the tooling lists the category with zero projects, and the three
interfaces, the checkout and the constructor chain exist in one place ready to
be copied.

### Phase 1 — Build Null Object end to end, as the category's reference

It goes first because it is the smallest and most self-contained of the five, and
because its structure is the one all five share: a naive version, a pattern, and
a bill heavy enough to change the recommendation.

Two things this phase settles for everyone after it:

- **How a verdict is delivered.** Every project in this category ends with a
  plain position — use this, use it narrowly, or prefer the alternative. The
  tone is set here: direct, reasoned, not hedged and not strident.
- **How an alternative is treated fairly.** §68 recommends `Optional` in many
  cases, which means the project argues partly against its own title. Getting
  that right once makes §69 and §71 straightforward.

**Exit:** one project passing every item in `spec.md` §9.

### Phase 2 — Build the remaining four, one at a time

**One project at a time, finished completely before the next begins.**

| Order | Project | The evidence it must produce | Risk |
| --- | --- | --- | --- |
| 1 | `object-pool-pattern` | Pooling a small object being **slower** than allocating one | Medium — the benchmark must be sound |
| 2 | `registry-pattern` | A test failing because of the order the tests ran in | Low |
| 3 | `service-locator-pattern` | The compiler saying nothing while a dependency is missing | Medium — tone |
| 4 | `dependency-injection-pattern` | Twenty lines of hand-wiring, then the same graph in a container | **Medium — scope** |

Four cautions, recorded now.

**§69's benchmark must be defensible.** "Pooling is slower than allocating" is a
strong claim and a JVM microbenchmark is easy to get wrong — dead-code
elimination, no warm-up, allocation hoisted out of the loop. Either warm up
properly and measure carefully with the method documented in the README, or make
the claim qualitatively with allocation counts instead of timings. Do not ship a
number that a knowledgeable viewer can dismantle in the comments, because the
project's authority rests on exactly that number.

**§71 must argue, not sneer.** Service Locator was a reasonable answer to a real
problem and is still correct for plugin systems and `ServiceLoader`. The project
shows its failures as runnable evidence and then gives its verdict. A video that
mocks a pattern teaches contempt rather than judgement.

**§72 must not become a Spring tutorial.** Hand-wiring first, always, with the
line count stated. The container is one scene near the end whose only job is
recognition. If the script is running long, the container scene is what is
wrong with it.

**§72 should ideally be built before the architectural category's §66**, so
Clean Architecture can link to it rather than explaining injection itself. If
the schedule does not allow it, §66 explains its own wiring and links forward.

**Exit:** five projects complete, each verified before the next begins.

### Phase 3 — Verify the category

1. The artefact sweep from
   [`../../micro-services-design-patterns/docs/ai-session.md`](../../micro-services-design-patterns/docs/ai-session.md)
   §2, pointed here.
2. `./gradlew test` in every project, all green, offline.
3. **The three-way comparison.** Projects 70, 71 and 72 solve the same problem
   with the same collaborators. Diff them and confirm that only the acquisition
   mechanism differs. If they have drifted, the argument the three make together
   does not hold.
4. Every benchmark number re-checked, with its method written down.
5. Every spec regenerated **after** its video exists.
6. Every video printed `audio timeline continuous`, and every one listened to.
7. Every poster and thumbnail looked at — and for §69 and §71 specifically,
   checked that the poster does not promise a technique the video advises
   against.
8. `git status` shows no mp4, m4a, srt, wav, log, `docs/audio/` or
   `video/build/`.
9. The six extra conformance items in `spec.md` §9 checked per project.

---

## Sequencing rules

**Finish one project before starting the next.**

**Give the verdict; do not hedge.** Three of these patterns are contested and
the reader is here for a position. "It depends" is only acceptable with the
dependency named.

**Run the demo before quoting it.** Every number comes from real
`./gradlew run` output, and every benchmark carries its method.

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
| `null-object`, `registry`, `service-locator` | 1 | **nothing else** | Each pattern is a dozen lines. A library would be larger than the subject. |
| `object-pool` | 1 | **nothing else**, with a caveat | See below. |
| `dependency-injection` | 2 | Spring Boot (`3.3.x`) | The container is how every reader has met this pattern. Recognition is the scene's whole job. |
| `dependency-injection-with-spring` | own project | Spring Boot (`4.1.1`), the container only | Built as a project of its own, after its hand-built partner. |
| `registry-with-spring` | own project | Spring Boot (`4.1.1`), its test support | The test-context cache is Spring's own version of the registry's order dependence. |
| `object-pool-with-hikaricp` | own project | HikariCP, H2, `slf4j-nop`, versions from Spring Boot 4.1.1's bill of materials | The mature answer to the hand-built pool's costs, over real JDBC. |
| `service-locator-with-consul` | own project | **A real Consul agent, run as a local process**; **Docker, running `nginx:1.31.5-alpine`**; no Java library beyond the JDK | Real service discovery needs a real agent, and server-side discovery needs a real proxy. |

**Infrastructure used by `service-locator-with-consul`.** Consul runs in development mode as a child process on
ports chosen at run time and is stopped when the run ends. nginx runs in a container named
`locator-demo-nginx`, started and removed by the project, which touches no other container. Both are optional
for anyone reading: the tests are skipped, not failed, when `consul` is not on the PATH or Docker and the image
are unavailable, and `docs/dependencies.md` says so. Act five relies on Docker Desktop providing
`host.docker.internal`.

**The Object Pool caveat.** JMH is the correct tool for the benchmark in §69 and
is available if needed. It is not the first choice only because it changes the
project layout, needs an annotation processor, and runs for minutes, which sits
badly with the two-second test budget — so if it is taken, it belongs in a
separate source set that `./gradlew test` does not run. First try: §69 measures
carefully by hand with warm-up and documents the method in its README, or makes
its claim with allocation counts rather than wall-clock timings. If neither is
convincing in a draft, the honest fallback is to state the claim qualitatively
and cite the JVM's escape analysis and generational collector rather than to
show a number that cannot be defended.

### Considered, and not currently planned

**Any open-source framework is available.** This table records current judgement
rather than prohibition. If a draft shows one of these earning its place, take it
and update the row.

| Candidate | Current judgement |
| --- | --- |
| Guice or Dagger, in §72 | One container is enough for recognition and Spring is the one the audience has. A sentence naming the alternatives costs nothing; a second container adds no new idea. |
| Apache Commons Pool, in §69 | Worth taking in the one place the project recommends pooling — connections — precisely because it shows the mature answer to the leak-and-dirty-object problems the demo just produced. Do not use it to pool ordinary objects, which is the practice §69 argues against. |
| JMH | See the caveat above. If the hand-rolled measurement is not convincing in a draft, JMH in a separate source set is a better outcome than a number that cannot be defended. |
| A mocking framework | Hand-written fakes are readable and this category's classes are tiny. No objection where one genuinely helps. |

---

## Risks

| Risk | Mitigation |
| --- | --- |
| **§69's benchmark is wrong and gets dismantled publicly** | The project's authority rests on that number. Warm up, document the method, or drop to allocation counts. A qualitative claim beats an indefensible measurement. |
| **§71 reads as contempt** | It shows evidence and then gives a verdict, and it names where the pattern is still right — plugin systems, `ServiceLoader`. |
| **§72 becomes a Spring tutorial** | Hand-wiring first with the line count stated; the container gets one scene whose job is recognition. |
| The three acquisition projects drift apart | The collaborators are settled in Phase 0 and the three-way diff is a Phase 3 check. |
| Posters promise what the videos argue against | Checked explicitly in Phase 3 for §69 and §71. Honest titles; no bait-and-switch. |
| §70 restates Singleton (§4) | It links to it and says plainly that a registry inherits every one of §4's problems, then spends its time on what is different: many things, looked up by key, registered at runtime. |
| The category reads as leftovers | `spec.md` §1 gives it a subject — how an object gets hold of another object — and the last three projects form one argument with a conclusion. |
| Scheduling against §66 | §72 before §66 is preferable but not required; either order works with a forward link. |

---

## Definition of done

The category is complete when:

- [ ] Five projects exist, each passing the repository-wide conformance
      checklist and the six extra items in `spec.md` §9.
- [ ] **Every project ends with a plain verdict**, and every video says it
      aloud.
- [ ] The three acquisition projects use the same collaborators and can be
      diffed against each other.
- [ ] **§69's performance claim is either carefully measured with its method
      documented, or stated qualitatively** — never an undefended number.
- [ ] §72 shows hand-wiring before any container, with the line count stated.
- [ ] Every project builds, tests pass in under two seconds, offline.
- [ ] Every video is rendered, printed `audio timeline continuous`, runs between
      eleven and thirteen minutes, and has been listened to.
- [ ] Every poster and thumbnail has been looked at, and none promises a
      technique its video advises against.
- [ ] All specs across the repository regenerate clean.
- [ ] The root `README.md`, `gradle-java/README.md` and the repository-wide spec
      all describe the category.
