# Distributed Tracing Pattern — Project Specification

The single reference document for this project: what it teaches, how it
is built, and the quality bar its video and its YouTube publication have
to meet.

This is a *specification*, not a tutorial. It says what must be true and
why. The teaching material itself lives in
[`distributed-tracing-pattern-explained.md`](distributed-tracing-pattern-explained.md); the problem it
addresses is set out at length in
[`problem-statement.md`](problem-statement.md).

Where this document repeats a rule from the repository-wide
[`video-and-publishing-spec.md`](../../../docs/video-and-publishing-spec.md),
that document is the authority. This project's `video/build_video.sh` is generated from `creational/abstract-factory-pattern`'s, differing only in the pattern name and the output filenames, so a change to the pipeline belongs there and in the repository-wide spec, not here.

---

## 1. Purpose

Teach the decision to give one customer request one identifier and to have every
unit of work record how long it took *and what asked for it* — and to teach the
half most write-ups leave out, which is that the resulting picture can be
confidently wrong in three ways, none of which raises an error.

The three formats are not alternatives. A learner is expected to read the
problem statement, run the code, then watch the video — or watch first and
read after. Whichever order they choose, the class names, the numbers and
the scenario must be identical, because the value of the repository is
that a learner carries one e-commerce domain from pattern to pattern and
only has to absorb the new structure.

### Non-goals

- Not a tracing SDK. `Tracer`, `Span` and `Trace` are six small classes in one JVM; OpenTelemetry, `traceparent` headers, a collector and a backend belong to the optional `real/` directory.
- Not a network lesson. There is no HTTP and no serialisation. A trace context crossing a process boundary is the same string being passed along, and the string is what is being taught.
- Not a measurement. Every duration is a scripted constant from `Clock.Scripted`, so the 900ms page and the 340ms model are figures a test can assert exactly, where a real measurement could not.
- Not storage, batching or back-pressure. The spans go into a list. What the volume costs is made concrete in Act 7 as a count, not as an architecture.
- Not metrics or logs. Both appear, but only to be distinguished from a trace: Act 2 exists to show what four correct logs cannot say.

---

## 2. Problem statement

The full treatment is in [`problem-statement.md`](problem-statement.md).
In brief:

The shop's product page takes nine hundred milliseconds. Four services
contributed to it — catalog, pricing, inventory and recommendations — and all
four are healthy, all four are responding, and all four are writing correct
logs. Nobody in the building can say which of them spent the time. There is
exactly one measurement in the whole situation, and it is the complaint.

Act 2 shows why more logging does not rescue this. Two customers are on the site
at once, and the interleaved log gives `quote started` at 07.120, `quote
started` at 07.160, `quote complete` at 07.300 and `quote complete` at 07.340.
Subtract one way and pricing took 180ms; subtract the other and it took 220ms.
Both look reasonable and one of them pairs one customer's start with another
customer's finish.

Then try to fix it by adding fields. The thread name works until the work
crosses a thread, which it does in Act 6. The pod name is the same for both
customers, and so is the product id. Every candidate fails the same test: **the
same across one request, and different across the next.** What is missing is not
detail. It is an identifier — and, one level less obviously, a parent.

**What the pattern must deliver:** the 900ms attributed to the service that
actually spent it, drawn from the data rather than from a tool's cleverness --
and each of the three ways that attribution can be wrong while looking right.

---

## 3. Code

### Structure

11 production classes under `com.jk.explore.tracing`:

| Role | Types |
| --- | --- |
| The caller | `ProductPage` |
| The rejected design | `InterleavedLog` |
| The identifier | `TraceContext` |
| The unit of work | `Span`, with its `parentSpanId` |
| The boundary | `Tracer`, `Tracer.Scope` |
| The assembled request | `Trace` |
| The drawing | `Waterfall` |
| The price of volume | `Sampler` |
| The thread failure | `AsyncHandoff` |
| Determinism | `Clock`, `Clock.Scripted` |
| Entry point | `ProductPageDemo` |

### Requirements

