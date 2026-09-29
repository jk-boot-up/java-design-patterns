# Domain Event Pattern — Teaching Video

A narrated, slide-based video that teaches Domain Event, and argues for when not to use it,
using this project's online store.

## Output Files

| File | What it is |
| --- | --- |
| `domain-event-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `domain-event-pattern-explained.m4a` | Audio-only version. |
| `domain-event-pattern-explained.srt` | Subtitles. |
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
| 1 | Domain Event | Title card and the definition |
| 2 | The Scenario | The scenario |
| 3 | The Order Calls Everyone |  |
| 4 | The Pattern |  |
| 5 | The Order Says What Happened |  |
| 6 | Delivered After The Save |  |
| 7 | A Failing Reaction |  |
| 8 | Events Are Facts |  |
| 9 | The Gap Between Saving And Telling |  |
| 10 | How To Recognise It |  |
| 11 | The Verdict |  |
| 12 | What Is Real Here |  |
| 13 | When This Is Too Much |  |
| 14 | Thanks for Watching | The exercise |

Scene 14 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force domain-event`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `domain-event-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).

Suggested description:

> Learn the Domain Event pattern in Java with an online store order being
> placed. A domain event is a record of something that has already happened,
> named in the past tense and never changed, and others react to it without
> the sender knowing who they are, like a birth announcement in a newspaper.
> We watch an order that calls three services fall into a half-done state,
> then let it simply say what happened, delivered after the save. We hear a
> failing reaction retried safely, and the real cost: the gap between saving
> and telling, which must be kept closed.
