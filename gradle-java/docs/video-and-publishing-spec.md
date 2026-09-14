# Video and Publishing Specification

The standard every pattern project under `gradle-java/` is built to. It covers
the worked domain, the narration, the audio and video pipeline, the poster and
thumbnail, and the YouTube publishing document.

This document is the *what*. The companion
[`implementation-plan.md`](implementation-plan.md) is the *how* — the ordered
plan for bringing the fourteen existing projects up to this standard.

A project is compliant when every item in [Conformance](#conformance) holds.

---

## 1. Scope

Thirty-seven projects across four categories, each a self-contained Gradle
Java 21 project with sources, JUnit 5 tests, `docs/`, `video/`, and a top-level
`README.md`:

| Category | Projects |
| --- | --- |
| Creational | abstract-factory, builder, factory-method, prototype, simple-factory, singleton, static-factory |
| Structural | adapter, bridge, composite, decorator, facade, flyweight, proxy |
| Behavioural | strategy, observer, command, template-method, state, chain-of-responsibility, iterator, mediator, memento, visitor, interpreter |
| Microservices | api-gateway, service-discovery, load-balancing, retry, circuit-breaker, bulkhead, database-per-service, api-composition, cqrs, saga, transactional-outbox, idempotent-consumer |

Two categories have their own subsidiary specification, each fixing the
e-commerce scenario its patterns are taught through and adding
category-specific conformance items. Both inherit this document unchanged;
where any of them appears to disagree with it, this one wins.

| Specification | Covers |
| --- | --- |
| [`../behavioural/docs/spec.md`](../behavioural/docs/spec.md) | The eleven behavioural patterns, plus four extra conformance items |
| [`../micro-services-design-patterns/docs/spec.md`](../micro-services-design-patterns/docs/spec.md) | The twelve microservices patterns, their one-JVM rule, and six extra conformance items |

---

## 2. The worked domain: e-commerce, everywhere

**Every project teaches its pattern through an online store.** Not a photo
gallery, not a document editor, not shapes on a canvas — a store.

The reason is that these projects are meant to be worked through in sequence.
A learner who has already met orders, line items, carts, catalogs and shipping
in the previous project spends none of their attention re-learning the setting
and all of it on the structure being introduced. Switching domains per pattern
would make each project cheaper to write and the series harder to follow.

Acceptable subject matter is anything a real store contains: checkout,
pricing and discounts, the product catalog and its imagery, orders and order
numbers, payments, shipping and couriers, inventory, notifications, invoices,
taxes, and regional differences between markets.

When a pattern's classic textbook example is not e-commerce, the pattern is
re-framed rather than the domain relaxed. Proxy, for instance, is classically
taught with a lazily loaded image; here it is a *product* image on a listing
page — the same structure, inside the store.

Each project must pick a scenario where the pattern is genuinely the right
answer. A contrived e-commerce wrapper around a non-e-commerce idea is worse
than a clean example, because the honest "when not to use this" section that
every project carries then has nothing to stand on.

---

## 3. Narration

| Setting | Value | Why |
| --- | --- | --- |
| Voice | macOS `Samantha`, US English | The only non-novelty voice installed on the build machine. Consistent across every project so the series sounds like one series. |
| Rate | **145 wpm** (`RATE` in `build_video.sh`) | See below. |
| Inter-scene pause | **0.9 s** (`apad=pad_dur=0.9`) | A clear beat between topics, so slides do not snap past and the viewer has a moment to read the new slide before the voice starts on it. |

### Why 145 words per minute

Conversational English runs at roughly 150 wpm, and audiobooks are narrated at
150–160. Instructional video sits deliberately below that: the viewer is
reading code on screen at the same time as listening, which is two demands on
the same attention, and unlike a live talk they cannot ask you to repeat
yourself.

The band that educational YouTube converges on is **140–160 wpm**, and
technical content with code on screen belongs at the lower end of it. 145 is
that lower end: unhurried enough to follow a class name being spelled out,
quick enough that a viewer does not reach for the 1.25x button — which is the
real failure mode of slow narration, because once they speed the video up they
have taken back the pacing you were trying to give them.

Slower than about 120 wpm is counterproductive for this material. It reads as
laboured rather than careful, and it inflates a ten-minute explanation into
half an hour, which measurably costs watch-through.

Rate is an environment variable, so any project can be re-narrated at another
speed without editing anything:

```bash
RATE=130 ./build_video.sh
```

### Script conventions

Narration lives in the `narration` field of each scene in `video/scenes.py`,
beside the slide it belongs to, so the two cannot drift apart. `narration.md`
is the human-readable copy for review.

- `[[slnc NNN]]` inserts an NNN-millisecond pause. These are instructions to
  `say`, not words; `make_subtitles.py` strips them.
- Words the synthesiser mishandles are spelled phonetically — "V A T" rather
  than "VAT".
- Scene 1 credits the author aloud; the final scene asks for the like and the
  subscribe.

### The opening, in four steps

The first scene (`01-poster`) is the only one whose narration has a required
structure, and it is required because it is the scene that decides whether
anybody watches the second one. It must proceed in this order:

1. **Say what the video is.** "This video explains the *X* design pattern in
   Java." Plainly, before anything else, so a viewer who arrived from a search
   result knows within four seconds that they are in the right place.
2. **Credit the author.** "…and it is written and presented by Jayasekhar
   Konduru."
3. **Give the pattern's definition, in general terms.** Two or three sentences
   of plain language saying what the pattern is and what it does, with no
   reference yet to the store, the catalog or the checkout. A viewer who stops
   the video here should still have learnt what the pattern is.
4. **Then the same thing in full, in the e-commerce domain.** The worked
   scenario, and what the viewer will be able to do by the end.

The reason for the order is that steps 3 and 4 used to be one step. The video
opened with the shop's scenario, and the general definition of the pattern was
left for the viewer to infer from a worked example — which works for somebody
already halfway to knowing it and fails for everybody else. The abstract
statement now comes first and the e-commerce scenario elaborates it, rather
than being the viewer's first encounter with the idea.

This costs fifteen to thirty seconds of runtime per video. That is the correct
trade: it is spent at the only point in the video where a viewer is still
deciding whether to leave.

---

## 4. Audio pipeline

The narration must be clean, evenly levelled, and **continuous** — no dropouts,
no seams at scene changes.

### 4.1 Filter chain

`say` emits 22.05 kHz mono; the AAC track needs 48 kHz stereo. The `CLEANUP`
chain in `build_video.sh` does that conversion and nothing more:

```
aresample=48000:filter_size=512:cutoff=0.98:linear_interp=1
highpass=f=75
equalizer=f=3000:t=q:w=1.5:g=1.5
```

- **`aresample`** with a long filter, so the upsampling itself adds no grit.
- **`highpass`** removes rumble below the voice.
- **`equalizer`** lifts 3 kHz slightly, where consonants live, for intelligibility.

**No spectral denoiser.** An earlier revision ran `afftdn` here and it looked
like an improvement by the numbers — about 15 dB off the noise floor — but it
made the voice audibly worse. A spectral denoiser works by subtracting an
estimated stationary noise floor; synthesised speech has almost none, so
`afftdn` subtracts speech instead and leaves it warbling. The faint residual
hiss is much the lesser problem. **Do not add a denoiser back without an A/B
listen.**

**No `lowpass`.** Band-limiting the top end removed air from an already dull
22 kHz source for no measurable gain.

### 4.2 Encode structure

The single most important rule:

> **Audio stays lossless until the final mux, and is encoded to AAC exactly
> once.**

AAC is a lapped format. Every separately encoded segment carries priming
samples at its head and padding at its tail, and `ffmpeg -f concat -c copy`
can strip neither. Concatenating per-scene AAC therefore punches a hole in the
timeline at *every* scene change — this measured as 30 gaps totalling 31
seconds of missing narration in a single 9-minute video.

So:

1. Each scene's narration is written as `pcm_s16le` WAV at 48 kHz stereo.
2. Video-only scene clips are encoded separately (`-an`).
3. Video clips are concatenated with `-c copy`; WAVs are concatenated as PCM.
4. The whole narration is encoded to AAC **once**, at the mux.

### 4.3 Loudness

`loudnorm=I=-16:TP=-1.5:LRA=11` — YouTube's target — applied **once over the
whole narration, in two passes**.

Per-scene levelling is wrong: it re-measures on every clip, so a quiet scene is
pushed up to match a loud one and the level audibly steps at each join.

Two passes rather than one because single-pass `loudnorm` runs in dynamic mode,
riding the level as it goes, and on some narrations it emits a timestamp
discontinuity partway through — an audible hole mid-sentence with nothing wrong
upstream of it. Measuring first and feeding the numbers back with `linear=true`
reduces it to one constant gain, which cannot do that, and which also stops it
pumping between quiet and loud lines.

### 4.4 A/V sync

Per scene, `frames = ceil(audio_duration * 30)` and the audio is padded to
exactly `frames / 30` seconds. Picture and narration are then the same length
in every scene, so slide changes cannot drift however long the video grows.

### 4.5 The self-check

After the mux, `build_video.sh` reads every audio packet timestamp and **fails
the build** if any two are more than 1.5 AAC frames apart. Both failure modes
above — concat seams and the `loudnorm` discontinuity — are easy to miss in a
spot check and ruin the whole video, so they are worth failing over.

A passing build prints:

```
audio timeline continuous: 25666 packets, no gaps
```

This check verifies *continuity*, not *fidelity*. It would not have caught the
`afftdn` problem. Quality changes still need a listen.

---

## 5. Video

| Property | Value |
| --- | --- |
| Resolution | 1920×1080 |
| Codec | H.264, `-preset slow -crf 18`, `yuv420p` |
| Frame rate | 30 fps |
| B-frames | disabled (`-bf 0`) |
| Audio | AAC 192 kbps, 48 kHz, stereo |
| Container | MP4 with `+faststart` |

`-bf 0` because B-frames save nothing on a static slide and push the video
track's first timestamp past the audio's, leaving players showing black at
0:00. For the same reason the mux drops the AAC priming edit list
(`-ignore_editlist 1`) so both streams start at 0.000.

Outputs per project, none committed:

| File | Purpose |
| --- | --- |
| `{pattern}-pattern-explained.mp4` | The video |
| `{pattern}-pattern-explained.m4a` | Audio-only, for revision |
| `{pattern}-pattern-explained.srt` | Subtitles, timed from the encoded clips |
| `poster.png` | Title card and YouTube thumbnail |

---

## 6. Poster and thumbnail

`poster.png` is the video's first frame *and* its YouTube thumbnail. It is the
only thing most people will ever see of the video, so it is held to the
strictest rules in this document.

### 6.1 Never strike out the message

**No strikethrough anywhere on the poster.** Earlier posters drew a rule
through the "before" code sample to mark it as the rejected approach. This is
banned:

- struck-through monospace is hard to read at full size and unreadable at the
  ~360×202 px YouTube serves in search results, which is the size that actually
  matters;
- it makes the card read as negative — as being about what is wrong — when the
  poster's job is to make the pattern look worth learning.

The before/after contrast stays, because it is what makes the card
informative. It is carried by **colour and a label**: the left pill is rose,
tagged `BEFORE`; the right is green, tagged `AFTER`. Both code samples remain
fully legible.

### 6.2 Layout

Fixed across every project so the series is recognisable as a set:

| Element | Position |
| --- | --- |
| Accent bar | full width, top edge |
| Eyebrow — `DESIGN PATTERNS - JAVA` | top left |
| Pattern name, two lines | left, 120–128 pt, second line in the accent colour |
| Short rule | under the title |
| Comparison panel | one rounded box holding both pills, the arrow, and the tagline |
| Tagline | centred in the panel, one line, ≤ 48 characters |
| Author pill | bottom left |

Bottom right and the last ~40 px of height are left clear: YouTube's duration
badge and watched-progress bar sit there.

### 6.3 Legibility rules

- Nothing smaller than 34 pt.
- Code samples auto-shrink to fit their pill; if a sample needs below 30 pt it
  is too long — shorten the sample, not the font.
- Every text colour is at least 4.5:1 against its background.
- The pattern name must be readable when the image is scaled to 20 % — check
  it, do not assume it.

---

## 7. Project documentation

Each project carries, under `docs/`:

| File | Content |
| --- | --- |
| `prerequisites.md` | What to know and install first |
| `problem-statement.md` | The problem, and why the naive approach hurts |
| `{pattern}-pattern-explained.md` | The pattern, the code, pitfalls, comparisons |
| `class-diagram.md` + PNG | Static structure |
| `uml-diagram.md` + PNG | Runtime call flow |
| `animation.html` | Step-by-step walkthrough, with optional narration |
| `make_animation_audio.sh` | Generates `docs/audio/step-N.m4a` |
| `session.md` | A 60-minute guided teaching session |
| **`youtube.md`** | **Publishing document — see below** |
| **`thumbnail.png`** | **1280×720 YouTube thumbnail, generated by `docs/make_thumbnails.py`** |

Plus `video/` (scenes, slides, subtitles, build script, `narration.md`,
`README.md`) and a top-level `README.md`.

---

## 8. `docs/youtube.md`

One file per project holding everything needed to publish, so uploading is
copy-and-paste rather than reconstruction. Required sections:

1. **Title** — the exact string to paste. ≤ 60 characters so it is not
   truncated in search results. Leads with the pattern name.
2. **Description** — the full text. The first two lines are what shows above
   the fold, so they carry the hook, not boilerplate. Then what the video
   covers, the chapter list, the repository link, and the prerequisites.
3. **Chapters** — `mm:ss Title`, one per scene, first entry `00:00`. YouTube
   requires at least three and the first at zero to render them as chapters.
   Timings come from the generated `.srt`, so they are regenerated when the
   narration changes.
4. **Tags** — a comma-separated list, under 500 characters total.
5. **Thumbnail** — the path to `docs/thumbnail.png`, with a note that it
   is generated by `docs/make_thumbnails.py` and must be uploaded
   manually. This is a separate image from `video/poster.png`: the
   poster is the video's 1920×1080 opening frame and carries the
   before/after comparison, which is unreadable once YouTube scales it
   to search-result size. The thumbnail is 1280×720 and carries only
   the pattern name, one line of promise, and one short piece of code.
6. **Upload checklist** — subtitles, language, thumbnail, HD processing, the
   playlist the video belongs to.
7. **Cards and end screen** — which video to link to next, following the
   learning order.

Chapter timings are the one part of this file that can silently go stale; they
must be regenerated whenever the narration is re-recorded.

---

## 9. Conformance

A project is compliant when all of the following hold:

- [ ] The worked example is e-commerce.
- [ ] `./gradlew build` passes; the README quotes the real `./gradlew run`
      output under the run command, and it still matches. Three projects
      (simple factory, factory method, facade) mint an identifier per run, so
      their transaction, order and tracking codes are expected to differ; every
      other line must match, and the README says so.
- [ ] Scene 1's narration follows the four-step opening of §3 — what the
      video is, the author credit, the pattern's definition in general
      terms, and only then the e-commerce scenario.
- [ ] `RATE` is 145 and `VOICE` is Samantha.
- [ ] `CLEANUP` matches §4.1 exactly — in particular, contains no `afftdn` and no `lowpass`.
- [ ] Per-scene audio is PCM; exactly one AAC encode, at the mux.
- [ ] `loudnorm` is two-pass with `linear=true`.
- [ ] The build prints `audio timeline continuous: N packets, no gaps`.
- [ ] `poster.png` shows the correct pattern name and contains no strikethrough.
- [ ] `docs/youtube.md` exists with all seven sections, and its chapter timings match the current `.srt`.
- [ ] `video/README.md` describes the pipeline as it actually is.
