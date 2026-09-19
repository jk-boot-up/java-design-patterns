# Repository Pattern — Teaching Video

A narrated, slide-based video that teaches Repository using this
project's code and its in-memory toy database.

## Output Files

| File | What it is |
| --- | --- |
| `repository-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `repository-pattern-explained.m4a` | Audio-only version. |
| `repository-pattern-explained.srt` | Subtitles. |
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
| 1 | Repository | Title card and the definition |
| 2 | The Scenario | One question, three askers |
| 3 | SQL In The Service |  |
| 4 | A Schema Change |  |
| 5 | The Pattern |  |
| 6 | The Caller Knows Only The Interface |  |
| 7 | Swap The Store |  |
| 8 | Cost One: A Method Per Question |  |
| 9 | Cost Two: The Leak |  |
| 10 | Cost Three: The Swap Is Rarely Used |  |
| 11 | The Toy Database |  |
| 12 | Where You Have Met This |  |
| 13 | What Is Real Here |  |
| 14 | When This Is Too Much |  |
| 15 | Thanks for Watching | The specification exercise |

Scene 15 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force repository`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `repository-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
