# Dependency Injection with Spring Pattern — Teaching Video

A narrated, slide-based video that shows what Spring's container replaces,
using the hand-built Dependency Injection project's classes.

## Output Files

| File | What it is |
| --- | --- |
| `dependency-injection-with-spring-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `dependency-injection-with-spring-pattern-explained.m4a` | Audio-only version. |
| `dependency-injection-with-spring-pattern-explained.srt` | Subtitles. |
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
| 1 | Dependency Injection with Spring | Title card, and the partner project |
| 2 | The Partner Project |  |
| 3 | Before The First Annotation |  |
| 4 | One Annotation Per Class |  |
| 5 | The Same Graph |  |
| 6 | What Each Annotation Replaced |  |
| 7 | A Missing Bean |  |
| 8 | A Circular Dependency |  |
| 9 | Field Injection |  |
| 10 | What The Magic Costs |  |
| 11 | The Verdict |  |
| 12 | Where You Have Met This |  |
| 13 | What Was Used |  |
| 14 | What Is Real Here |  |
| 15 | Thanks for Watching | The delete-an-annotation exercise |

Scene 15 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force dependency-injection-with-spring`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `dependency-injection-with-spring-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
