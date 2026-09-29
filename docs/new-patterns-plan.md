# Plan — Ten New Pattern Projects and a Root Index

Spec: [`new-patterns-spec.md`](new-patterns-spec.md). Work is done one project
at a time. Progress is tracked in the checklist below and updated as each step
finishes.

## Phase 0 — Tooling (once, before the first project)

1. **`tools/patternkit/`**: a small Python tool, run through the videokit venv.
   - `scaffold <category> <slug>`: creates the project directory, Gradle
     build and wrapper (copied from an existing project), package folders,
     `video/videokit.toml` with the `amy-slow` voice, and a starter
     `pattern.toml`.
   - `docs <slug>`: writes `README.md` and every `docs/*.md` from
     `pattern.toml`.
   - `diagrams <slug>`: draws the PNG diagrams from `[[diagram]]` entries
     (flow, class and sequence shapes; dark theme matching the slides).
   - `animation <slug>`: writes `docs/animation.html` from `[[step]]`
     entries, in the same style as the existing pages.
   - `scenes <slug>`: writes `video/scenes.py` from `[[scene]]` entries.
   - `build <slug>`: all of the above, then `./gradlew test`, the shared docs
     generators, `videokit all` and `videokit animation`, and the index.
2. **Registration without hand-editing:** the shared generators
   (`make_specs.py`, `make_youtube_docs.py`, `make_thumbnails.py`) also read
   `pattern.toml`, so a new project needs no edits to their tables.
3. **`gradle-java/docs/make_index.py`**: writes the root `index.md` and
   `index.html` by scanning the projects.
4. Try the whole chain on project 1 before building the others.

## Phase 1 — The ten projects, one at a time

For each project, in order:

1. `scaffold`.
2. Write the Java code: the naive version, the pattern and the demo, in 4–6
   acts with exact numbers. Write the tests.
3. `./gradlew test run`, and fix until green and the output reads well.
4. Write `pattern.toml`: the prose, diagrams, animation steps and scenes,
   using the numbers the demo actually printed.
5. `build`. Check the generated README, one diagram and the animation page.
6. Render the video and animation clips in the background; move on to the
   next project while they render.
7. Tick the checklist.

## Phase 2 — Finish

1. Regenerate `index.md` / `index.html` and the category READMEs.
2. Confirm every acceptance point in the spec for all ten.
3. Commit and push the source only when the author asks.

## Checklist

| # | Project | Code + tests | Docs | Diagrams | Animation | Video | Index |
| --- | --- | :---: | :---: | :---: | :---: | :---: | :---: |
| 0 | Tooling + index | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 1 | Money | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 2 | Test Double | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 3 | Content Enricher | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 4 | Materialized View | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 5 | Asynchronous Request–Reply | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 6 | Health Endpoint Monitoring | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 7 | Write-Behind Cache | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 8 | Immutable Object | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 9 | Table-Driven State Machine | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 10 | Modular Monolith | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

## Risks and how they are handled

- **Generated prose reading as filler.** The tool only lays text out; every
  sentence is written for the project in `pattern.toml`, from the real demo
  output.
- **Diagram layout.** Positions are given in the description, not computed,
  so every diagram is predictable. A diagram that looks cramped is fixed in
  its description, not by hand-editing the PNG.
- **Render time.** Videos render in the background while the next project is
  written.
- **A new category** (`testing-design-patterns`) needs a category README; the
  index script picks up any category automatically.
