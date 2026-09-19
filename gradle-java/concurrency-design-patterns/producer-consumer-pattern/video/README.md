# Producer–Consumer Pattern — Teaching Video

A narrated, slide-based video that teaches Producer–Consumer using this
project's code — and introduces the determinism harness every later
project in the concurrency category reuses.

## Output Files

| File | What it is |
| --- | --- |
| `producer-consumer-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `producer-consumer-pattern-explained.m4a` | Audio-only version. |
| `producer-consumer-pattern-explained.srt` | Subtitles. |
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
| 1 | Producer-Consumer | Title card, the definition, and this category's determinism promise |
| 2 | The Scenario | Checkout and packing, and the gap between them |
| 3 | Naive One — Inline | Checkout packs itself; every customer waits |
| 4 | Naive Two — Thread Per Order | Measured thread creation cost, extrapolated to the OOM cliff |
| 5 | The Pattern: A Bound, Chosen On Purpose | Why unbounded is the same failure again |
| 6 | The Queue At Capacity | Forced with a latch, not guessed with a sleep |
| 7 | Two Shutdowns | Poison pill versus interrupt |
| 8 | Clean Shutdown | 4 of 4 packed |
| 9 | Abrupt Shutdown | 4 lost, still queued |
| 10 | Why Nothing Sleeps | The category's whole discipline |
| 11 | The Harness's Own Proof | `Rendezvous` forcing a lost update, every run |
| 12 | What The Scheduler Really Does | The honesty rule |
| 13 | The Bill | Ordering, back-pressure, no free bound |
| 14 | When This Is Too Much | The honest boundary |
| 15 | Thanks for Watching | The sleep-vs-latch exercise |

Scene 15 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force producer-consumer`, then
re-run `./build_video.sh`.

This is the hardest audio-only category in the course: an interleaving is
naturally drawn, not spoken. Every narration line names the threads
involved and says the order of events in words — "both threads read ten;
both write nine" — rather than pointing at a picture.

## Publishing Notes

Upload `producer-consumer-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
