# Behavioural Patterns — Implementation Plan

How the eleven projects specified in [`spec.md`](spec.md) were built.

**All eleven are now complete**, so this document is a record rather than a
forecast: it is kept in the present tense because the sequence it describes is
the one to follow when a twelfth project is added or an existing one is rebuilt.
The state of the category as delivered is at the bottom, under
[Definition of done](#definition-of-done).

This is the *how*. The *what* is in `spec.md`, and the video and publishing
standard both inherit from is
[`../../docs/video-and-publishing-spec.md`](../../docs/video-and-publishing-spec.md).

---

## Starting state

At the time this plan was written, nothing existed: `gradle-java/behavioural/`
contained this `docs/` directory and no projects.

That was the significant difference from the plan that built the other fourteen:
that one was a remediation, bringing existing projects up to a standard written
after the fact. This one has the standard first, so every project can be
correct on the first pass and nothing needs re-rendering. The cost of getting
it wrong is high — a project that has to be re-narrated costs a full rebuild —
so the sequencing below front-loads the decisions that are expensive to change.

---

## Order of work

### Phase 0 — Wire the category into the shared tooling

Before any project is written, because all eleven depend on it and because
doing it later means editing eleven projects instead of four files.

1. **`docs/video-and-publishing-spec.md`** — §1 Scope currently reads
   "Fourteen projects" with a two-row table. It becomes twenty-five, with a
   Behavioural row listing the eleven, and a pointer to
   `behavioural/docs/spec.md` for the category detail.
2. **`docs/make_specs.py`** — eleven entries appended to `ORDER` and to
   `NAMES`. The per-project `META` block, which carries the role table and
   therefore the real class names, cannot be written before the project
   exists; it lands with the project in Phase 1 or 2. All three generators
   therefore skip a project in `ORDER` whose directory is not present yet,
   rather than failing, so the series can be listed in full from the start.
3. **`docs/make_youtube_docs.py`** — eleven title and tag entries, from
   `spec.md` §6.
4. **`docs/make_thumbnails.py`** — eleven entries.
5. **Root `README.md`** — the behavioural category and its learning order.

Phase 0 is done when all three generators still run clean over the existing
fourteen, and each reports the eleven new slugs as "not built yet" rather than
erroring.

### Phase 1 — Build Strategy end to end, as the category's reference

Strategy is first in the learning order and is the simplest of the eleven, so
it is the right project to shake out the template on. It is built **complete**
— code, tests, all ten documents, both diagrams, the animation, the video —
and reviewed before anything else starts.

Everything that is going to be copied eleven times gets settled here: the
`build_video.sh` derived from abstract-factory's, the `make_slides.py`
palette and layout, the scene structure, the `README.md` shape, the
`session.md` shape. A defect fixed at this point is fixed once; the same defect
found at project nine has to be fixed nine times, which is exactly how the
proxy poster shipped reading "DECORATOR PATTERN".

### Phase 2 — Build the remaining ten, in learning order

Observer, Command, Template Method, State, Chain of Responsibility, Iterator,
Mediator, Memento, Visitor, Interpreter.

In order, and one at a time, because the cross-references in `spec.md` §4 read
forward: State refers back to Strategy, Mediator back to Observer, Memento back
to Command. Building out of order means writing those references against
projects that do not exist yet.

The videos themselves carry no such forward reference. No end screen names the
pattern that comes next, because YouTube publishing order is not the build
order and a rendered video cannot be corrected without re-uploading it.

Per project, in this sequence — the code first, because every other artefact
quotes it, and the video last, because it is the only step that is expensive
to redo:

1. Design the domain model against `spec.md` §3. Confirm the naive alternative
   is one a competent developer would actually write; a straw man invalidates
   the whole comparison.
2. Scaffold the Gradle project from the previous one.
3. Write the production code and the naive counter-example classes.
4. Write the tests, including the interaction assertions §5.2 requires.
5. `./gradlew build`, then `./gradlew run`, and quote the real output in the
   top-level `README.md`.
6. Write `docs/` — problem statement, explainer, both diagrams, the animation,
   prerequisites, session plan. Render both Mermaid diagrams to PNG.
7. Write the assigned cross-reference from `spec.md` §4.
8. Write `video/scenes.py` and `make_slides.py`. Render the poster and
   **look at it**.
9. `./build_video.sh`. Confirm it prints `audio timeline continuous`.
10. `python3 ../../docs/make_youtube_docs.py <slug>` and
    `python3 ../../docs/make_specs.py <slug>`.
11. Walk the project's conformance checklist — the repository-wide fourteen
    plus the four in `spec.md` §7.

### Phase 3 — Verify the category

Once all eleven exist, the same sweep that closed out the other fourteen: build
and run all eleven, confirm narration rate and filter chain across every build
script, confirm every poster shows its own pattern name, confirm every
`youtube.md` chapter list matches its current `.srt`, and measure loudness on
every delivered MP4.

Then regenerate all twenty-five specs so the cross-category numbers are
consistent, and update the root `README.md`.

---

## Sequencing rules

**Nothing is rendered twice.** Everything that changes what a video *contains*
— narration text, slide content, the code being shown — lands before
`build_video.sh` is run for that project. This is why the video is step 9 of
11 rather than step 3.

**Listen to the first build of each project.** The continuity self-check
verifies that no audio is missing; it cannot hear that the audio is bad. It
passed cleanly for weeks while `afftdn` was warbling the voice across the whole
repository.

**Look at every poster.** Same reason, visually: `poster.png` is generated,
its correctness is not checked by anything, and it is the single most visible
artefact the project produces.

**Do not batch the videos.** Rendering eleven at the end is tempting because
each takes several minutes, but it defers the discovery of a systematic
narration or slide problem until every project has one.

---

## Risks

| Risk | Mitigation |
| --- | --- |
| The eleven projects blur together — same story, different nouns | The scenarios in `spec.md` §3 are deliberately drawn from different parts of the store: shipping, order events, the cart, fulfilment, the order lifecycle, checkout screening, catalog search, the checkout page, saved carts, catalog reporting, promotions. No two projects share a primary subject. |
| Template Method reads as a re-run of Factory Method | The distinction is a required section in both projects, not an aside. `spec.md` §3.4. |
| State reads as a re-run of Strategy | Same. `spec.md` §3.5. |
| Visitor's dependency on Composite drifts | Visitor reuses Composite's domain shape verbatim. If Composite changes, Visitor is rebuilt. |
| Interpreter is weak and shows it | It is last, and leads with why you probably should not use it. `spec.md` §3.11. |
| A shared-tooling defect propagates to all eleven | Phase 1 builds one project completely and reviews it before the other ten start. |

---

## Definition of done

The category is complete when:

- [x] Eleven projects exist, each passing the repository-wide conformance
      checklist and the four category items in `spec.md` §7.
- [x] Every project builds, tests pass, and its README quotes real run output.
- [x] Eleven videos are rendered, each having printed
      `audio timeline continuous`, each listened to at least once.
- [x] Eleven posters and thumbnails have been looked at.
- [x] All twenty-five projects' `spec.md` / `spec.html` regenerate clean.
- [x] The root `README.md` and the repository-wide spec both describe
      twenty-five projects across three categories.

As delivered: eleven projects, runtimes from 10:07 to 13:57, every MP4
measuring between -16.00 and -16.02 LUFS, and `./gradlew test` green in all
eleven. The one file-set audit worth repeating before a release is the loop over
`behavioural/*-pattern` that checks for the seventeen required files per
project; it currently reports nothing missing.
