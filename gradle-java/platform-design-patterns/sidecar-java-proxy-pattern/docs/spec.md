# Sidecar with a Java Proxy Pattern — Project Specification

The single reference document for this project: what it teaches, how it
is built, and the quality bar its video and its YouTube publication have
to meet.

This is a *specification*, not a tutorial. It says what must be true and
why. The teaching material itself lives in
[`sidecar-java-proxy-pattern-explained.md`](sidecar-java-proxy-pattern-explained.md); the problem it
addresses is set out at length in
[`problem-statement.md`](problem-statement.md).

Where this document repeats a rule from the repository-wide
[`video-and-publishing-spec.md`](../../../docs/video-and-publishing-spec.md),
that document is the authority. This project's `video/build_video.sh` is generated from `creational/abstract-factory-pattern`'s, differing only in the pattern name and the output filenames, so a change to the pipeline belongs there and in the repository-wide spec, not here.

---

## 1. Purpose

Turn the previous project's biggest claim — that a sidecar is
language-independent, so the proxy can be replaced without touching the service
-- from a sentence into something a reader watches happen. It has one job and
it is not explaining what a sidecar is; §41 does that, and this project links
to it and moves on.

The three formats are not alternatives. A learner is expected to read the
problem statement, run the code, then watch the video — or watch first and
read after. Whichever order they choose, the class names, the numbers and
the scenario must be identical, because the value of the repository is
that a learner carries one e-commerce domain from pattern to pattern and
only has to absorb the new structure.

### Non-goals

- Not a second Sidecar lesson. The pattern belongs to §41. A draft that spends more than one scene on what a sidecar is for has drifted, and the README opens by naming §41 as the project to read first.
- Not a criticism of nginx. nginx wins on almost every count in the closing table and the project says so; the gap it has is narrow, deliberate, and a consequence of the case it was designed for.
- Not a network lesson. Tier 1 has no socket and no serialisation. The port is an object with something bound to it, and the phrase *separate process* is carried by the narration and by `real/`.
- Not a performance measurement. `Clock` counts milliseconds and never sleeps, so the arrival times are identical on every machine and assertable by a test.
- Not a recommendation to write your own proxy. Act 7 is longer than the benefit, and the rule it lands on is narrow: swap only when the thing you need cannot be said in the configuration language at all.

---

## 2. Problem statement

The full treatment is in [`problem-statement.md`](problem-statement.md).
In brief:

§41 finished with checkout taking payments through an nginx proxy running
beside it, and the service itself carrying no retry code, no deadline, no
certificate and no counter. That was the right outcome and this project keeps
all of it.

It shipped with a gap, and the gap is not a bug in anybody's code. The payment
provider asked every merchant for two things in writing: at most three attempts
per payment, **and wait properly between them**. nginx can say the first. It
cannot say the second — retrying means moving to the next server in an
upstream group, that move happens immediately, and there is no directive
anywhere in the http proxy module that introduces a delay first. So the shop's
configuration honours the half of the agreement that limits it and drops the
half that would have helped.

The consequence is exact and it is arithmetic. The provider wobbles for 300
milliseconds. The proxy makes its three allowed attempts at 1ms, 2ms and 3ms,
all of them inside the bad window, and the payment fails having spent the
entire allowance before the provider had time to get better. Nothing in the
service is wrong. Nothing in the configuration is wrong. The sentence that
would have fixed it does not exist in the language the configuration is
written in.

**What this project must deliver:** the same three attempts, spaced out, with
the service not rebuilt, not restarted and not told — and an honest accounting
of what writing your own proxy costs, because the answer is usually don't.

---

## 3. Code

### Structure

14 production classes under `com.jk.explore.sidecarjavaproxy`:

| Role | Types |
| --- | --- |
| The address the service talks to, and the only thing a swap touches | `LocalPort` |
| What may be bound to it | `Proxy` |
| The proxy §41 deployed, and its one gap | `NginxProxy` |
| The forty lines that close the gap | `JavaProxy` |
| The service, unchanged and never restarted | `PaymentsService` |
| The one policy both proxies read | `ProxyPolicy` |
| The supplier at the other end | `PaymentGateway` |
| The evidence, taken at the far end | `CallLog` |
| Time, counted and never slept | `Clock` |
| Presentation, not policy | `Money` |
| The values | `Payment`, `Receipt`, `PaymentFailed` |
| Entry point | `ProxySwapDemo` |

### Requirements

