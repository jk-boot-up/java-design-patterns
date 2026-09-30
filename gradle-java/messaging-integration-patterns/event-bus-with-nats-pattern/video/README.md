# Event Bus with NATS Pattern — Teaching Video

A narrated, slide-based video that shows what changes when the Event Bus becomes a real
NATS server in a container, and the failure that is its own: an event nobody hears,
using this project's online store.

## Output Files

| File | What it is |
| --- | --- |
| `event-bus-with-nats-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `event-bus-with-nats-pattern-explained.m4a` | Audio-only version. |
| `event-bus-with-nats-pattern-explained.srt` | Subtitles. |
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
| 1 | Event Bus with NATS | Title card, the definition, the tannoy analogy |
| 2 | The Partner Project | The hand-built Event Bus this pairs with |
| 3 | Before The First Line | What NATS is, subjects, the container runtime |
| 4 | Everyone Knows Everyone | Act one |
| 5 | Everyone Knows The Bus | Act two |
| 6 | Subscribing By Name | Act three: exact names, star and arrow |
| 7 | One Failing Subscriber | Act four |
| 8 | An Event Nobody Hears | Act five |
| 9 | Ask, Do Not Tell | A request with no responders |
| 10 | The Bill | Act six |
| 11 | The Opposite Trade | The durable log, and its price |
| 12 | The Verdict | |
| 13 | How To Recognise It | |
| 14 | What Was Used | NATS 2.15.0, jnats 2.26.3, Testcontainers 2.0.5 |
| 15 | What Is Real Here | A real server, no test sleeps |
| 16 | Thanks for Watching | The exercise |

Scene 16 deliberately does not name whichever pattern comes next.

## Editing the Script

Narration lives in `scenes.py`. Edit it, re-run
`python3 ../../docs/make_narration.py --force event-bus-with-nats`,
then re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line speaks its
counts and outcomes in words, explains each term NATS introduces before using
the tool's name for it, and never points at a picture the listener cannot see.

## Publishing Notes

Upload `event-bus-with-nats-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).

Suggested description:

> Event Bus pattern in Java: an event bus is one shared line where senders
> announce events and each listener hears the ones it cares about, without
> sender and listener knowing each other. Explained with NATS, a real
> messaging server on the network that keeps nothing. Checkout announces that
> an order was placed, and the email service, the warehouse and analytics each
> listen for what they care about, like a warehouse loudspeaker: whoever is in
> the room hears it, and someone who walks in a second later hears nothing. We
> subscribe by name, survive a failing subscriber, hear an event nobody hears,
> and use ask instead of tell when an answer matters. We finish with the bill
> and the opposite trade. On this bus, publishing always succeeds, and
> succeeding means nothing.
