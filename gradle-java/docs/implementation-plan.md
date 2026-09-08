# Implementation Plan

How the fourteen projects are brought up to
[`video-and-publishing-spec.md`](video-and-publishing-spec.md).

---

## Current state

**Phases 1–7 are complete.** All fourteen projects pass every item of the
spec's conformance checklist; the per-item evidence is in
[Phase 7 — Verify](#phase-7--verify) below. The table in this section records
the position *before* the work started, and is kept because the plan is easier
to read against it.

Audited before planning. Every project builds, tests pass, and every project
has a `video/` pipeline that produces a real narrated MP4. The gaps are:

| Area | State |
| --- | --- |
| Domain | 13 of 14 are e-commerce. **proxy** uses a photo gallery. |
| Narration rate | All 14 at 165 wpm. Spec says 145. |
| Audio pipeline | 8 of 14 fixed (7 creational + proxy). **6 structural still concatenate per-scene AAC** and still run `afftdn`. |
| Poster | All 14 strike out the "before" sample. **proxy's poster is the decorator poster** — wrong title, wrong content. |
| `docs/youtube.md` | Missing from all 14. |

### The two defects worth naming

**Per-scene AAC concatenation.** The six structural projects listed above
encode each scene to AAC and join the results with `-c copy`. Because AAC is a
lapped format this leaves a hole in the timeline at every scene change; the
abstract-factory video measured 30 gaps totalling 31 seconds before the fix.
Their published videos are audibly broken and must be re-encoded, not patched.

**The proxy poster.** `structural/proxy-pattern/video/make_slides.py` was
copied from decorator and `kind_poster` was never updated. The rendered
`poster.png` reads "DECORATOR PATTERN" and shows decorator's code samples. It
would have gone to YouTube as the thumbnail of the proxy video.

---

## Order of work

Sequenced so that nothing is rendered or encoded twice. Everything that changes
what the video *contains* lands before anything is built, and the fourteen
builds run last, once.

### Phase 1 — Re-domain proxy to e-commerce

Proxy moves from a photo gallery to product imagery on a listing page. The
structure is unchanged, which is what makes this a rename plus a rewrite of the
prose rather than a new project:

| Now | Becomes |
| --- | --- |
| `Photo` | `ProductImage` |
| `HighResolutionPhoto` | `HighResolutionProductImage` |
| `PhotoProxy` | `LazyProductImage` (virtual proxy) |
| `AccessControlledPhotoProxy` | `RestrictedProductImage` (protection proxy) |
| `NaivePhotoGallery` | `NaiveProductListing` |
| `NaiveSecurePhotoViewer` | `NaiveAdminImageViewer` |
| `PhotoGalleryDemo` | `ProductImageDemo` |
| `Role.VIEWER` / `Role.ADMIN` | `Role.SHOPPER` / `Role.CATALOG_ADMIN` |

The scenario: a category page shows sixty listings. Each has a
full-resolution image that is expensive to decode, and only a handful are ever
scrolled into view. Some images — unreleased products, supplier-restricted
assets — may only be viewed by catalog staff. Both concerns belong outside the
image itself.

Touches sources, tests, all seven `docs/` files, both Mermaid diagrams and
their PNGs, `video/scenes.py`, `video/make_slides.py` (`kind_diagram`),
`narration.md`, and the two READMEs. Verified with `./gradlew build` and by
running `./gradlew run` and pasting the real output into the README.

### Phase 2 — Poster redesign, all 14

One change to a shared helper, applied to every project:

- `pill()` loses its `strike` parameter and gains a `tag` parameter.
- The tag renders as a small chip on the pill's top edge: `BEFORE` on the rose
  pill, `AFTER` on the green one.
- Every `kind_poster` swaps `strike=True` for `tag="BEFORE"`, and the
  right-hand pill gains `tag="AFTER"`.
- proxy's `kind_poster` is additionally rewritten from scratch for the correct
  pattern.

The contrast that made the old poster informative is kept; only the
strikethrough goes. See spec §6.

Each of the fourteen posters is rendered and **visually inspected** before the
phase is closed — this is exactly the failure that produced a decorator poster
in the proxy project, and only looking at the image catches it.

### Phase 3 — Audio pipeline, the 6 remaining structural projects

The fixed `build_video.sh` is generated from the abstract-factory reference by
substituting the title and the output file names, as was done for the
creational batch. That brings all six onto PCM-per-scene, a single AAC encode,
two-pass linear `loudnorm`, the chain-3 `CLEANUP`, and the gap check.

Their `video/README.md` files get the same corrected pipeline description the
other eight already have.

### Phase 4 — Narration rate to 145

`RATE` default changes from 165 to 145 in all fourteen scripts. One line each;
no other change. Runtimes grow by roughly 14 %.

### Phase 5 — Build all fourteen videos

Sequential, in the background, gated on the built-in continuity check. Each
build renders slides, narrates, encodes per-scene clips, concatenates, muxes,
generates subtitles, and fails if the audio timeline has a gap.

Roughly 10–20 minutes per project. Any project whose check fails is diagnosed
and rebuilt before the phase closes.

### Phase 6 — `docs/youtube.md` for all 14

Written last, because the chapter timings are read from the `.srt` files that
phase 5 produces. Seven sections as specified in spec §8, generated per project
from `scenes.py` (chapter titles) and the `.srt` (timings), with the title,
description, tags and end-screen link written by hand per pattern.

### Phase 7 — Verify

Walk the spec's conformance checklist against all fourteen projects and report
the result per project.

**Result: all fourteen pass all ten items.** How each was established, so that
a re-verification does not have to re-invent the method:

| Item | How it was checked |
| --- | --- |
| E-commerce domain | The worked scenario named in each top-level README |
| Build and run | `./gradlew build` in all fourteen, then `run` twice per project, diffed against the README's output block |
| `RATE` 145, Samantha | Both defaults read out of `build_video.sh` |
| `CLEANUP` per §4.1 | No `afftdn` and no `lowpass` in executable lines — the names survive only in the comments explaining why they were removed |
| PCM per scene, one AAC | `pcm_s16le` present and exactly one `-c:a aac`, at the mux |
| Two-pass `loudnorm` | `print_format=json` measurement feeding `measured_I=…:linear=true` |
| Gap check | The check is present in every script, and every build printed `no gaps` |
| Poster | All fourteen 1920×1080, each carrying its own pattern name, none drawing a strikethrough |
| `youtube.md` | All seven sections present; every chapter timestamp matched a cue start in the project's current `.srt`, first at `00:00` |
| `video/README.md` | Describes lossless per-scene WAV, the single AAC encode, `linear=true`, `RATE` 145, and the absence of a denoiser |

Two things worth recording because they were not obvious going in.

The "output matches the README" item was **not** met by any project at the
start of this phase: no README quoted the program's output at all, and no
document anywhere reproduced it. The output is now quoted in all fourteen and
verified against a second, independent run. Three demos — simple factory,
factory method and facade — mint an identifier per run, so their transaction,
order and tracking codes differ every time. Those READMEs say so, and the spec
item was reworded to match rather than pretending the output is byte-stable.

Beyond the checklist, every finished MP4 was measured: all fourteen sit at
−16.0 LUFS integrated with true peak below −3.5 dBTP and no silence longer
than three seconds. That is a level and dropout check, not a fidelity one —
see the risk below, which still stands.

---

## Risks

**Build time.** Fourteen full builds at CRF 18 is a few hours of wall clock,
and each is CPU-bound. They run sequentially in the background; a failure part
way through does not invalidate what came before, because each project's build
is independent.

**The continuity check is not a quality check.** It verifies that no audio
packet is missing. It cannot hear warbling, clipping, or a bad voice — the
`afftdn` problem passed it cleanly. A listen to at least one finished video is
required before the work is called done.

**Re-domaining proxy touches prose in eight files.** The risk is a stale
reference to a photo surviving in one of them. Mitigated by grepping the whole
project for the old vocabulary after the rewrite, not by re-reading each file.

**Chapter timings go stale.** Any later change to narration or rate invalidates
every `youtube.md` chapter list. They are generated from the `.srt`, so
regenerating is cheap, but it has to actually be done.
