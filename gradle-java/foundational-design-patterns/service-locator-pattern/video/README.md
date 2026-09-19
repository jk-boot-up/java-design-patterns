# Service Locator Pattern — Teaching Video

A narrated, slide-based video that teaches Service Locator, argues fairly against it,
and shows where it is still right, using this project's checkout.

## Output Files

| File | What it is |
| --- | --- |
| `service-locator-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `service-locator-pattern-explained.m4a` | Audio-only version. |
| `service-locator-pattern-explained.srt` | Subtitles. |
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
| 1 | Service Locator | Title card and the definition |
| 2 | The Scenario | The registry's problems |
| 3 | The Advance: Recipes |  |
| 4 | The Other Advance: Swap For A Test |  |
| 5 | The Bill: The Compiler Says Nothing |  |
| 6 | The Bill: Every Class Depends On It |  |
| 7 | Where It Is Still Right |  |
| 8 | The Verdict |  |
| 9 | The Word Is Ask |  |
| 10 | How To Recognise It |  |
| 11 | What Is Real Here |  |
| 12 | When This Is Too Much |  |
| 13 | Thanks for Watching | The third-plug-in exercise |

Scene 13 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force service-locator`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `service-locator-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
