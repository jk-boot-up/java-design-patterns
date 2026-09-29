# Content-Based Router with Camel Pattern — Teaching Video

A narrated, slide-based video that teaches Content-Based Router as Apache Camel
actually does it, over a real RabbitMQ broker, and argues for when not to use it,
using this project's online store.

## Output Files

| File | What it is |
| --- | --- |
| `content-based-router-with-camel-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `content-based-router-with-camel-pattern-explained.m4a` | Audio-only version. |
| `content-based-router-with-camel-pattern-explained.srt` | Subtitles. |
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

No container runtime is needed to build the video. It is only needed to run the
demo whose output the video quotes.

## Scene List

| # | Scene | Covers |
| --- | --- | --- |
| 1 | Content-Based Router with Camel | Title card and the definition |
| 2 | The Scenario | Six orders, one place to arrive |
| 3 | One Queue For Everything | Act one |
| 4 | The Words, In Plain Language | Queue, exchange, routing key; route, predicate, otherwise |
| 5 | The Route Reads And Chooses | Act two |
| 6 | The Route, As Written | The four questions in order, and the otherwise branch |
| 7 | The First Yes Wins | Act three |
| 8 | A Message No Question Claims | Act four |
| 9 | The One Line That Keeps It | The otherwise branch in the route |
| 10 | A New Question | Act five |
| 11 | The Bill | Act six |
| 12 | What The Simulation Left Out | The contrast with the partner project |
| 13 | How To Recognise It | |
| 14 | The Verdict | |
| 15 | What Is Real, And When Not | RabbitMQ 4.3.6 and Camel 4.20.0; when this is too much |
| 16 | Thanks for Watching | The exercise |

Scene 16 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../../docs/make_narration.py --force content-based-router-with-camel`,
then re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line speaks its
counts and outcomes in words, explains each term the broker and Camel introduce
before using the tool's name for it, and never points at a picture the listener
cannot see.

## Publishing Notes

Upload `content-based-router-with-camel-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).

Suggested description:

> Learn the Content-Based Router pattern in Java with Apache Camel and a
> real RabbitMQ broker. A router reads each message and sends it to the one
> place that suits it, so the sender does not choose and receivers never see
> messages that are not theirs. In our online store, same-day parcels go to
> express shipping, gift cards go to digital delivery, and orders of a
> thousand pounds or more go to a fraud check first. We sort six orders,
> hear the order of the questions change the answer, and find that Camel
> quietly drops an order no question claims. That message is only kept if
> the route says where to keep it.
