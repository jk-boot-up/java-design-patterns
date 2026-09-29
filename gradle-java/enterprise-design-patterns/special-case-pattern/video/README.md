# Special Case Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `special-case-pattern-explained.mp4` | the video, 1920×1080 |
| `special-case-pattern-explained.m4a` | audio only |
| `special-case-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Instead of returning null for a guest or a missing account, return an object for that special case, which answers every question in the right way for it. A special case is an object that stands in for an unusual but normal situation, such as a guest or a deleted account, and answers every question the ordinary object would, in the way that fits.
