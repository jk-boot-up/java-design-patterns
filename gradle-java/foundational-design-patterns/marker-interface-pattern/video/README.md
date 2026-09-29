# Marker Interface Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `marker-interface-pattern-explained.mp4` | the video, 1920×1080 |
| `marker-interface-pattern-explained.m4a` | audio only |
| `marker-interface-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Mark a type with an empty interface, so code and the compiler can tell what kind of thing it is, instead of trusting free-text tags. A marker interface is an empty interface whose name tells code and the compiler something about a type, replacing free-text tags that can be misspelt.
