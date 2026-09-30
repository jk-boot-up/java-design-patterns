# Message Translator with Apache Camel Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `message-translator-with-camel-pattern-explained.mp4` | the video, 1920×1080 |
| `message-translator-with-camel-pattern-explained.m4a` | audio only |
| `message-translator-with-camel-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Message Translator pattern in Java: a translator turns a message from one
> format into another, so the receiver only ever sees the one shape it
> understands, like an international post room that routes each letter to the
> right translator. Explained with Apache Camel, using an online store
> warehouse that takes orders from its web form and from marketplaces. We
> watch Camel refuse a foreign format sent straight to the warehouse, give
> each format its own translator route, add a normalizer that picks the route,
> and support a new format with a new route. We finish with the bill.
