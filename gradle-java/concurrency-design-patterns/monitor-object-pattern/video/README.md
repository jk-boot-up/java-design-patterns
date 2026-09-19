# Monitor Object Pattern — Teaching Video

A narrated, slide-based video that teaches Monitor Object using this
project's code, reusing Producer–Consumer's harness for its own
determinism.

## Output Files

| File | What it is |
| --- | --- |
| `monitor-object-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `monitor-object-pattern-explained.m4a` | Audio-only version. |
| `monitor-object-pattern-explained.srt` | Subtitles. |
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
| 1 | Monitor Object | Title card and the definition |
| 2 | The Scenario | One stock count, many checkout threads |
| 3 | A Plain Count — The Lost Update | Both read ten, both write nine |
| 4 | volatile — Still Not Atomic | Visibility is not atomicity |
| 5 | The Caller Holds The Lock | One forgetful caller |
| 6 | The Pattern — The Object Owns Its Lock | A private lock and a private condition |
| 7 | Waiting And Signalling | A taker waits for a delivery |
| 8 | Cost One — wait In A Loop | if versus while |
| 9 | Cost Two — Nested Monitors | Two locks, opposite orders |
| 10 | Cost Three — Calling Out | Unknown code under the lock |
| 11 | How The Demo Forces The Race | Rendezvous and wait-queue length |
| 12 | What The Scheduler Really Does | The honesty rule |
| 13 | The Bill, And When It Is Too Much | Costs gathered, and the honest boundary |
| 14 | Thanks for Watching | The fix-the-lock-order exercise |

Scene 14 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force monitor-object`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `monitor-object-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
