# Unit of Work with Spring Pattern — Teaching Video

A narrated, slide-based video that teaches @Transactional as a unit of work,
using the hand-built Unit of Work project's order over Spring Boot.

## Output Files

| File | What it is |
| --- | --- |
| `unit-of-work-with-spring-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `unit-of-work-with-spring-pattern-explained.m4a` | Audio-only version. |
| `unit-of-work-with-spring-pattern-explained.srt` | Subtitles. |
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
| 1 | Unit of Work with Spring | Title card, and the partner project |
| 2 | The Partner Project |  |
| 3 | Before The First Annotation |  |
| 4 | No Transaction |  |
| 5 | One Annotation |  |
| 6 | The Checked Exception |  |
| 7 | rollbackFor |  |
| 8 | A Flush Nobody Wrote |  |
| 9 | The Annotation That Does Nothing |  |
| 10 | Why These Surprise People |  |
| 11 | Where You Have Met This |  |
| 12 | What Was Used |  |
| 13 | What Is Real Here |  |
| 14 | When This Is Too Much |  |
| 15 | Thanks for Watching | The checked-exception exercise |

Scene 15 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force unit-of-work-with-spring`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `unit-of-work-with-spring-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
