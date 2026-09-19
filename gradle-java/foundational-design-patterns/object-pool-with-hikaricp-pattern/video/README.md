# Object Pool with HikariCP Pattern — Teaching Video

A narrated, slide-based video that shows HikariCP as the mature answer to the hand-built Object Pool's costs,
and what it still cannot fix.

## Output Files

| File | What it is |
| --- | --- |
| `object-pool-with-hikaricp-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `object-pool-with-hikaricp-pattern-explained.m4a` | Audio-only version. |
| `object-pool-with-hikaricp-pattern-explained.srt` | Subtitles. |
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
| 1 | Object Pool with HikariCP | Title card, and the partner project |
| 2 | The Partner Project |  |
| 3 | Before The First Line |  |
| 4 | It Opens What Demand Needs |  |
| 5 | The Dirty Return |  |
| 6 | What It Cannot Reset |  |
| 7 | Exhaustion, With A Timeout |  |
| 8 | Sizing Is Still A Guess |  |
| 9 | What Pooling Buys |  |
| 10 | The Verdict |  |
| 11 | Where You Have Met This |  |
| 12 | What Was Used |  |
| 13 | What Is Real Here |  |
| 14 | Thanks for Watching | The leak-detection exercise |

Scene 14 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force object-pool-with-hikaricp`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `object-pool-with-hikaricp-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
