# Message Translator / Normalizer Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `message-translator-pattern-explained.mp4` | the video, 1920×1080 |
| `message-translator-pattern-explained.m4a` | audio only |
| `message-translator-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Message Translator and Normalizer patterns in Java: a translator turns one
> format into the format your system uses, and a normalizer recognises each
> incoming format and picks the right translator, like one interpreter per
> language at an international meeting. Explained with an online store
> warehouse that takes orders from its own web form and from marketplaces that
> each send their own format. We watch the warehouse try to read every format
> itself, add translators and a normalizer, and welcome a new marketplace with
> one more translator. Translate at the edge, so the inside speaks one
> language.
