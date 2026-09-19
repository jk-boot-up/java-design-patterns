# Data Mapper Pattern — Teaching Video

A narrated, slide-based video that teaches Data Mapper using this
project's code and its in-memory toy database.

## Output Files

| File | What it is |
| --- | --- |
| `data-mapper-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `data-mapper-pattern-explained.m4a` | Audio-only version. |
| `data-mapper-pattern-explained.srt` | Subtitles. |
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
| 1 | Data Mapper | Title card and the definition |
| 2 | The Scenario | A customer, and storing it |
| 3 | Active Record Works | Three operations, one class |
| 4 | The Cost | The object needs the database |
| 5 | A Shape It Cannot Say | Two tables; one table, two objects |
| 6 | The Pattern | A mapper between object and rows |
| 7 | What The Customer Looks Like | Fields and behaviour only |
| 8 | The Bill: A Class Per Entity | Every entity gets a mapper |
| 9 | The Bill: A Silent Field | The postcode that never came back |
| 10 | The Toy Database | Rows, a counter, failure on demand |
| 11 | Where You Have Met This | JPA and the EntityManager |
| 12 | What Is Real Here | The honesty rule |
| 13 | When This Is Too Much | When Active Record is right |
| 14 | Thanks for Watching | The round-trip test exercise |

Scene 14 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force data-mapper`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `data-mapper-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
