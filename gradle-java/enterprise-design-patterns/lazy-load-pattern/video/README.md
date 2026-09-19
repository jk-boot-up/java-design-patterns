# Lazy Load Pattern — Teaching Video

A narrated, slide-based video that teaches Lazy Load using this
project's code and its in-memory toy database.

## Output Files

| File | What it is |
| --- | --- |
| `lazy-load-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `lazy-load-pattern-explained.m4a` | Audio-only version. |
| `lazy-load-pattern-explained.srt` | Subtitles. |
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
| 1 | Lazy Load | Title card and the definition |
| 2 | The Scenario | One order, a connected graph |
| 3 | Eager Loading |  |
| 4 | The Pattern |  |
| 5 | Four Ways To Load Later |  |
| 6 | Cost One: N Plus One |  |
| 7 | Cost Two: A Field Is Now I/O |  |
| 8 | Cost Three: The Closed Session |  |
| 9 | Where You Have Met This |  |
| 10 | The Toy Database |  |
| 11 | What Is Real Here |  |
| 12 | When This Is Too Much |  |
| 13 | What To Do About It |  |
| 14 | Thanks for Watching | The fetch-once exercise |

Scene 14 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force lazy-load`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `lazy-load-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
