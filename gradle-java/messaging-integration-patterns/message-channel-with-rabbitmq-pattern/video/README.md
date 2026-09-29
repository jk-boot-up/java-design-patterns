# Message Channel with RabbitMQ Pattern — Teaching Video

A narrated, slide-based video that teaches Message Channel on a real RabbitMQ
broker — what it keeps while nobody is listening, when it forgets a message,
and what survives its own restart — and argues for when not to use it, using
this project's online store.

## Output Files

| File | What it is |
| --- | --- |
| `message-channel-with-rabbitmq-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `message-channel-with-rabbitmq-pattern-explained.m4a` | Audio-only version. |
| `message-channel-with-rabbitmq-pattern-explained.srt` | Subtitles. |
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

The video itself needs no container runtime; only the demo does.

## Scene List

| # | Scene | Covers |
| --- | --- | --- |
| 1 | Message Channel with RabbitMQ | Title card and the definition |
| 2 | The Scenario | A shop and a warehouse, not always up together |
| 3 | Checkout Calls The Warehouse | Act one |
| 4 | The Broker's Words | Broker, queue, exchange, through a post office |
| 5 | A Real Channel Between Them | Act two |
| 6 | Nobody Is Listening Yet | Act three |
| 7 | Where The Message Lives | Three programs, and the rule that holds them together |
| 8 | Saying Done | Act four: acknowledgement, and a second delivery |
| 9 | Two Pickers, One Queue | Act four, continued: a slow and a fast picker, with and without a limit on unfinished orders (prefetch) |
| 10 | Written To Disk, Or Not | Act five: the restart |
| 11 | Two Settings, Not One | Durable queue, persistent message |
| 12 | The Bill | Act six: the limit, receipts, and the cost |
| 13 | What The Simulation Left Out | The contrast with the partner project |
| 14 | The Verdict | |
| 15 | What Is Real, And When Not | RabbitMQ 4.3.6 in a container the demo owns, and when a broker is too much |
| 16 | Thanks for Watching | The exercise |

Scene 16 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force message-channel-with-rabbitmq`,
then re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line speaks its
counts and outcomes in words, explains each term RabbitMQ introduces before
using the broker's name for it, and never points at a picture the listener
cannot see.

## Publishing Notes

Upload `message-channel-with-rabbitmq-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).

Suggested description:

> Message Channel pattern in Java, explained with a real RabbitMQ broker. In
> our online store the shop drops a pick order into a channel and goes
> straight back to selling, and the warehouse takes it out whenever it is
> ready. We hear the broker hold orders for a warehouse that is not even
> running, hand an order out again when a picker crashes before saying done,
> share orders between a slow picker and a fast one, and survive its own
> restart with some orders kept and others gone. A broker only forgets an
> order when the receiver says it is done, and only keeps it through a
> restart if both queue and message were saved.
