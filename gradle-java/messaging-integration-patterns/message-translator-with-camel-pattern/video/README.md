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

> Build the message translator with Apache Camel: one route per incoming format, Camel's own data formats to read CSV, JSON and XML, and a normalizer route that recognises the format and hands over to the right translator. With Camel, each translator is a route, each format is read by a data format, and a normalizer route sends each message to the right translator by name.
