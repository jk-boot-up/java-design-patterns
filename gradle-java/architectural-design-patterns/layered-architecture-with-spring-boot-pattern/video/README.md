# Layered Architecture with Spring Boot Pattern — Teaching Video

A narrated, slide-based video that shows what Spring Boot adds to the Layered Architecture pattern,
and the failures that are its own.

## Output Files

| File | What it is |
| --- | --- |
| `layered-architecture-with-spring-boot-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `layered-architecture-with-spring-boot-pattern-explained.m4a` | Audio-only version. |
| `layered-architecture-with-spring-boot-pattern-explained.srt` | Subtitles. |
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
| 1 | Layered Architecture with Spring Boot | Title card, and the partner project |
| 2 | The Partner Project |  |
| 3 | Before The First Line |  |
| 4 | Four Layers, One Real Request |  |
| 5 | One Transaction |  |
| 6 | Failures Become Statuses In One Place |  |
| 7 | The Shortcut Runs |  |
| 8 | It Also Leaks |  |
| 9 | A Rule The Container Does Not Have |  |
| 10 | The Verdict |  |
| 11 | How To Recognise It |  |
| 12 | Where You Have Met This |  |
| 13 | What Was Used |  |
| 14 | What Is Real Here |  |
| 15 | When This Is Too Much |  |
| 16 | Thanks for Watching | The exercise |

Scene 16 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force layered-architecture-with-spring-boot`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `layered-architecture-with-spring-boot-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
