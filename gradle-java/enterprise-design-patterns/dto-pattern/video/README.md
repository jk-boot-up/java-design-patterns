# DTO Pattern — Teaching Video

A narrated, slide-based video that teaches the DTO pattern using this
project's code and a tiny reflective JSON writer.

## Output Files

| File | What it is |
| --- | --- |
| `dto-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `dto-pattern-explained.m4a` | Audio-only version. |
| `dto-pattern-explained.srt` | Subtitles. |
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
| 1 | DTO | Title card and the definition |
| 2 | The Scenario | An endpoint returns a customer |
| 3 | Return The Domain Object |  |
| 4 | The Keys Are Private Names |  |
| 5 | The Pattern |  |
| 6 | A DTO Payload |  |
| 7 | A DTO Is Not A Domain Model |  |
| 8 | Cost One: Mapping Code |  |
| 9 | Cost Two: DTOs Multiply |  |
| 10 | Cost Three: The Mapping Decides What Loads |  |
| 11 | Where This Sits |  |
| 12 | Where You Have Met This |  |
| 13 | What Is Real Here |  |
| 14 | When This Is Too Much |  |
| 15 | Thanks for Watching | The phone-field exercise |

Scene 15 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force dto`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `dto-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
