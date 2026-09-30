# Aggregate Pattern — Teaching Video

A narrated, slide-based video that teaches Aggregate, and argues for when not to use it,
using this project's online store.

## Output Files

| File | What it is |
| --- | --- |
| `aggregate-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `aggregate-pattern-explained.m4a` | Audio-only version. |
| `aggregate-pattern-explained.srt` | Subtitles. |
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
| 1 | Aggregate | Title card and the definition |
| 2 | The Scenario | The scenario |
| 3 | A Loose Order |  |
| 4 | The Pattern |  |
| 5 | The Root Guards The Rules |  |
| 6 | There Is Only One Door |  |
| 7 | Other Aggregates By Id |  |
| 8 | Saved Whole, Or Not At All |  |
| 9 | An Aggregate Drawn Too Big |  |
| 10 | How To Recognise It |  |
| 11 | The Verdict |  |
| 12 | What Is Real Here |  |
| 13 | When This Is Too Much |  |
| 14 | Thanks for Watching | The exercise |

Scene 14 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force aggregate`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `aggregate-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).

Suggested description:

> Aggregate pattern from domain-driven design in Java: an aggregate is a small
> group of objects treated as one unit, with a single root object as the only
> way in, so the group's rules cannot be broken from outside, like a bank
> teller who guards the vault. Explained with an online store order and its
> lines. We watch an order break all its own rules when anyone can reach
> inside, then let one root guard them. We hear why an aggregate refers to
> others only by ID, how it is saved whole or not at all, and what goes wrong
> when one is drawn too big. An aggregate is where a rule lives, and where a
> save begins and ends.
