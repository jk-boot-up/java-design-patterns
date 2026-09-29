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

> Let same-day orders overtake standard ones on a real RabbitMQ priority queue, and see its two limits: priority only reorders messages still waiting on the queue, and it keeps no share for routine work. With RabbitMQ, a queue declared with `x-max-priority` hands out higher-priority messages first, but only among those still waiting on the queue.
