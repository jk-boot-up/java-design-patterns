# Railway-Oriented Programming Pattern — Teaching Video

A narrated, slide-based video built by `./build_video.sh` with the shared videokit library.

| File | What it is |
| --- | --- |
| `railway-oriented-pattern-explained.mp4` | the video, 1920×1080 |
| `railway-oriented-pattern-explained.m4a` | audio only |
| `railway-oriented-pattern-explained.srt` | subtitles |
| `poster.png` | the opening frame |

**Narration:** Piper `en_US-amy-medium`, speed 0.8, longer pauses (the approved `amy-slow` voice). Scenes are generated from `../pattern.toml` into `scenes.py`.

Suggested description:

> Let every step return a result that is either a success or a failure, and chain the steps so that the first failure switches to a failure track and the remaining steps are skipped. Railway-Oriented Programming chains steps that each return success or failure, so the first failure skips the rest and must be handled at the end.