1. **The pattern is one field.** `Span.parentSpanId` is a single string, and `start(context, name)` is the one argument that makes a pile of timings into a tree; the class diagram's arrow from `Span` to itself is the whole structure.
2. **The drawing is derived, not invented.** `Waterfall` computes indentation from the parent field and horizontal position from the start time, and nothing else — so the picture a hosted tool shows is demonstrably a property of the data.
3. **Self time, not total time.** The page span lasts the full 900ms and is charged 0ms of its own, recommendations lasts 400ms and is charged 60, and the six self times sum to exactly 900. The ranking model's 340ms is 37% of the page, and that is the finding.
4. **A span that is never closed is invisible.** `TracerTest.anUnclosedSpanIsInvisible` passes, which is why real instrumentation uses try-with-resources: an exception thrown past an open span deletes the record of the call that failed.
5. **An uninstrumented service produces a consistent lie.** In Act 5 recommendations forwards the context faithfully and opens no span. `ProductPageTest` asserts the resulting trace has one root, no orphans and 900ms fully accounted for *and* charges the page 60ms it never spent — that pair is the argument, not an oversight.
6. **The thread failure is one line in the wrong place.** `AsyncHandoff` reads the context from a `ThreadLocal` on the worker and is handed `null`, giving `2 separate roots — this trace is broken`; reading it on the thread that has it and passing it as a value gives the same two spans, the same 400ms and one root.
7. **Sampling is a decision made too early, priced in units.** `Sampler` keeps 10,000 of a million and discards 990,000, and the demo asks whether request 862,144 was kept: `no — it is gone, and it is not recoverable`. Tail sampling is named as the way out and not implemented.
8. **Nothing in the bill throws.** All three failures are the price of the pattern rather than mistakes made while applying it, and each one is asserted to produce output rather than an exception.
9. **The demo is deterministic.** The clock is scripted, span ids are sequential and the sampler counts rather than randomises, so two runs are byte-identical — there is one background thread in the project, in Act 6, and the demo waits for it.
10. **Every quoted number is the program's.** `DemoRunsTest` captures the demo's output and asserts the figures the README, the notes and the video narration speak aloud.
11. **Java 21, no third-party runtime dependencies.** JUnit 5 for tests
   only, so the project is readable by someone who does not know a DI
   framework.
12. **Every class fits on a slide.** This is teaching code; a class that
   needs scrolling to read has failed its purpose regardless of its
   design.

### Verification

- `./gradlew build` passes. 82 test methods across `AsyncHandoffTest`, `ClockTest`, `DemoRunsTest`, `InterleavedLogTest`, `ProductPageTest`, `SamplerTest`, `SpanTest`, `TraceContextTest`, `TraceTest`, `TracerTest`, `WaterfallTest`.
- `./gradlew run` output is quoted verbatim in the top-level `README.md`,
  and must still match.

---

## 4. Written material

Every document in `docs/` is required, and each has one job. A learner
reading them in the order given by the top-level README's table should
never need to jump forward.

| Document | Job |
| --- | --- |
| `prerequisites.md` | What to know and install first |
| `problem-statement.md` | The problem and why the naive approach hurts |
| `distributed-tracing-pattern-explained.md` | The pattern, the code, pitfalls, comparisons |
| `class-diagram.md` + PNG | Static structure |
| `uml-diagram.md` + PNG | Runtime call flow |
| `animation.html` | Step-by-step walkthrough, optionally narrated |
| `session.md` | A 60-minute guided teaching session |
| `youtube.md` | Everything needed to publish the video |
| `thumbnail.png` | The image to upload |
| `spec.md` / `spec.html` | This document |

Both Mermaid diagrams are committed as source *and* rendered PNG. The PNG
is what the README embeds, because GitHub's Mermaid rendering cannot be
relied on at these diagrams' size; the source is what gets edited.
Regenerating after an edit is mandatory — a diagram that disagrees with
the code is worse than no diagram.

---

## 5. Video quality specification

The finished video is `video/distributed-tracing-pattern-explained.mp4`, with an
audio-only `.m4a` and a `.srt` subtitle track alongside it. It is built by
`video/build_video.sh`, from scenes declared in `video/scenes.py` and
slides rendered by `video/make_slides.py`.

### 5.1 The opening, in four steps

Scene 1 is the only scene whose narration has a required structure, and
it is required because it is the scene that decides whether anybody
watches the second one. It must run in this order:

1. **What the video is** — "This video explains the Distributed Tracing pattern in
   Java", plainly, before anything else.
2. **The author credit** — "and it is written and presented by
   Jayasekhar Konduru".
3. **The pattern's definition, in general terms** — two or three
   sentences of plain language, with no mention yet of the store, the
   catalog or the checkout. A viewer who stops here has still learnt
   what the pattern is.
4. **Then the same thing in full, in the e-commerce domain** — the
   worked scenario, and what the viewer will be able to do by the end.

> **Requirement.** Steps 3 and 4 are separate and in that order. They
> used to be one step: the video opened straight into the shop's
> scenario and left the general definition to be inferred from a worked
> example, which works for a viewer already halfway to knowing the
> pattern and fails for everyone else. The cost is fifteen to thirty
> seconds of runtime, spent at the only point in the video where a
> viewer is still deciding whether to leave.

