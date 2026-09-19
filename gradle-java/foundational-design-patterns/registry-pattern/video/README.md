# Registry Pattern — Teaching Video

A narrated, slide-based video that teaches Registry, and why it is a global variable
with better manners, using this project's checkout.

## Output Files

| File | What it is |
| --- | --- |
| `registry-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `registry-pattern-explained.m4a` | Audio-only version. |
| `registry-pattern-explained.srt` | Subtitles. |
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
| 1 | Registry | Title card and the definition |
| 2 | The Scenario | Six classes down |
| 3 | Pass It Down |  |
| 4 | The Pattern |  |
| 5 | It Works |  |
| 6 | The Bill: Invisible |  |
| 7 | The Bill: Order Dependence |  |
| 8 | The Bill: What Is In It? |  |
| 9 | Where A Registry Is Right |  |
| 10 | The Verdict |  |
| 11 | How To Recognise It |  |
| 12 | What Is Real Here |  |
| 13 | When This Is Too Much |  |
| 14 | Thanks for Watching | The both-orders exercise |

Scene 14 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force registry`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `registry-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
