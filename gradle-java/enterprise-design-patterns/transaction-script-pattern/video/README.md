# Transaction Script Pattern — Teaching Video

A narrated, slide-based video that teaches Transaction Script, and argues for when not to use it,
using this project's online store.

## Output Files

| File | What it is |
| --- | --- |
| `transaction-script-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `transaction-script-pattern-explained.m4a` | Audio-only version. |
| `transaction-script-pattern-explained.srt` | Subtitles. |
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
| 1 | Transaction Script | Title card and the definition |
| 2 | The Scenario | The scenario |
| 3 | One Request, One Procedure |  |
| 4 | The Pattern |  |
| 5 | One Transaction |  |
| 6 | A Second Script Copies The Rule |  |
| 7 | Share A Procedure |  |
| 8 | The Bill: Growth |  |
| 9 | Where A Script Is Right |  |
| 10 | How To Recognise It |  |
| 11 | The Verdict |  |
| 12 | What Is Real Here |  |
| 13 | When This Is Too Much |  |
| 14 | Thanks for Watching | The exercise |

Scene 14 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force transaction-script`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `transaction-script-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
