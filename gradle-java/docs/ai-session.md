# AI Session Handover — Framework And Infrastructure Versions Batch

| | |
| --- | --- |
| Session started | 2026-09-23, about 19:00 IST |
| Last updated | 2026-09-24 (resumed session) |
| Branch | `main`, at `8994c81` |
| Commits made this session | none |
| Repository state | 157 projects committed (wave 1 committed 2026-09-24, `bef1611`..`bdac65c`, not pushed); wave 2 building |

This document exists so that a session working on this batch can be stopped at any point and
picked up later, by a different session with no memory of this one, without having to re-derive
the state of the work.

It covers the batch specified in [`framework-and-infra-versions-spec.md`](framework-and-infra-versions-spec.md),
which adds 28 projects and takes the repository from 152 to 180. That specification is the
authority on *what* is being built and *why*; this document records *how far it has got*.

There is a second, older handover at
[`../micro-services-design-patterns/docs/ai-session.md`](../micro-services-design-patterns/docs/ai-session.md)
covering the microservices category, which is finished. The two are unrelated except that both
point at the same toolchain document,
[`../micro-services-design-patterns/docs/ai-build-spec.md`](../micro-services-design-patterns/docs/ai-build-spec.md).

---

## 1. The instruction this batch is answering

The repository owner asked for versions of the existing patterns built on real infrastructure
and real framework stacks — Spring Boot and the rest — for the patterns that did not already
have one, and asked for a specification to be written and agreed before any building started.

He then made one constraint explicit, and it governs everything here:

> **The existing versions' code is not to be changed.** What is being added is *newer versions
> of the project* with an infrastructure and framework stack.

So every project in this batch is a new sibling directory. No existing project is edited,
refactored, retitled or deleted. This is checked with `git status` before any commit: no
tracked file belonging to an existing project may show as modified.

---

## 2. Current state

**Wave 1 is committed. Wave 2 is building in two groups of five** (Docker has 4 CPUs and 4 GB, so the heavy stacks wait for group B). Wave 1 commits: one per project, then one for registration and READMEs. The messaging category README, its HTML twin and the root README counts (messaging 5 → 10, total 152 → 157) are updated.

| Wave | Projects | State |
| --- | --- | --- |
| 1 | 5 messaging and integration | committed |
| 2 | 10 microservices | group A building 2026-09-24: cache-aside-with-redis, publisher-subscriber-with-redis, rate-limiter-with-redis, competing-consumers-with-rabbitmq, claim-check-with-s3. Group B next: transactional-outbox-with-debezium, database-per-service-with-containers, leader-election-with-kubernetes, queue-based-load-leveling-with-sqs, idempotent-consumer-with-kafka |
| 3 | 4 platform | not started |
| 4 | 9 framework versions | not started |

### Wave 1 detail

| Project | State |
| --- | --- |
| `splitter-aggregator-with-camel-pattern` | **Finished, verified and registered.** 16 scenes, video 8:51, `audio timeline continuous: 24925 packets`, −16.01 LUFS. Registered in the three generators on 2026-09-24; `spec.md`, `spec.html`, `thumbnail.png`, `youtube.md` and `README.html` generated |
| `message-channel-with-rabbitmq-pattern` | **Finished, verified and registered** 2026-09-24. 16 scenes, video 9:55, 12 tests, `audio timeline continuous: 27912 packets`, −16.01 LUFS. The best find: keeping a message through a restart takes two settings, a durable queue and persistent messages; after a restart both queues came back but one held 3 orders and the other 0, and an empty queue looks like a quiet day. Prefetch is defined in the docs but not demonstrated |
| `dead-letter-channel-with-rabbitmq-pattern` | **Finished, verified and registered** 2026-09-24. Moved from Testcontainers 1.21.4 to 2.0.5 (module `testcontainers-rabbitmq`, package `org.testcontainers.rabbitmq`) to match the batch; video re-rendered for the version slide. 16 scenes, video 8:13, 9 tests, `audio timeline continuous: 23126 packets`, −16.00 LUFS. The best find: the working queue reports nothing waiting while twenty paid orders sit parked, so every dashboard shows the shop healthy |
| `content-based-router-with-camel-pattern` | **Finished, verified and registered** 2026-09-24. 16 scenes, video 10:05, 12 tests, `audio timeline continuous: 28398 packets`, −16.01 LUFS. The best find: with no otherwise branch Camel acknowledges an unclaimed order and the broker deletes it — zero messages left anywhere and nothing logged, where the hand-built twin counted the drop. Coordinator fix: act two printed pence while act three printed pounds; `Order.pounds()` now formats both, so the slide's `1200.00` is real output |
| `event-bus-with-nats-pattern` | **Finished, verified and registered** 2026-09-24. 16 scenes, video 9:40, 8 tests, `audio timeline continuous: 27200 packets`, −16.01 LUFS. The best find: an event published with nobody listening is gone, and the demo proves it without waiting, because the warehouse's first event is ORD-2 |

The five were built in parallel by five separate agents, each confined to its own project
directory, each forbidden from running git and from touching the shared generators.

### What the finished project proves

`splitter-aggregator-with-camel-pattern` is the reference for the rest of the batch. Its
README section "What the simulation got right, and what it left out" is the shape every other
project in this batch should copy, and its best find shows why these projects are worth
building at all: **Camel's completion-by-size counts messages folded into an aggregate, not
distinct pieces of it.** A duplicated shipment therefore makes the aggregator declare an order
complete holding only two of its three lines, billing £265.97 where £515.96 was due. The
plain-Java simulation cannot produce that class of bug, because it counts the thing the author
intended rather than the thing the framework actually counts.

---

## 3. The step that is still owed to every project in wave 1

