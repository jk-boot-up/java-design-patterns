# Backends for Frontends Pattern — Project Specification

The single reference document for this project: what it teaches, how it
is built, and the quality bar its video and its YouTube publication have
to meet.

This is a *specification*, not a tutorial. It says what must be true and
why. The teaching material itself lives in
[`backends-for-frontends-pattern-explained.md`](backends-for-frontends-pattern-explained.md); the problem it
addresses is set out at length in
[`problem-statement.md`](problem-statement.md).

Where this document repeats a rule from the repository-wide
[`video-and-publishing-spec.md`](../../../docs/video-and-publishing-spec.md),
that document is the authority. This project's `video/build_video.sh` is generated from `creational/abstract-factory-pattern`'s, differing only in the pattern name and the output filenames, so a change to the pipeline belongs there and in the repository-wide spec, not here.

---

## 1. Purpose

Teach the decision to give each kind of client its own small backend, owned by
the team that owns the screen, holding the shape of one screen and nothing else
-- and to teach it against the fix that looks like it makes the pattern
unnecessary, because a `?fields=` query parameter reaches the same byte count
with no new process to run, and a reader who is not shown that working will
file this pattern under payload size and be wrong about it for years.

The three formats are not alternatives. A learner is expected to read the
problem statement, run the code, then watch the video — or watch first and
read after. Whichever order they choose, the class names, the numbers and
the scenario must be identical, because the value of the repository is
that a learner carries one e-commerce domain from pattern to pattern and
only has to absorb the new structure.

### Non-goals

- Not a network lesson. There is no HTTP, no JSON library and no serialisation. `Doc` is an ordered map that prints and measures itself, and every claim about round trips is made by *counting* them in `CallLog`, not by timing them.
- Not a performance measurement. `Shop` returns fixed data in microseconds, so the byte counts are identical on every machine and a test can assert them exactly, where a measurement could not.
- Not concurrency. The four internal calls are sequential where a real backend would fan them out and wait once, which means the project **understates** the pattern's benefit rather than overstating it.
- Not an API gateway. The two are neighbouring patterns and are commonly deployed together; Act 6 exists to separate them with a single question, not to implement either as infrastructure.
- Not deployment. Two independently deployable Spring Boot backends serving the same product over the wire, in front of a third service holding the shop, belong to the optional `real/` directory, which is a separate Gradle build.

---

## 2. Problem statement

The full treatment is in [`problem-statement.md`](problem-statement.md).
In brief:

The shop sells one copper coffee maker. On a phone the product screen draws six
things — title, price, one image, a rating, a rating count, and one line saying
when the parcel arrives. On a desktop the same product fills a page with fifteen,
including the description, a specification table, five images and three written
reviews. Five services hold all of it: catalog, pricing, inventory, reviews and
recommendations. Neither screen is wrong. Both teams are being reasonable. They
disagree about what a product *is*, and everything here comes out of that.

The first design is the one shops arrive at by accident, because it is nobody's
decision: the phone calls all five services itself. Five sequential round trips
before a pixel is drawn — sequential because pricing cannot be asked about a
product until the catalog has named it — carrying 1767 bytes and 29 fields, of
which 6 reach the screen.

The second design is one shared endpoint in front of the five, and it genuinely
helps: one round trip instead of five. But one endpoint publishes one document,
and that document must satisfy every client, so it grows into the union of all
of them. 1755 bytes arrive, 212 are drawn, 1543 — 87% — are thrown away on
arrival.

And then the obvious fix works. `GET /api/products/4417?fields=...` returns 212
bytes, which is the same saving the finished pattern gets, from a query
parameter, with nothing to deploy. **If this pattern were about payload size,
the story would end there.** It ends instead at the next request: the phone team
wants one line of text — "Free delivery, arrives Friday" — joined from stock,
the delivery rules and the clock. Half an hour of work. But it is a new field on
a document five other clients also receive, so it becomes a contract change in a
queue behind work that has nothing to do with the phone. The phone team could
have written it in an afternoon and waits five weeks.

**What the pattern must deliver:** that five-week queue removed, the byte saving
kept, the boundary against a gateway made decidable in one question — and the
three ways the pattern costs more than it saves, none of which throws.

---

## 3. Code

### Structure

14 production classes under `com.jk.explore.bff`:

| Role | Types |
| --- | --- |
| The contract | `ClientBackend` |
| The two live implementations | `MobileBff`, `WebBff` |
| The services behind them | `Shop` |
| The document | `Doc` |
| The ruler | `Screens` |
| The first rejected design | `ChattyPhone` |
| The second rejected design | `SharedApi` |
| The count that is the evidence | `CallLog`, `CallLog.Origin` |
| The duplicated belief | `SavingRules` |
| The gateway's question | `CrossCutting` |
| How many is too many | `ClientEstate` |
| Presentation, not policy | `Money` |
| Entry point | `ProductScreenDemo` |

### Requirements

