# Strangler Fig Pattern — Teaching Video

A narrated, slide-based video that teaches the Strangler Fig pattern,
and the way migrations actually fail, using a plain-Java model of the checkout.

## Output Files

| File | What it is |
| --- | --- |
| `strangler-fig-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `strangler-fig-pattern-explained.m4a` | Audio-only version. |
| `strangler-fig-pattern-explained.srt` | Subtitles. |
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
| 1 | Strangler Fig | Title card and the definition |
| 2 | The Scenario | A checkout that must keep running |
| 3 | The Big-Bang Rewrite |  |
| 4 | An Analogy: The Strangler Fig |  |
| 5 | A Router, And A Switch Per Capability |  |
| 6 | Shadow Reads |  |
| 7 | One Capability Rolls Back |  |
| 8 | The Bill: Two Systems |  |
| 9 | The Bill: Two Truths |  |
| 10 | The Failure That Actually Happens |  |
| 11 | The Verdict |  |
| 12 | How To Recognise It |  |
| 13 | What This Model Does Not Show |  |
| 14 | Where You Have Met This |  |
| 15 | When This Is Too Much |  |
| 16 | Thanks for Watching | The cost-model exercise |

Scene 16 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force strangler-fig`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `strangler-fig-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
