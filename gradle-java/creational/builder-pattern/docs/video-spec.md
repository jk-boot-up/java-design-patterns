# Teaching Video Specification

This is the specification the video in [`../video/`](../video/) is built to. It
describes *what the video must be*, not how to run the build — for the build
steps see [`../video/README.md`](../video/README.md).

This file is a port of
[`../../static-factory-pattern/docs/video-spec.md`](../../static-factory-pattern/docs/video-spec.md),
which is the portable contract every teaching video in these repositories is
built to. Only §11 (this project's scenes) and the identifiers named in §4 and
§12 differ from that original.

---

## 1. What gets produced

One build produces exactly four artefacts, all in `video/`:

| File | Format | Purpose |
| --- | --- | --- |
| `builder-pattern-explained.mp4` | 1920×1080, H.264 High, 30 fps, yuv420p, AAC-LC 192 kbps stereo @ 48 kHz, `+faststart` | The video. Uploaded to YouTube as-is. |
| `builder-pattern-explained.m4a` | AAC 192 kbps stereo | Audio-only, for revision on the move. |
| `builder-pattern-explained.srt` | SubRip | Captions. Uploaded alongside the video. |
| `poster.png` | 1920×1080 PNG | The opening frame, used as the custom thumbnail. |

None of the four are committed. They are build output; the scripts that produce
them are what lives in git. This project's `.gitignore` therefore carries:

```
/video/*.mp4
/video/*.m4a
/video/*.srt
/video/poster.png
/video/build/
```

**Target runtime: 10–13 minutes.** Long enough to teach the idea from nothing,
short enough that a student finishes it. That works out at roughly 15–19
scenes.

---

## 2. Source layout

Six files, all in `video/`, and no others:

| File | Responsibility |
| --- | --- |
| `scenes.py` | The single source of truth: slide content *and* the narration spoken over it, in one `SCENES` list. |
| `make_slides.py` | Renders one 1920×1080 PNG per scene into `build/`. |
| `make_subtitles.py` | Writes the SRT, timed from the encoded scene clips. |
| `build_video.sh` | The whole pipeline, one command, no arguments. |
| `narration.md` | The full spoken script, generated from `scenes.py`, for human review. |
| `README.md` | How to rebuild, what the options are, and how to publish. |

The rule behind this layout is that **slide and narration never live apart**. A
scene is a `dict` holding `key`, `kind`, `title`, `body` and `narration`
together, so it is impossible to reword the narration and forget the slide, or
the other way round.

---

## 3. The pipeline

`build_video.sh` runs five stages and nothing else:

1. **Slides.** `make_slides.py` renders `build/<key>.png` per scene.
2. **Narration text.** Each scene's `narration` string is written to
   `build/<key>.txt`.
3. **Speech and per-scene clips.** macOS `say` speaks each `.txt` to AIFF; the
   AIFF is cleaned (§6), padded with a 0.9 s tail, and married to its PNG as
   `build/scene-<key>.mp4`.
4. **Concatenation.** The concat demuxer joins the clips with `-c copy`, then a
   second lossless remux applies the two opening-frame fixes (§7). The audio
   track and `poster.png` are lifted out here.
5. **Subtitles.** `make_subtitles.py` measures the encoded clips and writes the
   SRT.

Intermediates are deleted afterwards unless `KEEP_INTERMEDIATE=1` is set. The
slide PNGs are kept.

**Requirements:** macOS (for `say`), `ffmpeg`, and Python 3 with `pillow` and
`matplotlib`. `matplotlib` is a dependency only for the DejaVu TTFs it bundles,
which is what makes the slides render identically on any machine without a
font install.

---

## 4. The slide system

Canvas is 1920×1080 throughout. Background `#0F172A`, with an accent rule
across the top eight pixels. The palette, scene kinds, and the two hard rules
for `code` and `console` scenes are unchanged from the original spec — see
[`../../static-factory-pattern/docs/video-spec.md`](../../static-factory-pattern/docs/video-spec.md)
§4 for the full table. The only project-specific change is the footer label,
`Builder Pattern  ·  Java 21`, and the identifiers the syntax-colouring rules
in `make_slides.py` look for (`PurchaseOrder`, `Builder`, `Address`, `Money`
in place of `Discount`, `Money`).

---

## 5. Branding

Unchanged from the original spec. Every video opens and closes with the same
two cards — the poster doubling as the YouTube thumbnail, the outro asking for
the like and the subscribe — and the author credit sits in the same pill, at
the same position, for the same reason. See §5 of the original for the full
rationale.

The narration of scene 1 credits the author out loud: *"This one is written and
presented by Jayasekhar Konduru."*

---

## 6. Narration

**Voice: `Samantha`, US English, female. Rate: 165 wpm.** Unchanged from the
original spec, for the same reason: consistency across every video in the
collection.

The same three conventions apply — explicit `[[slnc NNN]]` pauses, maths and
symbols spelled out, no references the video cannot show. See §6 of the
original spec for the reasoning behind each.

`narration.md` is regenerated from `scenes.py` whenever the wording changes
substantially. It is the review copy, never the source.

---

## 7. Audio and container correctness

Unchanged from the original spec — the same `CLEANUP` filter chain, and the
same three settings (`-bf 0`, `-ignore_editlist 1`, `+faststart`) for the
opening frame. See §7 of the original for the full explanation of why each one
is necessary.

---

## 8. Subtitles

Unchanged from the original spec — cues are timed from the encoded scene
clips, not the raw narration audio, for the reason given in §8 there.

---

## 9. Verification

A build is not finished until it has been measured. The same commands from §9
of the original spec apply, with `builder-pattern-explained.mp4` /
`.srt` in place of the static factory filenames.

---

## 10. Publishing

Unchanged from the original spec. See §10 there for the click-by-click
YouTube instructions; `video/README.md` in this project carries the
project-specific description text.

---

## 11. This project's scenes

Nineteen scenes, matching the shape of the original.

| # | Kind | Scene |
| --- | --- | --- |
| 1 | poster | Builder Pattern |
| 2 | bullets | The Job |
| 3 | code | The Constructor With Nine Parameters |
| 4 | code | Telescoping Constructors |
| 5 | bullets | Why That Hurts |
| 6 | quote | The Builder Pattern |
| 7 | bullets | A Made-to-Order Sandwich Counter |
| 8 | diagram | The Shape of It |
| 9 | code | Required Facts, Optional Pieces |
| 10 | code | One Method, One Piece |
| 11 | code | A Rule That Lives in One Place |
| 12 | code | Checked Only When You Say You're Done |
| 13 | code | The Product Stops Watching the Builder |
| 14 | code | The Director, the Java Way |
| 15 | console | Running It |
| 16 | bullets | Where It Stops |
| 17 | bullets | How It Relates to the Others |
| 18 | title | One Sentence to Keep |
| 19 | outro | Thanks for Watching |

The shape is the same one the original spec argues for, and it still holds:
**pose the problem → show the obvious answer failing → name the technique →
give it a physical analogy → draw the structure → walk the real code → run it
→ say where it stops → one sentence to keep.**

---

## 12. Porting this to a new project

Unchanged process from §12 of the original spec. This project is itself an
example of following it: `make_slides.py`, `make_subtitles.py` and
`build_video.sh` were copied over, the `OUT_*` names and footer label were
renamed, `kind_diagram` was redrawn for this project's structure, the
syntax-colouring identifiers were updated, `scenes.py` was written fresh
following §11's shape, and the real demo output in the `console` scene was
pasted from an actual `./gradlew run`.
