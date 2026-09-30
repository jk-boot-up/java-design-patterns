# Splitter and Aggregator with Camel Pattern — Teaching Video

A narrated, slide-based video that teaches Splitter and Aggregator as Apache Camel
actually does it, and argues for when not to use it, using this project's online store.

## Output Files

| File | What it is |
| --- | --- |
| `splitter-aggregator-with-camel-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `splitter-aggregator-with-camel-pattern-explained.m4a` | Audio-only version. |
| `splitter-aggregator-with-camel-pattern-explained.srt` | Subtitles. |
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
| 1 | Splitter and Aggregator with Camel | Title card and the definition |
| 2 | The Scenario | One basket, three warehouses |
| 3 | One Picker, One Order | Act one |
| 4 | Camel's Three Words | Route, correlation, completion condition |
| 5 | Camel Splits The Order | Act two |
| 6 | They Come Back In Any Order | Act three |
| 7 | The Completion Condition | Act four |
| 8 | A Deadline | Act five |
| 9 | The Whole Difference | The two lines that separate the aggregators |
| 10 | The Bill | Act six |
| 11 | What The Simulation Left Out | The contrast with the partner project |
| 12 | How To Recognise It | |
| 13 | The Verdict | |
| 14 | What Is Real Here | Camel 4.20.0, no container, offline |
| 15 | When This Is Too Much | |
| 16 | Thanks for Watching | The exercise |

Scene 16 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force splitter-aggregator-with-camel`,
then re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line speaks its
counts and outcomes in words, explains each term Camel introduces before using
the framework's name for it, and never points at a picture the listener cannot
see.

## Publishing Notes

Upload `splitter-aggregator-with-camel-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).

Suggested description:

> Splitter and Aggregator pattern in Java: a splitter breaks one message into
> pieces that are handled separately, and an aggregator gathers the answers
> back into one when a completion rule says they are ready. Explained with
> Apache Camel, using an online store basket with three items in warehouses in
> Leeds, Reading and Glasgow, where each warehouse prices its own line. We
> hear an aggregator wait forever because nobody gave it a deadline, a real
> deadline end that wait, and the moment Camel declares an order finished when
> it is not. An aggregator with only a count will wait forever, so the
> deadline is the other half of the pattern.
