# Modular Monolith Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `modular-monolith-pattern-explained.mp4` | the video, 1920×1080 |
| `modular-monolith-pattern-explained.m4a` | audio only |
| `modular-monolith-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Build one program, but split it into modules that own their data and talk only through front doors, and check those walls on every build. A modular monolith is one program split into modules that each own their data and rules and are reached only through small front doors, with the walls between them checked on every build.
