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

> Translate each incoming format into one canonical message at the edge, with one small translator per format and a normalizer that picks the right one, so the rest of the system speaks only one language. A message translator converts one format into another; a normalizer recognises each incoming format and picks the translator, so everything arrives in one canonical shape.
