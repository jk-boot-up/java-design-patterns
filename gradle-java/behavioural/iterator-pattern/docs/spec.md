# Iterator Pattern — Project Specification

The single reference document for this project: what it teaches, how it
is built, and the quality bar its video and its YouTube publication have
to meet.

This is a *specification*, not a tutorial. It says what must be true and
why. The teaching material itself lives in
[`iterator-pattern-explained.md`](iterator-pattern-explained.md); the problem it
addresses is set out at length in
[`problem-statement.md`](problem-statement.md).

Where this document repeats a rule from the repository-wide
[`video-and-publishing-spec.md`](../../../docs/video-and-publishing-spec.md),
that document is the authority. This project's `video/build_video.sh` is generated from `creational/abstract-factory-pattern`'s, differing only in the pattern name and the output filenames, so a change to the pipeline belongs there and in the repository-wide spec, not here.

---

## 1. Purpose

Teach handing out a small object that remembers where a caller has got to, so
that walking an awkward collection is written once instead of once per caller
-- and teach the split the pattern turns on, which is that the collection
knows what is in it and the iterator knows where you are, in two different
objects, with no exceptions.

The three formats are not alternatives. A learner is expected to read the
problem statement, run the code, then watch the video — or watch first and
read after. Whichever order they choose, the class names, the numbers and
the scenario must be identical, because the value of the repository is
that a learner carries one e-commerce domain from pattern to pattern and
only has to absorb the new structure.

### Non-goals

- Not an argument for wrapping a `List`. A `List` already has an iterator, and the notes say plainly that writing another one around it is ceremony; the pattern earns its keep here because the storage is paged, and the explainer names the other cases — trees, streams of lines, sequences with no end — rather than implying it is always worthwhile.
- Not a streams tutorial, and not an argument against streams. The comparison section places index loops, iterators and streams side by side and states explicitly that streams are built on this pattern rather than being an alternative to it. `java.util.stream` is not imported anywhere in the project.
- Not a lesson in generics. `Iterable<Product>` and `Iterator<Product>` are read, never written; no class in the project declares a type parameter, because a beginner should not have to learn generic class declarations to learn this pattern.
- Not concurrency. `ConcurrentModificationException` gets one mention in the pitfalls and nothing more; there are no threads, no fail-fast modification counting, and no synchronisation anywhere.
- Not a real paged API. `CatalogueFeed` fakes the warehouse with a list and a counter, so there is nothing to install, connect to or stub — the counter is the point, because it turns laziness into something a test can assert.

---

## 2. Problem statement

The full treatment is in [`problem-statement.md`](problem-statement.md).
In brief:

The shop's catalogue does not live in the application. It lives in the
warehouse system, which hands products over three at a time: you ask for page
zero, then page one, and you know you have reached the end when a page comes
back empty. There is no `size()` and no `hasMorePages()`. Everything else a
caller might want, it works out by hand, in a loop.

`NaiveCatalogueBrowser` is what that looks like after three people have each
needed to walk the catalogue. Three methods, three hand-written copies of the
same page loop, and two of them are wrong. `countProducts()` hard-codes three
pages, so it is correct today and silently under-counts on the day a tenth
product is added. `findCheapest()` starts its page counter at one instead of
zero, never looks at page zero, and so never sees the four-pound socks — it
returns the eight-pound Coffee Mug, which is a real product at a real price,
correctly formatted, and not the cheapest thing in the shop. Neither bug
throws, neither is logged, and both can live in production indefinitely.

**What the pattern must deliver:** the page loop written exactly once, in a
class with a name that can be tested on its own; a catalogue that can be used
in a `for`-each loop without any caller naming a page; fetching that happens
only when a caller actually reaches the page, so stopping early costs nothing;
and two simultaneous walks over one catalogue that do not disturb each other.

---

## 3. Code

### Structure

6 production classes under `com.jk.explore.iterator`:

| Role | Types |
| --- | --- |
| Aggregate | `java.lang.Iterable` — not written here; the JDK's |
| Iterator | `java.util.Iterator` — not written here either |
| Concrete aggregate | `ProductCatalogue` — holds the feed, and no position at all |
| Concrete iterator | `CatalogueIterator` — package-private; every field on it is position |
| Awkward storage | `CatalogueFeed` — pages of three, and a counter of pages fetched |
| Element | `Product` — a record |
| Naive alternative | `NaiveCatalogueBrowser` — three methods, three loops |
| Entry point | `CatalogueDemo` |

