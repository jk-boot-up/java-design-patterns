# Hexagonal Architecture Pattern — Teaching Video

A narrated, slide-based video teaching Ports and Adapters using this
project's code — one core, four ports, and two kinds of adapter, swapped
independently.

## Output Files

| File | What it is |
| --- | --- |
| `hexagonal-architecture-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `hexagonal-architecture-pattern-explained.m4a` | Audio-only version. |
| `hexagonal-architecture-pattern-explained.srt` | Subtitles. |
| `poster.png` | The video's opening frame. Not the thumbnail. |

**Narration:** female voice (macOS `Samantha`, US English), 145 words per
minute.

## Rebuilding

```bash
./build_video.sh
```

The audio chain is identical across every project in this repository; see
[`../../layered-architecture-pattern/video/README.md`](../../layered-architecture-pattern/video/README.md)
for the full explanation of why it is built the way it is.

### Requirements

- **macOS** (for `say`), **ffmpeg**, **Python 3** with `pillow` and `matplotlib`

## Scene List

| # | Scene | Covers |
| --- | --- | --- |
| 1 | Hexagonal Architecture | Title card, the plain-language definition of ports and adapters |
| 2 | The Scenario | Ada's £382.50 order, and the four things the core needs |
| 3 | The Naive Version | `NaivePlaceOrderService`, naming three adapters directly |
| 4 | Ports, Declared By The Core | The four interfaces, and the "who names whom" test |
| 5 | One Move From The Project Before It | The exact difference from Layered Architecture |
| 6 | The Core, Driven By HTTP | A simulated request, and the core's two imports |
| 7 | The Half Most Treatments Skip | Driven versus driving, and why both must be shown |
| 8 | The Same Core, Driven By A CLI Instead | The driving-side proof |
| 9 | The Rule, Written Where A Build Can Read It | `ArchitectureTest`'s core/adapter rule |
| 10 | Watching It Go Red | The failure naming `NaivePlaceOrderService` |
| 11 | The Forced Change, Both Halves At Once | Storage and calling-side swapped together, counted |
| 12 | The Bill | Interfaces for one implementation, and mapping cost |
| 13 | When This Is Too Much | The honest question about whether a swap will ever happen |
| 14 | Thanks for Watching | The third-driving-adapter exercise |

Scene 14 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force hexagonal-architecture`, then
re-run `./build_video.sh`.

## Publishing Notes

Upload `hexagonal-architecture-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
