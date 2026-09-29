# Polling Consumer with RabbitMQ Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `polling-consumer-with-rabbitmq-pattern-explained.mp4` | the video, 1920×1080 |
| `polling-consumer-with-rabbitmq-pattern-explained.m4a` | audio only |
| `polling-consumer-with-rabbitmq-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Let the label printer take orders from a real RabbitMQ queue only when it is ready, by polling with basicGet, and compare it with RabbitMQ's own answer: push with a prefetch limit. With RabbitMQ, a polling consumer asks for messages with `basicGet` when it is ready; push with a prefetch limit gives the same protection with less waste.
