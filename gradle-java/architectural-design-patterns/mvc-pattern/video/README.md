# MVC Pattern — Teaching Video

A narrated, slide-based video that teaches MVC using this project's code —
one order, two views, and the question of who is allowed to compute the
total.

## Output Files

| File | What it is |
| --- | --- |
| `mvc-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. Upload-ready for YouTube. |
| `mvc-pattern-explained.m4a` | Audio-only version. |
| `mvc-pattern-explained.srt` | Subtitles, timed from the encoded scene clips. |
| `poster.png` | The video's opening frame, 1920×1080. Not the thumbnail. |

**Narration:** female voice (macOS `Samantha`, US English), 145 words per
minute.

The `.mp4`, `.m4a` and `.srt` are build output and are not committed — run
`./build_video.sh` to produce them. `poster.png` *is* committed.

## Source Files

| File | Purpose |
| --- | --- |
| `narration.md` | The full spoken script, generated from `scenes.py` — edit the scenes, not the script. |
| `scenes.py` | Slide content and narration together. |
| `make_slides.py` | Renders one 1920×1080 PNG per scene. |
| `make_subtitles.py` | Generates the SRT. |
| `build_video.sh` | The whole pipeline. |
| `build/` | Generated slide images. |

## Rebuilding

```bash
./build_video.sh
```

The audio chain — no denoiser, two-pass loudness, lossless per-scene WAV
joined to a single AAC encode, `+faststart` and a dropped edit list — is
identical across every project in this repository and documented at length
in [`../../layered-architecture-pattern/video/README.md`](../../layered-architecture-pattern/video/README.md)
and, in full, in
[`../../../platform-design-patterns/externalised-configuration-pattern/video/README.md`](../../../platform-design-patterns/externalised-configuration-pattern/video/README.md).

### Requirements

- **macOS** — the narration uses the built-in `say` command
- **ffmpeg** — `brew install ffmpeg`
- **Python 3** with `pillow` and `matplotlib`

## Scene List

| # | Scene | Covers |
| --- | --- | --- |
| 1 | MVC | Title card, author credit, the plain-language definition of Model/View/Controller |
| 2 | The Scenario | Ada's £382.50 order, placed once, shown twice |
| 3 | Version One — No Separation At All | `EverythingOrderScreen`, and why it cannot be tested without a full checkout |
| 4 | Three Roles | Model, View, Controller — what each is not allowed to know |
| 5 | The Shortcut | `RoundedEmailView`'s bug: £382.50 on screen, £383.00 in the email |
| 6 | The Whole Mechanism, In One Interface | `OrderSummaryView`'s single narrow method |
| 7 | Classic MVC, And The MVC You Have Used | Observation versus web MVC's assemble-once model |
| 8 | MVP And MVVM, In One Scene | The passive view and the bound ViewModel |
| 9 | The Rule, Written Where A Build Can Read It | `ArchitectureTest`'s view/infrastructure rule |
| 10 | Watching It Go Red | The failure naming `RoundedEmailView` and `ProductTable` |
| 11 | The Forced Change | Adding the real second view, counted: 1 file added, 20 of 21 classes untouched |
| 12 | Both Views, Every Time | £382.50 on both, structurally guaranteed |
| 13 | The Bill | A narrow interface's real cost, and controllers that grow |
| 14 | When This Is Too Much | One output that will never grow a second |
| 15 | Thanks for Watching | The widen-the-model exercise, like, subscribe |

Scene 15 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force mvc`, then re-run
`./build_video.sh`. As with every project in this category, narration
describes structure as rules and directions in words — no line depends on
seeing the slide.

## Publishing Notes

Upload `mvc-pattern-explained.mp4`, with `../docs/thumbnail.png` as the
thumbnail and the `.srt` as the captions. Title, description, chapters and
tags live in [`../docs/youtube.md`](../docs/youtube.md).
