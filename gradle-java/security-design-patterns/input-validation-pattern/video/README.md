# Input Validation Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `input-validation-pattern-explained.mp4` | the video, 1920×1080 |
| `input-validation-pattern-explained.m4a` | audio only |
| `input-validation-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Check everything that comes from outside at the boundary, turn it into types that cannot hold bad values, report every problem at once, and still encode text on its way out. Input Validation checks everything from outside at the boundary, against rules for what is allowed, before the program uses it.
