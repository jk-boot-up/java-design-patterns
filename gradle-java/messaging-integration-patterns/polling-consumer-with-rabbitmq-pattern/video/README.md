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

> Polling Consumer pattern in Java with a real RabbitMQ broker, using an
> online store warehouse label printer. A polling consumer asks for the next
> message when it is ready instead of having messages pushed at it as fast
> as they arrive, and RabbitMQ offers push, pull, and a middle way, like a
> kitchen that asks for the next ticket or keeps a few on the rail. We watch
> unlimited push overwhelm the printer, protect it by polling, learn that
> pausing is not polling, and see what polling costs when nothing is
> happening. We finish with RabbitMQ's middle way: prefetch.
