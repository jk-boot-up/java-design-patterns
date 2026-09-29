# Plugin Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `plugin-pattern-explained.mp4` | the video, 1920×1080 |
| `plugin-pattern-explained.m4a` | audio only |
| `plugin-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Let the code name only interfaces, and let one configuration file per environment say which class plays each part. Plugin lets the code ask only for interfaces while a configuration file per environment names the class for each one, and a single factory creates them.
