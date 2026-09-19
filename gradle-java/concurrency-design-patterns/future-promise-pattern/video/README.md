# Future/Promise Pattern — Teaching Video

A narrated, slide-based video that teaches Future/Promise using this
project's code, reusing Producer–Consumer's harness for its own
determinism.

## Output Files

| File | What it is |
| --- | --- |
| `future-promise-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `future-promise-pattern-explained.m4a` | Audio-only version. |
| `future-promise-pattern-explained.srt` | Subtitles. |
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
| 1 | Future/Promise | Title card, the definition, and how this project extends §46/§47 |
| 2 | The Scenario | Three independent lookups, each measured at 200ms |
| 3 | Naive — Sequential Lookups | 619ms, paid one after another for no reason |
| 4 | The Pattern — Concurrent Lookups | 208ms, all three submitted at once |
| 5 | The Two Halves Beginners Conflate | Future is the reader's half; Promise is the writer's |
| 6 | Future And Promise, Made Explicit | The handoff, on two separate threads |
| 7 | Exceptions Move | A stack trace that omits the calling thread entirely |
| 8 | get() With No Timeout Is A Hang | The rescue timeout, and why it is not optional |
| 9 | Cancellation Is Cooperative | cancel(true) asks; a task is free to ignore it |
| 10 | One More Cost: Chained Callbacks | Why `thenApply`/`thenCompose` depth turns unreadable |
| 11 | The Same Harness, Proven Again | The lost-update proof, reused from §46 |
| 12 | What The Scheduler Really Does | The honesty rule |
| 13 | The Bill | All three costs, gathered in one place |
| 14 | When This Is Too Much | The honest boundary |
| 15 | Thanks for Watching | The remove-the-timeout exercise |

Scene 15 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force future-promise`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `future-promise-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