**Four files per project are deliberately missing and must be generated centrally**:
`docs/spec.md`, `docs/spec.html`, `docs/thumbnail.png` and `docs/youtube.md`.

They are missing because `make_specs.py`, `make_thumbnails.py` and `make_youtube_docs.py` each
carry a hand-maintained table of slugs, and a project absent from those tables is silently
skipped. Those three files are shared by every project in the repository, so five agents
editing them in parallel would only produce conflicts. Registration was therefore deferred and
is done once, by the coordinating session, after a wave's projects exist.

For each finished project, from the `gradle-java` directory:

```bash
# 1. add the slug by hand to the table in each of the three generators
#    (slug has the -pattern suffix removed: splitter-aggregator-with-camel)
# 2. then, and only after the video exists:
python3 docs/make_specs.py        <slug>
python3 docs/make_thumbnails.py   <slug>
python3 docs/make_youtube_docs.py <slug>
python3 docs/make_readme_html.py  <category-or-project-path>
```

**Order matters.** `make_specs.py` measures the rendered mp4 to fill in runtime, subtitle count
and loudness. Run before the video exists, it does not fail — it silently writes
`~not yet built over 0 scenes, 0 subtitle cues`. That defect has reached the repository once
before. Check the line each run prints; every field in it should look plausible:

```
splitter-aggregator-with-camel   spec.md + spec.html  (16 scenes, 8:51, 9 tests, -16.00 LUFS)
```

---

## 4. How to establish state at the start of a session

Do not trust the tables above. They are a snapshot and the tree may have moved. Run the checks.
From the `gradle-java` directory:

```bash
# which of the batch's projects exist, and which have a rendered video
for d in */*-with-*-pattern; do
  printf "%-60s files:%4s  mp4:%s\n" "$d" \
    "$(find "$d" -type f | wc -l | tr -d ' ')" \
    "$(ls "$d"/video/*.mp4 2>/dev/null | wc -l | tr -d ' ')"
done

# the constraint that matters most: no existing project modified
git status --porcelain | grep -vE '^\?\?'     # must print nothing

# no rendered media has leaked into the git surface
git status --porcelain | grep -Ei '\.(mp4|m4a|srt|wav|aac|log)$|docs/audio/|video/build/'

# a spec generated before its video is stale
for d in */*-with-*-pattern; do
  [ -f "$d/docs/spec.md" ] && printf "%-60s %s\n" "$d" \
    "$(grep -oE '[0-9]+ scenes' "$d/docs/spec.md" | head -1)"
done
```

Note that `ls *.mp4` fails under zsh with `no matches found` rather than returning empty, which
during a render looks like a build failure and is not.

---

## 5. Standing instructions

These are the repository owner's, stated explicitly. They are not preferences to be
re-litigated, and they override any default behaviour.

- **Existing projects are never modified.** See §1. Additive work only.
- **Nothing is committed or pushed without being asked.**
- **Commit messages carry no `Co-Authored-By` trailer and no mention of any assistant.** Subject
  and body, then stop. The same applies to pull request descriptions.
- **Rendered output never enters the repository** — no mp4, m4a, srt, wav or log, nothing under
  `video/build/` or `docs/audio/`. `animation.html`, `video/poster.png`, `docs/thumbnail.png`
  and `docs/images/*.png` are committed, because nothing rebuilds those on GitHub.
- **Every worked example uses the e-commerce domain.** One online store across all 180 projects.
  Analogies used to *explain* may come from any domain and often should; the code may not.
- **Every explanation must work with the listener's eyes closed.** Much of the audience listens
  rather than watches. No "as you can see here", and nothing that depends on a diagram, a slide
  or a line of code being visible. The audience is beginners: short sentences, plain language,
  one idea at a time.
- **Posters never strike out their message.** Strikethrough is unreadable at search-result size.
- **No video outro names another pattern**, because publishing order is not fixed.
- **Scene 1 narration has a required four-step order**: what the video is, credit to Jayasekhar
  Konduru, the pattern in plain general words, then the same in e-commerce terms.
- **Every number** in a README, document, slide or narration line is the real output of
  `./gradlew run` for that project. Nothing rounded, nothing invented.
- **Any fix to the audio pipeline is rolled out to all projects**, not left where it was found.
- **New projects are self-contained** (instruction of 2026-09-24, spec §5.5a). No relative link
  or path into a sibling project, the twin named in words, the audio pipeline explained in the
  project's own `video/README.md`. Existing projects are not to be disturbed to retrofit this.
  `gradle-java/docs`, including its three registration tables, is the permitted shared place.

---

## 6. What to do next

1. ~~Verify the four wave-1 builds~~ — done 2026-09-24.
2. ~~Register all five slugs and generate the four files per project~~ — done.
3. ~~Update the messaging README, its HTML twin and the root README counts~~ — done.
4. ~~Commit wave 1~~ — done. The owner then asked for a prefetch act in
   `message-channel-with-rabbitmq`; that revision is in progress and gets its own commit.
5. Then wave 2, the ten microservices projects, which is the largest of the four.

Three things worth carrying forward into later waves:

**A render takes eight to ten minutes.** Run it in the background and poll for the output file
rather than blocking, and delete `video/.build.log` afterwards — it is not covered by
`.gitignore`.

**Parallel building worked.** Five agents in one working tree, each confined to its own new
directory with git and the shared generators off limits, produced no collisions. The only
coordination cost is the central registration step in §3, and that is cheap.

**`make_thumbnails.py` and `make_readme_html.py` need `/usr/bin/python3`.** The Homebrew
`python3` first on the PATH has no matplotlib and fails with `No module named 'matplotlib'`.
`make_specs.py` and `make_youtube_docs.py` run under either.
