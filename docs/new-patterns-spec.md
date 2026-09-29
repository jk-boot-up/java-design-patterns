# Spec — Ten New Pattern Projects and a Root Index

## 1. Goal

Add ten new teaching projects to `gradle-java/`, one at a time, each of the
same quality as the existing ones, and add a generated index at the repository
root that lists and links every project. Most of the work is generated from one
content file per project, so the effort (and the tokens) go into the teaching
content, not into boilerplate.

## 2. The ten projects, in build order

| # | Pattern | Category (directory) | The online-store scenario |
| --- | --- | --- | --- |
| 1 | Money | `enterprise-design-patterns` | Prices as doubles lose pennies; a `Money` type with currency and exact arithmetic, rounding, allocation of a discount across lines |
| 2 | Test Double | `testing-design-patterns` (new) | Testing checkout without charging a card: dummy, stub, spy, mock and fake payment gateways, and what each can prove |
| 3 | Content Enricher | `messaging-integration-patterns` | An order event with only a customer id is enriched with name, address and loyalty tier before the warehouse sees it |
| 4 | Materialized View | `micro-services-design-patterns` | "Best sellers this week" computed on every page view vs. a view kept up to date from order events |
| 5 | Asynchronous Request–Reply | `micro-services-design-patterns` | A large sales export: 202 Accepted, a status URL to poll, and the result when ready |
| 6 | Health Endpoint Monitoring | `micro-services-design-patterns` | Liveness vs. readiness for the checkout service; a load balancer that stops sending traffic to an instance that is alive but not ready |
| 7 | Write-Behind Cache | `micro-services-design-patterns` | Stock updates written to the cache now and to the database in batches; the speed, and the writes lost in a crash |
| 8 | Immutable Object | `foundational-design-patterns` | A price list shared by many threads; a mutable one corrupted mid-read vs. an immutable one replaced whole |
| 9 | Table-Driven State Machine | `behavioural` | Order status transitions (placed, paid, shipped, delivered, cancelled, refunded) as a table instead of scattered ifs |
| 10 | Modular Monolith | `architectural-design-patterns` | One deployable shop split into modules (catalog, orders, payments) with enforced boundaries, before any microservice |

Each is a **plain-Java** project (Java 21, Gradle wrapper, JUnit 5, no framework,
runs offline). A framework or real-infrastructure sibling may come later as a
separate `-with-<tool>` project; it is out of scope here.

## 3. What every project must contain

The same deliverables as the existing projects:

- **Code:** `src/main/java/com/jk/explore/<package>/`: the naive version, the
  pattern, and a `<Name>Demo` main class that runs the story in numbered acts
  and prints exact, repeatable numbers. **Tests:** JUnit 5, asserting every
  number the demo prints, plus the pattern's key property. No `Thread.sleep`,
  no wall clock; timing is simulated, so every run is identical.
- **`README.md`:** what it is, the analogy, the scenario, how to run and test,
  technologies and versions, the diagrams embedded, the costs, when it is too
  much, where you have met it. Plus a generated, self-contained `README.html`.
- **`docs/`:** `problem-statement.md`, `prerequisites.md`, `session.md` (a
  one-hour session guide with exercises), `<name>-explained.md`,
  `architecture-diagram.md`, `class-diagram.md`, `data-flow-diagram.md`,
  `sequence-diagram.md`, `uml-diagram.md`, `spec.md` + `spec.html`,
  `youtube.md`, `thumbnail.png`, `animation.html`.
- **Diagrams:** PNG files in `docs/images/`, drawn by a script from a small
  description. **No Mermaid** anywhere.
- **Video:** `video/scenes.py` (about 14 scenes), narrated with the approved
  voice, **Piper Amy at 0.8 speed with longer pauses** (the `amy-slow`
  settings), as the project's main voice. Produces `-explained.mp4`, `.m4a`,
  `.srt` and `poster.png`. Rendered media is not committed.
- **Animation:** `docs/animation.html`, one step per act, with the Narration
  on/off switch and per-step Play/Pause, clips in `docs/audio/`.

## 4. Teaching quality (non-negotiable)

- **Written for beginners.** Plain words, short sentences, one idea at a time;
  every term is explained the first time it is used.
- **Works with the eyes closed.** Narration never says "as you can see"; it
  names the actors, says what each does, and describes the flow in order.
- **Opening order**, exactly as in the approved api-composition video: what
  the video is, "This video is presented by Jayasekhar Konduru", "First, a
  simple definition" of the pattern in plain words, an everyday analogy (from
  whichever domain makes it clearest for a beginner), then the domain the code
  uses, introduced and explained before any detail, then what the viewer will
  see by the end.
- **The online store is the default domain** for the code. Where it fits a
  pattern poorly, use whichever domain makes the pattern easiest to learn, and
  say why in the README. Analogies may come from anywhere.
- **Honest:** each project shows the naive version working first, then where
  it hurts, the pattern, and then the pattern's own costs and when not to use it.
- **Closing:** one-sentence summary, the repository, one exercise, like and
  subscribe. Never announce the next pattern.
- **Pronunciation:** handled by videokit (API spelled A, P, I; the name spoken
  as "Jaya Shaykar").

## 5. The root index

`index.md` and `index.html` at the repository root, **generated** by a script
that scans `gradle-java/*/*-pattern/`, never edited by hand:

- grouped by category, in the course order, with a count per category;
- for each project: its title, a one-line summary, and links to its README,
  README.html, animation and spec; framework versions listed under their
  plain-Java project;
- `index.html` is self-contained (inline styles, no external links other than
  the project links) and works when opened from disk.

Re-running the script after adding a project keeps the index current.

## 6. Automation (to keep effort and tokens low)

One content file per project, **`pattern.toml`**, holds everything that is not
Java code: metadata, README and docs prose, diagram descriptions, animation
steps and video scenes. A new tool, **`tools/patternkit`**, turns it into:

| From `pattern.toml` | Generated |
| --- | --- |
| `[project]` | Gradle files and wrapper, package layout, videokit settings, registrations in the shared docs generators (spec, YouTube doc, thumbnail) |
| `[readme]`, `[docs.*]` | `README.md`, `docs/*.md` |
| `[[diagram]]` | `docs/images/*.png` and the diagram `.md` files |
| `[[step]]` | `docs/animation.html` (then voiced by videokit) |
| `[[scene]]` | `video/scenes.py` (then built by videokit) |

Then the existing generators produce `spec.*`, `youtube.md`, `thumbnail.png`
and `README.html`, and videokit produces the video, audio and animation clips.
A single command builds a whole project:
`tools/patternkit/patternkit.sh build <slug>`.

## 7. Acceptance for each project

1. `./gradlew test` passes, and `./gradlew run` prints the acts.
2. Every file in section 3 exists; the HTML pages are self-contained; no Mermaid.
3. The video and animation are rendered in the approved voice with no errors.
4. The project appears in `index.md` and `index.html` and in its category README.
5. Nothing rendered (mp4, m4a, srt, wav, audio clips, build folders) is committed.
