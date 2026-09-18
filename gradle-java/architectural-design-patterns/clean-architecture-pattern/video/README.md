# Clean Architecture Pattern — Teaching Video

A narrated, slide-based video teaching Clean Architecture using this
project's code — the dependency-inversion moment shown in code, and the
largest forced change in the category.

## Output Files

| File | What it is |
| --- | --- |
| `clean-architecture-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `clean-architecture-pattern-explained.m4a` | Audio-only version. |
| `clean-architecture-pattern-explained.srt` | Subtitles. |
| `poster.png` | The video's opening frame. Not the thumbnail. |

**Narration:** female voice (macOS `Samantha`, US English), 145 words per
minute.

## Rebuilding

```bash
./build_video.sh
```

The audio chain is identical across every project in this repository; see
[`../../layered-architecture-pattern/video/README.md`](../../layered-architecture-pattern/video/README.md)
for the full explanation.

### Requirements

- **macOS** (for `say`), **ffmpeg**, **Python 3** with `pillow` and `matplotlib`

## Scene List

| # | Scene | Covers |
| --- | --- | --- |
| 1 | Clean Architecture | Title card, the plain-language definition, and an upfront admission of the overlap with Hexagonal |
| 2 | The Scenario | Ada's £382.50 order |
| 3 | The Naive Version | `NaivePlaceOrderInteractor`, naming three gateways directly |
| 4 | Four Circles, One Rule | Entities, use cases, interface adapters, frameworks & drivers |
| 5 | This Is Not Hexagonal Again | The four genuine differences, named precisely |
| 6 | The Real Graph, Wired By Hand | The composition root, twenty lines, no container |
| 7 | The Dependency-Inversion Moment | `orders.save(order)` — control out, dependency in |
| 8 | Wired By Hand, On Purpose | Why there is no DI container in this project |
| 9 | Add Two Things At Once | The forced change: a new controller and a new gateway, added together |
| 10 | Both Paths, Proven Rather Than Narrated | The counted bill, and `BothAddedAtOnceTest` |
| 11 | The Rule, As ArchUnit's Own API | `Architectures.layeredArchitecture()` |
| 12 | Watching It Go Red | The failure naming `NaivePlaceOrderInteractor` |
| 13 | The Bill | Fourteen files for one feature — the most over-applied pattern here |
| 14 | When This Is Too Much | The honest boundary |
| 15 | Thanks for Watching | The third-delivery-mechanism exercise |

Scene 15 deliberately does not name whichever pattern comes next. Scene 8
mentions, in passing, that a companion project assembles this same graph
with a container — not as a publishing-order promise, but because the
category's own plan requires this project to point forward to it.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force clean-architecture`, then
re-run `./build_video.sh`.

## Publishing Notes

Upload `clean-architecture-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
