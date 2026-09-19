# Object Pool Pattern — Teaching Video

A narrated, slide-based video that teaches Object Pool, and when it makes things slower,
using this project's payment gateway connection.

## Output Files

| File | What it is |
| --- | --- |
| `object-pool-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `object-pool-pattern-explained.m4a` | Audio-only version. |
| `object-pool-pattern-explained.srt` | Subtitles. |
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
| 1 | Object Pool | Title card and the definition |
| 2 | The Scenario | A slow handshake |
| 3 | A Connection Per Payment |  |
| 4 | The Pattern: A Pool |  |
| 5 | Now, The Bill |  |
| 6 | Cost One: It Is Slower |  |
| 7 | How This Was Measured |  |
| 8 | Cost Two: A Dirty Return |  |
| 9 | Cost Three: A Leak |  |
| 10 | Cost Four: Sizing Is A Guess |  |
| 11 | The Verdict |  |
| 12 | How To Recognise It |  |
| 13 | What Is Real Here |  |
| 14 | When This Is Too Much |  |
| 15 | Thanks for Watching | The big-receipt exercise |

Scene 15 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force object-pool`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `object-pool-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
