# Read-Write Lock Pattern — Teaching Video

A narrated, slide-based video that teaches Read-Write Lock using this
project's code, reusing Producer–Consumer's harness for its own
determinism.

## Output Files

| File | What it is |
| --- | --- |
| `read-write-lock-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `read-write-lock-pattern-explained.m4a` | Audio-only version. |
| `read-write-lock-pattern-explained.srt` | Subtitles. |
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
| 1 | Read-Write Lock | Title card, the definition, and this project's place in the category |
| 2 | The Scenario | A price read by a thousand shoppers, changed now and then |
| 3 | No Lock — The Torn Read | The new amount with the old currency |
| 4 | One Lock — Correct, But Queued | 15ms, every reader behind every reader |
| 5 | The Pattern — Two Locks In One | Shared read lock, exclusive write lock |
| 6 | The Surprise | 138ms: slower, not faster |
| 7 | Cost One — Writer Starvation | A queued writer overtaken by a later reader |
| 8 | Cost Two — The Upgrade Deadlock | A thread waiting on itself |
| 9 | Cost Three — When The Lock Loses | Mutex 16ms, lock 137ms, snapshot 2ms |
| 10 | How The Demo Forces The Torn Read | Latch and gate, no sleeping |
| 11 | What The Scheduler Really Does | The honesty rule |
| 12 | The Bill | All three costs, gathered in one place |
| 13 | When To Use It, And When Not | The honest boundary |
| 14 | Thanks for Watching | The make-the-read-slower exercise |

Scene 14 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force read-write-lock`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `read-write-lock-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
