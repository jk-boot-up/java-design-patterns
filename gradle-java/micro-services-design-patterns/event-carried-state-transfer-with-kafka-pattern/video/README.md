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

> Event-Carried State Transfer pattern in Java: the new data travels in the
> event, so each service keeps its own copy, and Kafka keeps events on topics
> so a copy can be rebuilt at any time, like a town noticeboard a new postman
> reads once. Explained with a real Kafka broker, using an online store where
> a customer service owns addresses and a shipping service prints labels. We
> replace thin events and call-backs, build a brand-new copy from the topic,
> keep order within a partition by keying on the customer, and treat deleting
> as an event. We finish with the bill.
