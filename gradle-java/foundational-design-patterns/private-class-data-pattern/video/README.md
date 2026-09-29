# Private Class Data Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `private-class-data-pattern-explained.mp4` | the video, 1920×1080 |
| `private-class-data-pattern-explained.m4a` | audio only |
| `private-class-data-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Put the figures a class must never change into a private, unchangeable data object, so not even the class's own methods can overwrite them. Private class data moves the values a class must never change into a private, unchangeable data object, so not even the class's own methods can overwrite them.