### 5.2 Delivered characteristics

| Property | Value | Why |
| --- | --- | --- |
| Container | MP4, `+faststart` | The index sits at the front, so the poster paints the moment the file opens |
| Video | H.264, 1920×1080, 30 fps, CRF 18, `preset slow`, `yuv420p` | 1080p is the minimum at which code on a slide is readable; `yuv420p` is what every player accepts |
| B-frames | Disabled (`-bf 0`) | They save nothing on a static slide and complicate the timestamps the gap check reads |
| Audio | AAC-LC, 48 kHz, stereo, 192 kbps | YouTube's recommended upload settings, so no re-encode on their side |
| Loudness | −16 LUFS integrated, true peak ≤ −1.5 dBTP | YouTube's normalisation target — deliver at it and the platform leaves the audio alone |
| Stream start | Both streams at exactly 0.000 s | Otherwise the video track starts 21 ms late and players show black at 0:00 |
| Narration | macOS `say`, voice Samantha, 145 wpm | The pace educational YouTube converges on for technical material |
| Inter-scene pause | 0.9 s of appended silence | So slides do not snap past the moment a sentence ends |
| Runtime | ~16:53 over 16 scenes, 247 subtitle cues |  |

### 5.3 The two defects this pipeline exists to prevent

Both produce a file that looks fine and sounds broken, and both were live
in this repository before the current build script. They are documented
here because the obvious "simplification" of the pipeline reintroduces
them.

**Per-scene AAC concatenation.** AAC is a lapped format: every separately
encoded clip carries priming samples at its head and padding at its tail.
Concatenating such clips with `-c copy` strips neither, so each join
leaves a hole in the timeline. Measured on the reference project before
the fix: 30 gaps totalling 31 seconds of missing narration.

> **Requirement.** Each scene's narration is written as lossless PCM WAV.
> The joined narration is encoded to AAC exactly once, at the final mux.
> There must be exactly one `-c:a aac` in the build script.

**Dynamic-mode `loudnorm`.** Left to itself `loudnorm` rides the level as
it goes, and on some narrations emits a timestamp discontinuity partway
through — the same audible hole, mid-sentence, with nothing wrong
upstream of it.

> **Requirement.** Loudness is measured over the whole narration in a
> first pass, and the measured figures are fed back with `linear=true` so
> the second pass applies one constant gain. This also stops the level
> pumping between quiet and loud lines.

### 5.4 Why there is no denoiser

An earlier version ran `afftdn` over the narration and, by the numbers, it
worked — about 15 dB off the noise floor. It also made the voice
noticeably worse. A spectral denoiser needs a real, roughly stationary
noise floor to subtract; synthesised speech has almost none, so `afftdn`
subtracts parts of the speech instead and leaves it warbling.

> **Requirement.** The `CLEANUP` chain contains no `afftdn` and no
> `lowpass`. It is exactly: resample to 48 kHz with a long filter
> (`filter_size=512`, `cutoff=0.98`, `linear_interp=1`), a 75 Hz high-pass
> for rumble, and a gentle +1.5 dB shelf at 3 kHz for consonants. The
> faint remaining hiss is much the lesser problem.

Levelling is deliberately not in this chain either: run per scene it
re-measures on every clip, so a quiet scene is pushed up to match a loud
one and the level audibly steps at each join. It happens once, over the
whole narration.

### 5.5 Synchronisation

Scene lengths are rounded up to a whole number of video frames —
`frames = ceil(duration × 30)`, `target = frames / 30` — and each scene's
WAV is padded to exactly that target. Picture and narration are therefore
the same length for every scene, so slide changes cannot drift away from
the voice however many scenes the video grows to.

### 5.6 Self-check, and its limit

After the mux the build reads every audio packet timestamp and fails if
any two are more than one AAC frame apart, printing
`audio timeline continuous: N packets, no gaps`. A build that does not
print that line has not passed.

**This check verifies continuity, not fidelity.** It cannot hear
warbling, clipping or a bad voice — the `afftdn` problem passed it
cleanly for weeks. Any change to the filter chain or the voice requires
someone to actually listen to the result before it is called done.
Objective measurement of the delivered file (integrated loudness, true
peak, silence detection) is a useful guard but is not a substitute for
that.

---

## 6. Poster and thumbnail

Two different images, for two different jobs. Conflating them is the
mistake this section exists to prevent.

**`video/poster.png`** — 1920×1080, the video's opening frame, lifted out
of the build. It carries the before/after comparison: the approach being
replaced on one side, the pattern on the other.

