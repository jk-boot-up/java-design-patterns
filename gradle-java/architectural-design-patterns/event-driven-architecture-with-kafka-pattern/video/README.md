# Event-Driven Architecture with Kafka Pattern — Teaching Video

A narrated, slide-based video that shows what Apache Kafka adds to the Event-Driven Architecture pattern,
and the failures that are its own.

## Output Files

| File | What it is |
| --- | --- |
| `event-driven-architecture-with-kafka-pattern-explained.mp4` | The video — 1920×1080, H.264, 30 fps, stereo AAC. |
| `event-driven-architecture-with-kafka-pattern-explained.m4a` | Audio-only version. |
| `event-driven-architecture-with-kafka-pattern-explained.srt` | Subtitles. |
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
| 1 | Event-Driven Architecture with Kafka | Title card, and the partner project |
| 2 | The Partner Project |  |
| 3 | Before The First Line |  |
| 4 | Calling And Waiting |  |
| 5 | Telling The Log |  |
| 6 | A Service That Is Down |  |
| 7 | A New Reader |  |
| 8 | Not The Same Instant |  |
| 9 | The Bill |  |
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
`python3 ../../docs/make_narration.py --force event-driven-architecture-with-kafka`, then
re-run `./build_video.sh`.

Same discipline as the rest of the category: every narration line names
the threads involved and speaks counts and outcomes in words, rather than
pointing at a picture the listener cannot see.

## Publishing Notes

Upload `event-driven-architecture-with-kafka-pattern-explained.mp4`, with
`../docs/thumbnail.png` as the thumbnail and the `.srt` as the captions.
Title, description, chapters and tags live in
[`../docs/youtube.md`](../docs/youtube.md).

Suggested description:

> Learn the Event-Driven Architecture pattern in Java with Apache Kafka,
> using a real Kafka broker behind the same online store. Services stop
> calling each other and write events to a topic instead, and the broker
> remembers how far each reader has got, like a library that keeps a
> bookmark for every reader. We lose an order the old way, send events to
> Kafka, watch a service catch up after an outage, add a new reader that
> replays history, and then price it honestly: a broker to run, and readers
> that may see the same event twice.
