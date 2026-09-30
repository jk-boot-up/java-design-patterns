# Priority Queue with RabbitMQ Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `priority-queue-with-rabbitmq-pattern-explained.mp4` | the video, 1920×1080 |
| `priority-queue-with-rabbitmq-pattern-explained.m4a` | audio only |
| `priority-queue-with-rabbitmq-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Priority Queue pattern in Java: urgent messages overtake routine ones, and
> RabbitMQ can make a queue a priority queue, but nobody can overtake someone
> already in the scanner, as at airport fast-track. Explained with a real
> RabbitMQ broker, using an online store warehouse where same-day orders must
> catch the courier's van. We watch first in, first out miss the van, put
> same-day orders first, survive a flood, and see why prefetch means priority
> only applies to what is still waiting. We finish with the bill: starvation
> of routine orders.
