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

> Guaranteed Delivery pattern in Java: a message, once accepted, must never be
> lost, not when the program crashes and not when the broker restarts, and
> RabbitMQ can give that guarantee if you ask correctly, like recorded
> delivery with a receipt at each end. Explained with a real RabbitMQ broker,
> using an online store's order confirmation emails. We watch a durable queue
> lose transient messages, make them persistent and confirmed, acknowledge
> only after sending, and crash before the acknowledgement to see a message
> delivered twice. Store it, confirm it, and acknowledge it only when the work
> is done.
