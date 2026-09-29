# Request-Reply with RabbitMQ Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `request-reply-with-rabbitmq-pattern-explained.mp4` | the video, 1920×1080 |
| `request-reply-with-rabbitmq-pattern-explained.m4a` | audio only |
| `request-reply-with-rabbitmq-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Ask and answer over a real RabbitMQ broker: each request carries a return address and a correlation ID, the inventory service replies to that address with that ID, and an expiry on the request makes sure an abandoned request is never handled late. With RabbitMQ, request-reply uses the `replyTo` and `correlationId` properties, and an expiry so a request nobody waits for is dropped.
