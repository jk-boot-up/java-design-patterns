# Event-Carried State Transfer with Kafka Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `event-carried-state-transfer-with-kafka-pattern-explained.mp4` | the video, 1920×1080 |
| `event-carried-state-transfer-with-kafka-pattern-explained.m4a` | audio only |
| `event-carried-state-transfer-with-kafka-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Carry each customer's address in events on a real Kafka topic, keyed by customer and compacted, so shipping can build its own copy from the topic, keep each customer's updates in order, and learn of deletions through tombstones. With Kafka, state events keyed by entity on a compacted topic let any service build and keep its own copy, in order, with deletions as tombstones.
