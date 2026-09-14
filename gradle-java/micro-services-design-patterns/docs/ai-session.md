# AI Session Handover — Microservices Category

This document exists so that an AI session working on this repository can be stopped at any
point and picked up later, by a different session with no memory of the earlier one, without
having to re-derive the state of the work or rediscover the conventions.

Read this first, then [`ai-build-spec.md`](ai-build-spec.md) for the mechanics of building a
project, then [`spec.md`](spec.md) for what each of the twelve projects is supposed to teach.

**Companion documents.** [`spec.md`](spec.md) is the category's content specification: the
twelve scenarios, the one-JVM rule, and the conformance checklist. [`implementation-plan.md`](implementation-plan.md)
is the build plan, now a record of a finished build with its definition-of-done ticked.
[`ai-build-spec.md`](ai-build-spec.md) is the toolchain: exact commands, file shapes, and the
traps that have actually cost time.

---

## 1. Current state

**The category is complete.** All twelve projects are built, tested, documented, rendered and
committed. There is no outstanding work item from the original plan.

| | |
| --- | --- |
| Projects in this category | 12 |
| Projects in the repository | 37, across four categories |
| Tests | passing in all 12; none uses `Thread.sleep` |
| Videos | 12 rendered, all present on disk, none in git |
| Specs | all 37 regenerate clean |
| Working branch | `design_patterns_part_1` |

The twelve projects, in the learning order fixed by [`spec.md`](spec.md) §1:

| # | Project | Scene count | Runtime |
| --- | --- | --- | --- |
| 26 | `api-gateway-pattern` | 15 | 17:38 |
| 27 | `service-discovery-pattern` | 16 | 17:39 |
| 28 | `load-balancing-pattern` | 16 | 18:31 |
| 29 | `retry-pattern` | 16 | 16:12 |
| 30 | `circuit-breaker-pattern` | 16 | 18:06 |
| 31 | `bulkhead-pattern` | 16 | 17:18 |
| 32 | `database-per-service-pattern` | 16 | 17:26 |
| 33 | `api-composition-pattern` | 16 | 18:05 |
| 34 | `cqrs-pattern` | 16 | 17:26 |
| 35 | `saga-pattern` | 16 | 18:21 |
| 36 | `transactional-outbox-pattern` | 16 | 10:36 |
| 37 | `idempotent-consumer-pattern` | 16 | 10:52 |

Every video measures within 0.02 LU of the −16 LUFS target, which is the figure YouTube
normalises to.

The last two projects are noticeably shorter than the other ten. That is a deliberate change
of pace rather than an omission: they were written tighter, and the tighter ones are the
better watch. If the earlier ten are ever revised, shortening them is an improvement, not a
regression.

---

## 2. How to establish state at the start of a session

Do not trust this document's claims about what is finished. It is a snapshot, and the tree
may have moved since. Run the checks instead. From this directory:

```bash
# every project has its full artefact set
for d in *-pattern; do
  s="${d%-pattern}"; miss=""
  for f in docs/problem-statement.md "docs/$s-pattern-explained.md" docs/class-diagram.md \
           docs/uml-diagram.md docs/prerequisites.md docs/session.md docs/animation.html \
           docs/make_animation_audio.sh docs/youtube.md docs/thumbnail.png docs/spec.md \
           docs/images/class-diagram.png docs/images/uml-diagram.png \
           video/scenes.py video/make_slides.py video/build_video.sh video/make_subtitles.py \
           video/narration.md video/README.md video/poster.png README.md; do
    [ -f "$d/$f" ] || miss="$miss $f"
  done
  [ -z "$miss" ] && echo "$d: complete" || echo "$d: MISSING$miss"
done

# every project builds and tests
for d in *-pattern; do (cd "$d" && ./gradlew -q test >/dev/null 2>&1) \
  && echo "$d: PASS" || echo "$d: FAIL"; done

# no rendered media has leaked into the git surface
git status -uall --short . | grep -Ei '\.(mp4|m4a|srt|wav|aac|log)$|docs/audio/|video/build/'
```

A fourth check is worth running because it has caught a real defect: a `spec.md` that reports
`0 scenes` or `not yet built` was generated before its video existed and is stale.

```bash
for d in *-pattern; do
  printf "%-32s %s\n" "$d" "$(grep -oE '[0-9]+ scenes' "$d/docs/spec.md" | head -1)"
done
```

---

## 3. Standing instructions from the repository owner

These are not preferences to be re-litigated. They have been stated explicitly and they
override any default behaviour or any convention imported from another project.

### Committing and the git surface

- **Nothing is committed or pushed without being asked.** Build artefacts are added to
  `.gitignore`; source and documentation are kept out of it.
