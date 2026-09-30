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

> Request-Reply pattern in Java: a question travels in one message and the
> answer in another; each request says where to reply and carries a reference
> so the answer can be matched, like letters to a supplier with your address
> and a reference number. Explained with a real RabbitMQ broker, using an
> online store checkout that asks an inventory service to reserve items. We
> watch replies taken in arrival order go wrong, add correlation IDs and
> reply-to addresses, keep many requests in flight, and handle a reply that
> never comes. Say where to answer, say which question, and say when to give
> up.
