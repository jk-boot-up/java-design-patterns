# Service Stub Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `service-stub-pattern-explained.mp4` | the video, 1920×1080 |
| `service-stub-pattern-explained.m4a` | audio only |
| `service-stub-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Put an external service behind a gateway interface, and during development and testing plug in a small, free, in-memory stub that behaves like it, checked regularly against the real thing. A service stub is a small in-memory stand-in for an external service, behind the same gateway interface, used in development and tests and checked against the real service regularly.
