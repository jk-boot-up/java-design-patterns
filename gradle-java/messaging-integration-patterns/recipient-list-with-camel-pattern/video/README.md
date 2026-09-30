# Recipient List with Apache Camel Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `recipient-list-with-camel-pattern-explained.mp4` | the video, 1920×1080 |
| `recipient-list-with-camel-pattern-explained.m4a` | audio only |
| `recipient-list-with-camel-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Recipient List pattern in Java: for each message the list works out who
> should get it and sends a copy to each of them and to nobody else, like a
> clerk writing the names on a letter before the post room copies it.
> Explained with Apache Camel, whose recipient list step is built in, using an
> online store sending orders to its warehouses. We watch every order go to
> every warehouse, send each order only where it is needed, let rules add
> recipients, change the table while running, and see what happens when one
> recipient fails.
