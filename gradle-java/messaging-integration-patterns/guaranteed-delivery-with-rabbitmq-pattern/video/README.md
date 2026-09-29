# Guaranteed Delivery with RabbitMQ Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `guaranteed-delivery-with-rabbitmq-pattern-explained.mp4` | the video, 1920×1080 |
| `guaranteed-delivery-with-rabbitmq-pattern-explained.m4a` | audio only |
| `guaranteed-delivery-with-rabbitmq-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Guarantee delivery with a real RabbitMQ broker: persistent messages on a durable queue, publisher confirms so the sender knows each message is stored, and acknowledgements so a message leaves the queue only after it has been handled. With RabbitMQ, guaranteed delivery takes a durable queue, persistent messages, publisher confirms and acknowledgements after the work is done.