1. **The swap is proved by identity, not by behaviour.** `TheSwapTest.theServiceIsUntouched` asserts `assertSame` on the service's port and equality on its start number across the swap. A service that merely behaved the same afterwards would be a service somebody had carefully rebuilt.
2. **The demo could not restart the service if it wanted to.** There is exactly one `new PaymentsService(...)` in the whole program, in `main`, and `ServiceStaysEmptyTest` counts the constructions in the source with comments stripped to prove it.
3. **The argument is the spacing, and it is measured at the far end.** `TheSpacingTest` asserts nginx's three attempts arrive at 1ms, 2ms and 3ms and the Java proxy's at 1ms, 202ms and 603ms, using the provider's own recorded arrival times rather than anything a proxy says about itself.
4. **Neither proxy is greedier than the other.** Both spend exactly three attempts on the same payment against the same allowance; only one of them gets paid. The allowance is untouched, so the improvement costs the provider nothing.
5. **The nginx tests all pass.** They pin a boundary rather than a defect: the proxy does exactly what its configuration language can express, and the payment still fails.
6. **The service source is checked, not just exercised.** `ServiceStaysEmptyTest` opens `PaymentsService.java` with its comments stripped and fails if the words retry, backoff, keystore, truststore, timeout or tls appear in the code.
7. **The swap window is shown rather than skipped.** Act 6 vacates the port on a healthy network and prints `attempts that reached the provider: 0`, because the retry code that would have covered it was deleted in §41 on purpose, and concludes that a real swap is a rollout with the old proxy kept installable.
8. **The bill is longer than the benefit.** Act 7 prints the two proxies side by side with their languages and line counts, then lists what the 22 lines of somebody else's configuration brought for free and the 40 lines of your own do not: TLS termination, a structured access log, connection pooling, and twenty years of answered advisories.
9. **The rule it lands on is narrow.** Swap when the thing you need cannot be said in the configuration language at all — not when it is awkward, and not when you would rather write Java.
10. **Every quoted number is the program's.** `DemoRunsTest` captures the demo's output and asserts the arrival times, the start numbers, the zero-attempt window and the closing table.
11. **Java 21, no third-party runtime dependencies.** JUnit 5 for tests
   only, so the project is readable by someone who does not know a DI
   framework.
12. **Every class fits on a slide.** This is teaching code; a class that
   needs scrolling to read has failed its purpose regardless of its
   design.

### Verification

- `./gradlew build` passes. 30 test methods across `DemoRunsTest`, `ServiceStaysEmptyTest`, `SupportingTypesTest`, `TheSpacingTest`, `TheSwapTest`.
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
| `sidecar-java-proxy-pattern-explained.md` | The pattern, the code, pitfalls, comparisons |
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

The finished video is `video/sidecar-java-proxy-pattern-explained.mp4`, with an
audio-only `.m4a` and a `.srt` subtitle track alongside it. It is built by
`video/build_video.sh`, from scenes declared in `video/scenes.py` and
slides rendered by `video/make_slides.py`.

### 5.1 The opening, in four steps

Scene 1 is the only scene whose narration has a required structure, and
it is required because it is the scene that decides whether anybody
watches the second one. It must run in this order:

1. **What the video is** — "This video explains the Sidecar with a Java Proxy pattern in
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
| Runtime | ~19:58 over 17 scenes, 301 subtitle cues |  |

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
   truncate it, leading with the pattern name. Currently *"Sidecar in Java - Swapping the Proxy, Not the Service"*,
   53 characters. The suffix after the dash names the worked e-commerce scenario, so the title says what the viewer will actually watch rather than only which pattern it is about.
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
   order. For this project: Sidecar on Kubernetes.

> **Requirement.** Chapter timings are generated from the built `.srt`,
> never written by hand, by
> `python3 ../../docs/make_youtube_docs.py sidecar-java-proxy`. They are the one part of
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

Last verified: all eleven items pass. The delivered MP4 measures -16.00 LUFS
integrated, -3.81 dBTP true peak, and both streams start at 0.000.

---

## 9. Rebuilding

From the project root:

```bash
(cd video && ./build_video.sh)        # CPU-bound at CRF 18
```

Then, because the narration timings will have moved:

```bash
python3 ../../docs/make_youtube_docs.py sidecar-java-proxy
python3 ../../docs/make_specs.py sidecar-java-proxy
```

Changing the voice or the filter chain means listening to the result.
Changing the narration text means both of the above, and re-checking the
runtime claims in the top-level `README.md` and in `video/README.md`.
