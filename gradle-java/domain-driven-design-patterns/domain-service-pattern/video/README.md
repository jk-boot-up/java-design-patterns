# Domain Service Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `domain-service-pattern-explained.mp4` | the video, 1920×1080 |
| `domain-service-pattern-explained.m4a` | audio only |
| `domain-service-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> When a business rule involves several domain objects and belongs to none of them, give it its own stateless class in the domain, named in the business's own words. A domain service is a stateless class, named in business language, that holds a rule involving several domain objects and belonging to none of them.
