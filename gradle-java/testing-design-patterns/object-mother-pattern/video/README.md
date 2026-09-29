# Object Mother / Test Data Builder Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `object-mother-pattern-explained.mp4` | the video, 1920×1080 |
| `object-mother-pattern-explained.m4a` | audio only |
| `object-mother-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Give tests ready-made, named test objects (an Object Mother), or a builder with sensible defaults where each test states only the details it cares about (a Test Data Builder). An Object Mother hands tests named, ready-made objects; a Test Data Builder starts from defaults and lets each test state only what it cares about.
