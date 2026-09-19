# Thread Pool Pattern — Teaching Video

A narrated, slide-based video that teaches Thread Pool using this
project's code, picking up directly from Producer–Consumer's queue and
harness.

## Output Files

| File | What it is |
| --- | --- |
| `thread-pool-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `thread-pool-pattern-explained.m4a` | Audio-only version. |
| `thread-pool-pattern-explained.srt` | Subtitles. |
| `poster.png` | The video's opening frame. Not the thumbnail. |

**Narration:** female voice (macOS `Samantha`, US English), 145 words per
minute.

## Rebuilding

```bash
./build_video.sh
```

The audio chain is identical across every project in this repository; see
[`../../../architectural-design-patterns/layered-architecture-pattern/video/README.md`](../../../architectural-design-patterns/layered-architecture-pattern/video/README.md)
for the full explanation.

### Requirements

- **macOS** (for `say`), **ffmpeg**, **Python 3** with `pillow` and `matplotlib`

## Scene List

| # | Scene | Covers |
| --- | --- | --- |
| 1 | Thread Pool | Title card, the definition, and how this project extends §46 |
| 2 | The Scenario, Continued | Same shop, now a packing team instead of one packer |
| 3 | Naive One — A Thread Per Order, Again | The identical cost §46 measured, from the team's side |
| 4 | Naive Two — The Queue Nobody Chose | `newFixedThreadPool`'s hidden unbounded queue |
| 5 | The Pattern: Two Bounds, Not One | Workers and queue, both chosen on purpose |
| 6 | The Queue At Capacity | Forced full, and rejected with no patience window |
| 7 | Sizing Is A Real Decision | Too few workers, too many workers |
| 8 | Pool Starvation | A task waiting on a task in its own pool |
| 9 | The Same Harness, Proven Again | The lost-update proof, reused from §46 |
| 10 | What The Scheduler Really Does | The honesty rule, plus the one scenario needing no forcing |
| 11 | Java's Answer | Virtual threads, measured against act one |
| 12 | The Bill | No patience window, the nesting hazard, sizing |
| 13 | When This Is Too Much | The honest boundary |
| 14 | Thanks for Watching | The pool-starvation exercise |

Scene 14 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force thread-pool`, then
re-run `./build_video.sh`.

Same discipline as §46: every narration line names the threads involved
and speaks counts and outcomes in words, rather than pointing at a
picture the listener cannot see.

## Publishing Notes

Upload `thread-pool-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