1. **Two implementations, both live, on purpose.** `ClientBackend` has two implementing classes and neither is a fallback: the phone always talks to `MobileBff` and the desktop always to `WebBff`, at the same time, in production. Two arrowheads into one interface is the pattern rather than a detail of it.
2. **A backend is the size of its screen, and stays that size.** `MobileBffTest.sendsOnlyWhatIsDrawn` asserts `assertEquals(Screens.PHONE, screen.paths())` — equality, not containment — so a seventh field fails the build. That assertion is the only reason a backend does not drift back into a shared endpoint over a year.
3. **The two backends must disagree.** `WebBffTest.disagreesWithThePhonesBackend` asserts the two return *different* field lists. If they ever converged the shop would be paying twice for one job and the pattern should be withdrawn rather than admired.
4. **The obvious fix is shown succeeding.** Act 2 runs the `?fields=` query and prints 212 bytes before the pattern is introduced, so the reader sees the payload argument settled and knows the pattern is not resting on it.
5. **The saving that is not bytes.** Act 2 also prints the delivery sentence as `not available — a field like this belongs to one client, and this endpoint belongs to all of them`. The five-week queue is the problem the pattern removes, and it is organisational with a technical cause.
6. **A backend omits calls, not just fields.** `MobileBff` never calls recommendations, because the phone screen has no related-products strip; internal calls go 5, 5, 4 across the three designs while device calls go 5, 1, 1. **The work relocated onto a network that costs nothing; it was not deleted.**
7. **Presentation belongs in the backend.** Pricing returns `4799`; the phone is sent the string `"£47.99"`. The conversion happens in a process that can be corrected this afternoon rather than in an app customers will still be running in two years.
8. **Shape inside, belief behind.** Act 5 copies one discount rule into `MobileBff`, and after the pricing team adds a minimum-duration condition the desktop claims nothing while the phone advertises `Save £12.00` for a price that rose 11 days ago. Nothing throws, nothing is logged, both backends' tests pass, and no test writable inside either one can notice — the rule is that anything the shop would still believe with every client switched off belongs behind the backend.
9. **The gateway boundary is one question, and the code answers it.** `CrossCutting.copiesBehindAGateway()` takes no argument, and that absence is the answer: 8 copies across 2 backends against 4 whatever the number of backends. *What does this screen need?* is a backend for a frontend; *is this request allowed in at all?* is a gateway.
10. **One per disagreement, not per device and not per team.** `ClientEstate` scores six clients as three genuine disagreements — the tablet is the phone's fields in a wider column, the kiosk is the desktop page with the basket hidden, the partner feed is not a screen. **Two backends is a pattern. Nine is a department.**
11. **Every quoted number is the program's.** `DemoRunsTest` captures the demo's output and asserts the figures the README, the notes and the video narration speak aloud.
12. **Java 21, no third-party runtime dependencies.** JUnit 5 for tests
   only, so the project is readable by someone who does not know a DI
   framework.
13. **Every class fits on a slide.** This is teaching code; a class that
   needs scrolling to read has failed its purpose regardless of its
   design.

### Verification

- `./gradlew build` passes. 46 test methods across `CallLogTest`, `ChattyPhoneTest`, `ClientEstateTest`, `CrossCuttingTest`, `DemoRunsTest`, `DocTest`, `MobileBffTest`, `MoneyTest`, `SavingRulesTest`, `SharedApiTest`, `ShopTest`, `WebBffTest`.
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
| `backends-for-frontends-pattern-explained.md` | The pattern, the code, pitfalls, comparisons |
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

The finished video is `video/backends-for-frontends-pattern-explained.mp4`, with an
audio-only `.m4a` and a `.srt` subtitle track alongside it. It is built by
`video/build_video.sh`, from scenes declared in `video/scenes.py` and
slides rendered by `video/make_slides.py`.

### 5.1 The opening, in four steps

Scene 1 is the only scene whose narration has a required structure, and
it is required because it is the scene that decides whether anybody
watches the second one. It must run in this order:

1. **What the video is** — "This video explains the Backends for Frontends pattern in
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
| Runtime | ~18:30 over 16 scenes, 263 subtitle cues |  |

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
   truncate it, leading with the pattern name. Currently *"Backends for Frontends in Java - One Shape Won't Fit"*,
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
   order. For this project: Sidecar.

> **Requirement.** Chapter timings are generated from the built `.srt`,
> never written by hand, by
> `python3 ../../docs/make_youtube_docs.py backends-for-frontends`. They are the one part of
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

Last verified: all eleven items pass. The delivered MP4 measures -16.02 LUFS
integrated, -3.61 dBTP true peak, and both streams start at 0.000.

---

## 9. Rebuilding

From the project root:

```bash
(cd video && ./build_video.sh)        # CPU-bound at CRF 18
```

Then, because the narration timings will have moved:

```bash
python3 ../../docs/make_youtube_docs.py backends-for-frontends
python3 ../../docs/make_specs.py backends-for-frontends
```

Changing the voice or the filter chain means listening to the result.
Changing the narration text means both of the above, and re-checking the
runtime claims in the top-level `README.md` and in `video/README.md`.
