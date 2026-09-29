# Content Enricher Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `content-enricher-pattern-explained.mp4` | the video, 1920×1080 |
| `content-enricher-pattern-explained.m4a` | audio only |
| `content-enricher-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> When a message is too thin for its receivers, add the missing details once, in the middle, instead of making every receiver look them up. A Content Enricher takes a message that is too thin for its receivers, looks the missing details up once, and passes on a fuller message, so no receiver has to ask.
