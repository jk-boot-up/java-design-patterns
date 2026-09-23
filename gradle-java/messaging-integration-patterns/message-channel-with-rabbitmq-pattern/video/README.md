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
| 9 | Written To Disk, Or Not | Act five: the restart |
| 10 | Two Settings, Not One | Durable queue, persistent message |
| 11 | The Bill | Act six: the limit, receipts, and the cost |
| 12 | What The Simulation Left Out | The contrast with the partner project |
| 13 | The Verdict | |
| 14 | What Is Real Here | RabbitMQ 4.3.6 in a container the demo owns |
| 15 | When This Is Too Much | |
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