### Requirements

1. **The page loop exists once.** `CatalogueIterator.hasNext` is the only place in the project that increments a page number or knows that an empty page means the end. Nothing else — not the catalogue, not the demo, not any test — contains a second copy.
2. **The aggregate holds no position.** `ProductCatalogue` has one field, the feed. It has no page number, no index and no `next()`, and `iterator()` returns a new instance on every call rather than a cached one, which is what makes two simultaneous walks possible.
3. **Fetching is lazy, and the build proves it.** `CatalogueFeed` counts its own calls, so the tests can assert that creating an iterator fetches nothing and that consuming two products fetches exactly one page of three. Moving the first fetch into a constructor turns that test red.
4. **Two iterators do not interfere.** A test advances one iterator over a catalogue and asserts the other is still at the first product. This is the test that catches the most common first-attempt mistake, which is putting the position on the aggregate.
5. **`hasNext()` is safe to call repeatedly.** It consumes nothing, so calling it twice in a row returns the same answer and skips no element; `next()` calls it rather than trusting the caller, and throws `NoSuchElementException` with a readable message at the end.
6. **The caller never names a page.** The demo's second section is a plain `for`-each loop, and the word `page` does not appear in it. Crossing a page boundary is invisible from outside the iterator.
7. **The naive alternative is argued against honestly.** Its `allProducts` method is correct and its author was not careless; the case against it is that the loop was written three times and so could be got wrong three ways. Both bugs are pinned by *passing* tests that assert the wrong behaviour, each paired with the same question put through the iterator.
8. **The cost is stated, not hidden.** The notes say that over an `ArrayList` this pattern is pure ceremony, that a `hasNext()` which consumes is a real and easy bug, and that `remove()` is left unimplemented on purpose — with an explanation of what it would have to do to work against a paged source.
9. **Java 21, no third-party runtime dependencies.** JUnit 5 for tests
   only, so the project is readable by someone who does not know a DI
   framework.
10. **Every class fits on a slide.** This is teaching code; a class that
   needs scrolling to read has failed its purpose regardless of its
   design.

### Verification

- `./gradlew build` passes. 13 test methods across `CatalogueIteratorTest`, `NaiveCatalogueBrowserTest`, `ProductCatalogueTest`.
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
| `iterator-pattern-explained.md` | The pattern, the code, pitfalls, comparisons |
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

The finished video is `video/iterator-pattern-explained.mp4`, with an
audio-only `.m4a` and a `.srt` subtitle track alongside it. It is built by
`video/build_video.sh`, from scenes declared in `video/scenes.py` and
slides rendered by `video/make_slides.py`.

### 5.1 The opening, in four steps

Scene 1 is the only scene whose narration has a required structure, and
it is required because it is the scene that decides whether anybody
watches the second one. It must run in this order:

1. **What the video is** — "This video explains the Iterator pattern in
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
| Runtime | ~10:23 over 14 scenes, 155 subtitle cues |  |

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
   truncate it, leading with the pattern name. Currently *"Iterator Pattern in Java - Paging the Catalog"*,
   45 characters. The suffix after the dash names the worked e-commerce scenario, so the title says what the viewer will actually watch rather than only which pattern it is about.
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
   order. For this project: Mediator.

> **Requirement.** Chapter timings are generated from the built `.srt`,
> never written by hand, by
> `python3 ../../docs/make_youtube_docs.py iterator`. They are the one part of
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
integrated, -3.79 dBTP true peak, and both streams start at 0.000.

---

## 9. Rebuilding

From the project root:

```bash
(cd video && ./build_video.sh)        # CPU-bound at CRF 18
```

Then, because the narration timings will have moved:

```bash
python3 ../../docs/make_youtube_docs.py iterator
python3 ../../docs/make_specs.py iterator
```

Changing the voice or the filter chain means listening to the result.
Changing the narration text means both of the above, and re-checking the
runtime claims in the top-level `README.md` and in `video/README.md`.