**`docs/thumbnail.png`** — 1280×720, generated by
[`make_thumbnails.py`](../../../docs/make_thumbnails.py), and the image
that is uploaded. It is deliberately not the poster: YouTube serves a
thumbnail at roughly 360 pixels wide in a search result, and at that size
a two-column code comparison is a smudge. The thumbnail therefore carries
three things only — the pattern name, one line of promise, and one short
piece of code — each set large enough to survive the shrink.

> **Requirement.** Neither image strikes out its "before" sample. A rule
> drawn through monospace is hard to read at full size and illegible at
> thumbnail size, and striking the code out makes the card read as being
> about what is wrong rather than what is being taught. The rejected
> approach is marked with a `BEFORE` chip and the pattern with an `AFTER`
> chip; colour and label carry the contrast.

> **Requirement.** The poster is inspected visually before it is
> considered done, not merely confirmed to exist. `proxy-pattern` once
> shipped a poster reading "DECORATOR PATTERN", complete with
> decorator's code samples, because `make_slides.py` was copied and
> `kind_poster` was never updated. Only looking at the image catches
> that.

---

## 7. YouTube publication

[`youtube.md`](youtube.md) holds everything needed to publish, so that
uploading is copy-and-paste rather than reconstruction. Seven sections
are required:

1. **Title** — the exact string, ≤ 60 characters so search does not
   truncate it, leading with the pattern name. Currently *"Distributed Tracing in Java - Which Service Is Slow?"*,
   52 characters. The suffix after the dash names the worked e-commerce scenario, so the title says what the viewer will actually watch rather than only which pattern it is about.
2. **Description** — first two lines carry the hook, because that is what
   shows above the fold; then what the video covers, the chapters, the
   repository link, the prerequisites.
3. **Chapters** — `mm:ss Title`, one per scene, first entry `00:00`.
   YouTube needs at least three and the first at zero to render them at
   all.
4. **Tags** — comma-separated, under 500 characters.
5. **Thumbnail** — pointing at `docs/thumbnail.png`, and explaining why
   it is not the poster.
6. **Upload checklist** — subtitles, language, thumbnail, HD processing,
   playlist.
7. **Cards and end screen** — which video comes next in the learning
   order. For this project: Backends for Frontends.

> **Requirement.** Chapter timings are generated from the built `.srt`,
> never written by hand, by
> `python3 ../../docs/make_youtube_docs.py distributed-tracing`. They are the one part of
> the file that goes stale silently: any change to the narration text or
> the speaking rate invalidates every timestamp, and a chapter list that
> is thirty seconds out is worse than none. Regenerate after any
> rebuild.

Subtitles are uploaded from the generated `.srt` rather than left to
YouTube's automatic captions, which mis-transcribe class names
throughout.

---

## 8. Conformance

This project is compliant when all of the following hold. The full
version, which governs all fourteen projects, is in
[`video-and-publishing-spec.md`](../../../docs/video-and-publishing-spec.md)
§9.

- [ ] The worked example is e-commerce.
- [ ] `./gradlew build` passes, and the README quotes the real `./gradlew run` output, which still matches.
- [ ] Scene 1 follows the four-step opening of §5.1 — what the video is, the author credit, the pattern's definition in general terms, and only then the e-commerce scenario.
- [ ] `RATE` is 145 and `VOICE` is Samantha.
- [ ] `CLEANUP` is exactly as §5.4 gives it — no `afftdn`, no `lowpass`.
- [ ] Per-scene audio is PCM; exactly one AAC encode, at the mux.
- [ ] `loudnorm` is two-pass with `linear=true`.
- [ ] The build prints `audio timeline continuous: N packets, no gaps`.
- [ ] `poster.png` shows the correct pattern name and contains no strikethrough, confirmed by looking at it.
- [ ] `docs/youtube.md` has all seven sections, and its chapter timings match the current `.srt`.
- [ ] `video/README.md` describes the pipeline as it actually is.

Last verified: all eleven items pass. The delivered MP4 measures -16.01 LUFS
integrated, -3.60 dBTP true peak, and both streams start at 0.000.

---

## 9. Rebuilding

From the project root:

```bash
(cd video && ./build_video.sh)        # CPU-bound at CRF 18
```

Then, because the narration timings will have moved:

```bash
python3 ../../docs/make_youtube_docs.py distributed-tracing
python3 ../../docs/make_specs.py distributed-tracing
```

Changing the voice or the filter chain means listening to the result.
Changing the narration text means both of the above, and re-checking the
runtime claims in the top-level `README.md` and in `video/README.md`.
