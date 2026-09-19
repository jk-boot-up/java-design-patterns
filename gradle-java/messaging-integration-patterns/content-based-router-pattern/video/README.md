# Content-Based Router Pattern — Teaching Video

A narrated, slide-based video that teaches Content-Based Router, and argues for when not to use it,
using this project's online store.

## Output Files

| File | What it is |
| --- | --- |
| `content-based-router-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `content-based-router-pattern-explained.m4a` | Audio-only version. |
| `content-based-router-pattern-explained.srt` | Subtitles. |
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
| 1 | Content-Based Router | Title card and the definition |
| 2 | The Scenario | The scenario |
| 3 | One Channel For Everything |  |
| 4 | The Pattern |  |
| 5 | A Router Looks Inside |  |
| 6 | The First Rule That Matches Wins |  |
| 7 | Nothing Matches |  |
| 8 | A New Route, And Nobody Else Changes |  |
| 9 | The Bill |  |
| 10 | How To Recognise It |  |
| 11 | The Verdict |  |
| 12 | What Is Real Here |  |
| 13 | When This Is Too Much |  |
| 14 | Thanks for Watching | The exercise |

Scene 14 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force content-based-router`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `content-based-router-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
