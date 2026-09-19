# Circuit Breaker with Resilience4j Pattern — Teaching Video

A narrated, slide-based video that shows what Resilience4j adds to the Circuit Breaker pattern,
and the failures that are its own.

## Output Files

| File | What it is |
| --- | --- |
| `circuit-breaker-with-resilience4j-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `circuit-breaker-with-resilience4j-pattern-explained.m4a` | Audio-only version. |
| `circuit-breaker-with-resilience4j-pattern-explained.srt` | Subtitles. |
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
| 1 | Circuit Breaker with Resilience4j | Title card, and the partner project |
| 2 | The Partner Project |  |
| 3 | Before The First Line |  |
| 4 | Healthy |  |
| 5 | The Service Goes Down |  |
| 6 | Open: Fail Fast |  |
| 7 | Half-Open: One Probe |  |
| 8 | What Counts As A Failure |  |
| 9 | The Annotation Is A Proxy |  |
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
`python3 ../../docs/make_narration.py --force circuit-breaker-with-resilience4j`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `circuit-breaker-with-resilience4j-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).