- **Rendered output never enters the repository.** The mp4, m4a, srt and wav next to each
  video, everything under `video/build/`, and the generated `docs/audio/` narration clips are
  all ignored. They regenerate from committed scripts. A single video is 24–42 MB, and twelve
  of them would collide with GitHub's file-size limits.
- **`animation.html` is committed.** It is source, not output.
- **`video/poster.png` and `docs/thumbnail.png` are committed**, as are the rendered diagrams
  under `docs/images/`. Nothing rebuilds those on GitHub, so ignoring them would leave the
  documentation showing broken images.
- **Commit messages carry no `Co-Authored-By` trailer and no mention of Anthropic or Claude.**
  This repository is published under the owner's name and the history shows them as sole
  author. Write a subject and a body, and stop.

### Teaching content

- **Every worked example uses the e-commerce domain** — one online shop, carried across all
  thirty-seven projects, so a learner moving between patterns only has to absorb the new
  structure. Analogies used to *explain* a pattern may come from any domain at all, and often
  should; the *code* may not.
- **Every explanation must work with the listener's eyes closed.** A large share of the
  audience listens rather than watches. No sentence may say "as you can see here" or depend on
  a diagram, a class name on a slide, or a line of code being visible. The words alone name
  the actors, say what each decides, and give the order things happen in.
- **The audience is beginners.** Short sentences, plain language, one idea at a time.
- **Posters never strike out their message.** Struck-through text is unreadable at
  search-result size and makes the poster look negative. Signal "this is the approach we are
  replacing" with colour, a label or an icon.
- **No video outro names the next pattern.** Publishing order is not fixed, so a teaser would
  date the video.
- **The opening narration of scene 1 has a required four-step order**: say what the video is,
  credit Jayasekhar Konduru, give the pattern in plain general words, then elaborate in
  e-commerce terms.

### Numbers

Every figure quoted in a README, a document, a slide or a narration line comes from the real
output of `./gradlew run` for that project. Nothing is rounded and nothing is invented. When
a demo changes, the quoted output changes with it.

---

## 4. What each project contains

Twenty-two committed files plus source, identical in shape across all twelve. `cqrs-pattern`,
`api-gateway-pattern` and `database-per-service-pattern` are the reference projects; copy from
one of them rather than from an older category.

```
README.md                     quotes real run output, including the failure
build.gradle, settings.gradle, gradlew, gradlew.bat, gradle/wrapper/
src/main/java/com/jk/explore/<slug>/
src/test/java/com/jk/explore/<slug>/
docs/problem-statement.md     the scenario, and what goes wrong
docs/<slug>-pattern-explained.md   one sentence, an everyday analogy, the acts, the cost
docs/class-diagram.md         Mermaid classDiagram plus prose
docs/uml-diagram.md           Mermaid sequenceDiagrams, one per act
docs/prerequisites.md         required / helpful / explicitly not required
docs/session.md               a one-hour facilitator guide for teaching the pattern
docs/animation.html           self-contained interactive animation, no dependencies
docs/make_animation_audio.sh  generates docs/audio/step-N.m4a for it
docs/youtube.md               title, description, chapters, thumbnail
docs/images/*.png             the two Mermaid diagrams rendered
docs/thumbnail.png            generated
docs/spec.md, docs/spec.html  generated
video/scenes.py               the script: 14–16 scenes
video/make_slides.py          renders one PNG per scene
video/build_video.sh          narrates and assembles
video/make_subtitles.py       writes the .srt
video/narration.md            generated from scenes.py
video/README.md               scene table and notes on the shape
video/poster.png              opening title card and YouTube thumbnail
```

Note the name collision: `docs/session.md` inside a *project* is a teaching guide for running
a one-hour session with a room of developers. That is a different thing from this document,
which is a handover for an AI session. They are not related.

---

## 5. If the work were to be extended

Nothing is outstanding, so this section is about what a *new* instruction would most likely
be, and where the constraints are.

**A thirteenth project needs a spec change first.** [`spec.md`](spec.md) §8 fixes what is out
of scope and why. Adding a pattern is a decision made in the spec, not mid-build.

**Shortening the ten long videos** is the most valuable improvement available. The last two
projects show the target: a tighter script at around eleven minutes rather than eighteen.

**Re-rendering everything** takes roughly eight to ten minutes of wall time per video, so a
full category rebuild is a two-hour job. Build in the background and poll for the output file
rather than blocking.

**Any fix to the audio pipeline is rolled out to all thirty-seven projects**, not left in the
one project where it was diagnosed. This has been stated explicitly and has already happened
twice, once for a denoiser that was making the voice sound underwater and once for a stdin
conflict in the animation audio script.
