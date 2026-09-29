# Context Map and Shared Kernel Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `context-map-pattern-explained.mp4` | the video, 1920×1080 |
| `context-map-pattern-explained.m4a` | audio only |
| `context-map-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Write down how the parts of a system relate, check the code against that map, and where two parts must agree exactly, share a tiny kernel that both own. A context map records how the parts of a system relate; a shared kernel is a tiny model two parts share and change only together.
