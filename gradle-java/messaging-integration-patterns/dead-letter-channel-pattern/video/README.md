# Dead Letter Channel Pattern — Teaching Video

A narrated, slide-based video that teaches Dead Letter Channel, and argues for when not to use it,
using this project's online store.

## Output Files

| File | What it is |
| --- | --- |
| `dead-letter-channel-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `dead-letter-channel-pattern-explained.m4a` | Audio-only version. |
| `dead-letter-channel-pattern-explained.srt` | Subtitles. |
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
| 1 | Dead Letter Channel | Title card and the definition |
| 2 | The Scenario | The scenario |
| 3 | A Message That Can Never Succeed |  |
| 4 | The Pattern |  |
| 5 | A Dead Letter Channel |  |
| 6 | It Says Why |  |
| 7 | A Slow Day Is Not A Dead Letter |  |
| 8 | Fix It, And Replay |  |
| 9 | The Bill: Nobody Is Looking |  |
| 10 | How To Recognise It |  |
| 11 | The Verdict |  |
| 12 | What Is Real Here |  |
| 13 | When This Is Too Much |  |
| 14 | Thanks for Watching | The exercise |

Scene 14 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force dead-letter-channel`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `dead-letter-channel-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).

Suggested description:

> Dead Letter Channel pattern in Java, explained with an online store order
> that arrives garbled and can never be read. A dead letter channel is where
> a message goes after a fixed number of failed tries, so it stops blocking
> the messages behind it and someone can look at it later, like the post
> office's undeliverable mail room. We watch one bad message block
> everything, then move it aside after three tries with its reason. We tell
> a slow moment apart from a dead letter, replay a message after a fix, and
> face the real cost: nobody is looking.
