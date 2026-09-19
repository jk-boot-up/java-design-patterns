# Repository with Spring Data Pattern — Teaching Video

A narrated, slide-based video that teaches Spring Data's repository interface,
using the hand-built Repository project's customers and question over Spring Boot.

## Output Files

| File | What it is |
| --- | --- |
| `repository-with-spring-data-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `repository-with-spring-data-pattern-explained.m4a` | Audio-only version. |
| `repository-with-spring-data-pattern-explained.srt` | Subtitles. |
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
| 1 | Repository with Spring Data | Title card, and the partner project |
| 2 | The Partner Project |  |
| 3 | Before The First Annotation |  |
| 4 | An Interface With No Implementation |  |
| 5 | A Query From A Name |  |
| 6 | Cost: A Name Can Be Wrong |  |
| 7 | Cost: The Leak On Speed |  |
| 8 | The Managed Entity That Leaks |  |
| 9 | And The Swap? |  |
| 10 | Where You Have Met This |  |
| 11 | What Was Used |  |
| 12 | What Is Real Here |  |
| 13 | When This Is Too Much |  |
| 14 | Thanks for Watching | The name-prefix finder exercise |

Scene 14 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force repository-with-spring-data`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `repository-with-spring-data-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
